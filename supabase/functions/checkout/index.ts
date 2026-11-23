/**
 * checkout
 *
 * The gate in front of Recurly for API App signups. It replaces the public
 * Recurly hosted payment pages (apiant.recurly.com/subscribe/<plan>), which a
 * card-testing bot used in November 2026 because nothing stood between an
 * anonymous request and a card authorisation.
 *
 * A card reaches the payment gateway only after, in this order:
 *   1. the request carries an allowed browser Origin,
 *   2. the per-IP and site-wide attempt limits have room,
 *   3. a Cloudflare Turnstile token verifies (or a signed pass from a
 *      verified first attempt, used only to finish a 3-D Secure challenge).
 *
 * Plans are addressed by a public alias ("shopconnect-monthly"). The alias to
 * Recurly plan code map lives in the CHECKOUT_PLANS secret, so the real plan
 * codes (which are the hosted page URLs) never appear in this public repo or
 * in any page.
 *
 * GET  ?plan=<alias>&add_on_code=a,b&add_on_quantity=1,2
 *        -> { ok, plan: { alias, name, interval, trial, lines[], recurring_total } }
 * POST { plan, add_on_code, add_on_quantity, token_id, turnstile_token,
 *        first_name, last_name, email, company,
 *        pass, three_d_secure_action_result_token_id }
 *        -> { ok: true, redirect }
 *         | { ok: false, three_d_secure_action_token_id, pass }
 *         | { error }
 *
 * Secrets: RECURLY_API_KEY, TURNSTILE_SECRET_KEY, CHECKOUT_PLANS,
 *          CHECKOUT_SIGNING_SECRET
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders, isOriginAllowed } from "../_shared/cors.ts";
import { getClientIp } from "../_shared/turnstile.ts";
import { checkRateLimit } from "../_shared/ratelimit.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { isValidEmail, normalizeEmail } from "../_shared/leadvalidate.ts";

const RECURLY = "https://v3.recurly.com";
const RECURLY_ACCEPT = "application/vnd.recurly.v2021-02-25";
const DEFAULT_REDIRECT = "https://apiant.com/";

/** Attempts one IP may make per hour. A person retyping a card needs a few. */
const PER_IP_MAX = 6;
/**
 * Attempts the whole site may make per hour. Normal volume is a handful of
 * signups a day; the bot made about 500 in one hour from 500 different IPs,
 * which no per-IP limit can see. Past this number checkout closes for the
 * rest of the window and the page tells people to contact us.
 */
const SITE_MAX = 40;
const PASS_TTL_MS = 15 * 60 * 1000;

type Json = Record<string, unknown>;

function logEvent(obj: Json): void {
  console.log(JSON.stringify(obj));
}

function cap(s: unknown, max: number): string {
  return typeof s === "string" ? s.slice(0, max).trim() : "";
}

function reply(cors: Record<string, string>, status: number, body: Json): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

function planMap(): Record<string, string> {
  try {
    const m = JSON.parse(Deno.env.get("CHECKOUT_PLANS") || "{}");
    return m && typeof m === "object" ? m : {};
  } catch (_e) {
    return {};
  }
}

async function recurly(path: string, init?: RequestInit): Promise<{ status: number; body: any }> {
  const key = Deno.env.get("RECURLY_API_KEY") || "";
  const res = await fetch(RECURLY + path, {
    ...init,
    headers: {
      "Authorization": "Basic " + btoa(key + ":"),
      "Accept": RECURLY_ACCEPT,
      // Deno sends "Accept-Language: *" by default and Recurly answers 406 to it.
      "Accept-Language": "en-US",
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  let body: any = null;
  try {
    body = await res.json();
  } catch (_e) {
    body = null;
  }
  return { status: res.status, body };
}

/* ---------- plan + add-on pricing ---------- */

interface AddOnLine { code: string; name: string; quantity: number; amount: number }
interface PlanView {
  alias: string;
  name: string;
  interval: string;
  trial: string;
  base: number;
  setup_fee: number;
  lines: AddOnLine[];
  recurring_total: number;
}
interface Resolved { view: PlanView; code: string; success_url: string; add_ons: { code: string; quantity: number }[] }

const planCache = new Map<string, { at: number; plan: any; addOns: any[] }>();

async function loadPlan(code: string): Promise<{ plan: any; addOns: any[] } | null> {
  const hit = planCache.get(code);
  if (hit && Date.now() - hit.at < 5 * 60 * 1000) return hit;
  const [p, a] = await Promise.all([
    recurly(`/plans/code-${encodeURIComponent(code)}`),
    recurly(`/plans/code-${encodeURIComponent(code)}/add_ons?state=active&limit=200`),
  ]);
  if (p.status !== 200 || !p.body || p.body.state !== "active") {
    logEvent({ evt: "checkout_plan_lookup_failed", status: p.status, state: p.body && p.body.state });
    return null;
  }
  const entry = { at: Date.now(), plan: p.body, addOns: (a.body && a.body.data) || [] };
  planCache.set(code, entry);
  return entry;
}

function usd(list: any[] | undefined, field: string): number {
  const c = (list || []).find((x) => x.currency === "USD");
  return c && typeof c[field] === "number" ? c[field] : 0;
}

function addOnAmount(addOn: any, qty: number): number {
  if (addOn.tier_type === "flat" || !addOn.tier_type) {
    return usd(addOn.currencies, "unit_amount") * qty;
  }
  const tiers: any[] = addOn.tiers || [];
  if (addOn.tier_type === "stairstep") {
    const tier = tiers.find((t) => t.ending_quantity == null || qty <= t.ending_quantity) || tiers[tiers.length - 1];
    return tier ? usd(tier.currencies, "unit_amount") : 0;
  }
  // tiered / volume: priced by Recurly at purchase; not itemised here.
  return NaN;
}

function plural(n: number, unit: string): string {
  const u = unit.replace(/s$/, "");
  return n === 1 ? u : `${n} ${u}s`;
}

async function resolve(alias: string, codesCsv: string, qtysCsv: string): Promise<Resolved | null> {
  const code = planMap()[alias];
  if (!code) return null;
  const loaded = await loadPlan(code);
  if (!loaded) return null;
  const { plan, addOns } = loaded;

  // The product pages send every calculator control, including zero
  // quantities and codes a plan does not carry. Keep what the plan sells.
  const codes = codesCsv ? codesCsv.split(",").map((s) => s.trim()).slice(0, 40) : [];
  const qtys = qtysCsv ? qtysCsv.split(",").map((s) => parseInt(s.trim(), 10)) : [];
  const wanted = new Map<string, number>();
  codes.forEach((c, i) => {
    const q = qtys[i];
    if (c && Number.isFinite(q) && q > 0 && q <= 100000) wanted.set(c, q);
  });

  const lines: AddOnLine[] = [];
  const purchase: { code: string; quantity: number }[] = [];
  for (const a of addOns) {
    const required = a.optional === false;
    const q = wanted.get(a.code) ?? (required ? (a.default_quantity || 1) : 0);
    if (!q) continue;
    purchase.push({ code: a.code, quantity: q });
    lines.push({ code: a.code, name: a.name, quantity: q, amount: addOnAmount(a, q) });
  }

  const base = usd(plan.currencies, "unit_amount");
  const setup = usd(plan.currencies, "setup_fee");
  const sum = lines.reduce((s, l) => s + l.amount, base);
  const trialLen = plan.trial_length || 0;

  return {
    code,
    success_url: (plan.hosted_pages && plan.hosted_pages.success_url) || DEFAULT_REDIRECT,
    add_ons: purchase,
    view: {
      alias,
      name: plan.name,
      interval: plural(plan.interval_length || 1, plan.interval_unit || "months"),
      trial: trialLen > 0 ? `${trialLen}-${(plan.trial_unit || "days").replace(/s$/, "")}` : "",
      base,
      setup_fee: setup,
      lines,
      recurring_total: sum,
    },
  };
}

/* ---------- bot check ---------- */

/**
 * Strict Turnstile verification. The shared verifyTurnstile() is switched off
 * site-wide (see _shared/turnstile.ts), which is right for lead forms and
 * wrong for an endpoint that authorises cards, so checkout verifies here and
 * fails closed on every error path.
 */
async function turnstileOk(token: string, req: Request): Promise<{ ok: boolean; reason?: string }> {
  const secret = Deno.env.get("TURNSTILE_SECRET_KEY");
  if (!secret) return { ok: false, reason: "server_misconfigured" };
  if (!token) return { ok: false, reason: "missing_token" };
  try {
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ secret, response: token, remoteip: getClientIp(req) }),
    });
    if (!res.ok) return { ok: false, reason: "verify_http_error" };
    const data = await res.json();
    if (data.success === true) return { ok: true };
    return { ok: false, reason: Array.isArray(data["error-codes"]) ? data["error-codes"].join(",") : "invalid_token" };
  } catch (_e) {
    return { ok: false, reason: "verify_exception" };
  }
}

async function hmac(data: string): Promise<string> {
  const secret = Deno.env.get("CHECKOUT_SIGNING_SECRET") || "";
  if (secret.length < 32) throw new Error("CHECKOUT_SIGNING_SECRET not configured");
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  return Array.from(new Uint8Array(sig)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

/** A pass proves this email + plan already cleared Turnstile minutes ago. */
async function issuePass(email: string, alias: string): Promise<string> {
  const exp = Date.now() + PASS_TTL_MS;
  return `${exp}.${await hmac(`${exp}|${email}|${alias}`)}`;
}

async function passOk(pass: string, email: string, alias: string): Promise<boolean> {
  const [expStr, sig] = (pass || "").split(".");
  const exp = parseInt(expStr, 10);
  if (!exp || !sig || exp < Date.now()) return false;
  let want: string;
  try {
    want = await hmac(`${exp}|${email}|${alias}`);
  } catch (_e) {
    return false;
  }
  if (want.length !== sig.length) return false;
  let diff = 0;
  for (let i = 0; i < want.length; i++) diff |= want.charCodeAt(i) ^ sig.charCodeAt(i);
  return diff === 0;
}

/** Site-wide attempt counter. Fails closed: a broken counter must not open the gate. */
async function siteWindowOk(): Promise<boolean> {
  try {
    const sb = getServiceClient();
    const since = new Date(Date.now() - 3600 * 1000).toISOString();
    const { count, error } = await sb
      .from("rate_limits")
      .select("*", { count: "exact", head: true })
      .eq("bucket", "checkout-site")
      .eq("key", "all")
      .gte("created_at", since);
    if (error) return false;
    if ((count ?? 0) >= SITE_MAX) return false;
    await sb.from("rate_limits").insert({ bucket: "checkout-site", key: "all" });
    return true;
  } catch (_e) {
    return false;
  }
}

/* ---------- handler ---------- */

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  const ip = getClientIp(req);

  try {
    if (req.method === "GET") {
      const u = new URL(req.url);
      const r = await resolve(cap(u.searchParams.get("plan"), 80), cap(u.searchParams.get("add_on_code"), 2000), cap(u.searchParams.get("add_on_quantity"), 400));
      if (!r) return reply(cors, 404, { error: "Unknown plan" });
      return reply(cors, 200, { ok: true, plan: r.view });
    }
    if (req.method !== "POST") return reply(cors, 405, { error: "Method not allowed" });

    // 1. Browser context. Scripts that omit or forge Origin stop here.
    if (!isOriginAllowed(req)) {
      logEvent({ evt: "checkout_reject", reason: "origin", ip });
      return reply(cors, 403, { error: "Forbidden" });
    }

    const body = await req.json();
    const alias = cap(body.plan, 80);
    const email = normalizeEmail(body.email);
    const first_name = cap(body.first_name, 80);
    const last_name = cap(body.last_name, 80);
    const company = cap(body.company, 200);
    const token_id = cap(body.token_id, 64);
    const threeDsResult = cap(body.three_d_secure_action_result_token_id, 64);

    if (!isValidEmail(email)) return reply(cors, 400, { error: "A valid email is required." });
    if (!first_name || !last_name) return reply(cors, 400, { error: "First and last name are required." });
    if (!/^[A-Za-z0-9_-]{10,64}$/.test(token_id)) return reply(cors, 400, { error: "Card details are missing. Please re-enter your card." });

    // 2. Attempt limits, counted before any gateway call.
    const rl = await checkRateLimit(req, { bucket: "checkout", max: PER_IP_MAX, windowSeconds: 3600 });
    if (!rl.ok) {
      logEvent({ evt: "checkout_reject", reason: "rate_limited", ip });
      return reply(cors, 429, { error: "Too many attempts. Please wait an hour or contact support@apiant.com." });
    }
    if (!(await siteWindowOk())) {
      logEvent({ evt: "checkout_reject", reason: "site_window", ip });
      return reply(cors, 429, { error: "Checkout is temporarily unavailable. Please contact support@apiant.com and we will set you up." });
    }

    // 3. Bot check: a fresh Turnstile token, or a pass when finishing 3-D Secure.
    let verified = false;
    if (threeDsResult && body.pass) verified = await passOk(cap(body.pass, 200), email, alias);
    if (!verified) {
      const t = await turnstileOk(cap(body.turnstile_token, 4096), req);
      if (!t.ok) {
        logEvent({ evt: "checkout_reject", reason: "turnstile", detail: t.reason, ip });
        return reply(cors, 403, { error: "We could not confirm you are a person. Please reload the page and try again." });
      }
    }

    const r = await resolve(alias, cap(body.add_on_code, 2000), cap(body.add_on_quantity, 400));
    if (!r) return reply(cors, 400, { error: "This plan is not available." });

    // An email that already holds a live subscription is an existing customer.
    // Adding a card to that account from an anonymous form would let anyone
    // who knows the email replace its billing details, so those go to support.
    const existing = await recurly(`/accounts/code-${encodeURIComponent(email)}`);
    if (existing.status === 200 && existing.body && existing.body.state === "active" && existing.body.has_live_subscription) {
      logEvent({ evt: "checkout_reject", reason: "existing_customer", ip });
      return reply(cors, 409, { error: "This email already has an APIANT subscription. Please contact support@apiant.com to add a product." });
    }

    const billing_info: Json = { token_id };
    if (threeDsResult) billing_info.three_d_secure_action_result_token_id = threeDsResult;

    const purchase = await recurly("/purchases", {
      method: "POST",
      body: JSON.stringify({
        currency: "USD",
        account: { code: email, email, first_name, last_name, company: company || undefined, billing_info },
        subscriptions: [{ plan_code: r.code, add_ons: r.add_ons.length ? r.add_ons : undefined }],
      }),
    });

    if (purchase.status === 200 || purchase.status === 201) {
      logEvent({ evt: "checkout_accept", plan: alias, ip });
      return reply(cors, 200, { ok: true, redirect: r.success_url });
    }

    const err = (purchase.body && purchase.body.error) || {};
    const txn = err.transaction_error || {};
    if (txn.three_d_secure_action_token_id) {
      logEvent({ evt: "checkout_3ds", plan: alias, ip });
      return reply(cors, 200, {
        ok: false,
        three_d_secure_action_token_id: txn.three_d_secure_action_token_id,
        pass: await issuePass(email, alias),
      });
    }

    logEvent({ evt: "checkout_declined", plan: alias, type: err.type, code: txn.code || null, ip });
    const msg = err.type === "transaction"
      ? (txn.message || "Your card was declined.")
      : err.type === "validation"
      ? "Some details were not accepted. Please check the form and try again."
      : "We could not complete the signup. Please try again or contact support@apiant.com.";
    return reply(cors, 402, { error: msg });
  } catch (e) {
    console.error("checkout error:", (e as Error).message);
    return reply(cors, 500, { error: "Internal error" });
  }
});
