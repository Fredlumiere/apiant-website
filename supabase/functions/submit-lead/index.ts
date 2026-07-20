/**
 * submit-lead
 *
 * Saves a qualified lead to lead_sessions and returns a session ID for
 * WhatsApp handoff to the ElevenLabs agent. Public endpoint.
 *
 * This is the single server-side validated entry point for lead submissions.
 * It validates + origin-checks + rate-limits the payload, persists it, then
 * relays a minimal validated copy to the downstream iPaaS webhook (see relay.ts).
 * The browser no longer POSTs to apiant.com/webhook directly.
 *
 * POST {
 *   turnstile_token,
 *   company_type, domain, company_description, detected_type,
 *   email, mobile, first_name, last_name, company_name,
 *   integration_needs, source_page, source_url, form_id
 * }
 *
 * Returns { session_id: "apt_XXXXXXXX" }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders, isOriginAllowed } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { verifyTurnstile, getClientIp } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";
import { isHoneypotTripped } from "../_shared/honeypot.ts";
import { relayToWebhook } from "../_shared/relay.ts";
import {
  isAllowedCompanyType,
  isValidEmail,
  normalizeCompanyType,
  normalizeEmail,
  parseEmailBlocklist,
  resolveSource,
} from "../_shared/leadvalidate.ts";

const SESSION_ID_BYTES = 8;
const SESSION_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";
const COMPANY_TYPE_LABELS: Record<string, string> = {
  saas: "SaaS Company",
  si: "System Integrator",
  enterprise: "Enterprise",
};

function generateSessionId(): string {
  const bytes = new Uint8Array(SESSION_ID_BYTES);
  crypto.getRandomValues(bytes);
  let out = "apt_";
  for (let i = 0; i < bytes.length; i++) {
    out += SESSION_CHARS.charAt(bytes[i] % SESSION_CHARS.length);
  }
  return out;
}

function cap(s: unknown, max: number): string {
  return typeof s === "string" ? s.slice(0, max) : "";
}

// One JSON object per decision so accepted/rejected submissions are greppable.
function logEvent(obj: Record<string, unknown>): void {
  console.log(JSON.stringify(obj));
}

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const body = await req.json();

    // Honeypot bot trap: a hidden form field that humans leave blank. If it is
    // filled, the request is a bot. Return a benign success shape and persist
    // nothing, so the bot cannot tell its submission was dropped.
    if (isHoneypotTripped(body)) {
      logEvent({ evt: "lead_reject", reason: "honeypot", ip: getClientIp(req), form_id: cap(body.form_id, 64) });
      return new Response(
        JSON.stringify({ ok: true }),
        { headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    // Origin / browser-context enforcement. A genuine submission comes from one
    // of our pages and carries an allowed Origin and/or Referer. Direct scripted
    // POSTs (the legacy/abuse path) usually have neither. Reject those.
    const isDev = (Deno.env.get("ENV") || "").toLowerCase() === "dev";
    const originAllowed = isOriginAllowed(req);
    const source = resolveSource(
      { origin: req.headers.get("Origin"), referer: req.headers.get("Referer") },
      body.source_url,
      originAllowed,
      isDev,
    );
    if (!source.hasBrowserContext) {
      logEvent({ evt: "lead_reject", reason: "no_browser_context", ip: getClientIp(req), form_id: cap(body.form_id, 64) });
      return new Response(
        JSON.stringify({ error: "Forbidden" }),
        { status: 403, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const turnstile = await verifyTurnstile(body.turnstile_token, req);
    if (!turnstile.ok) {
      return new Response(
        JSON.stringify({ error: "Verification failed. Please retry." }),
        { status: 403, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const rl = await checkRateLimit(req, { bucket: "submit-lead", max: 10, windowSeconds: 3600 });
    if (!rl.ok) {
      logEvent({ evt: "lead_reject", reason: "rate_limited", ip: getClientIp(req), form_id: cap(body.form_id, 64) });
      return rateLimitResponse(cors, rl.retryAfterSec);
    }

    const email = normalizeEmail(body.email);
    const company_type = normalizeCompanyType(body.company_type);
    const form_id = cap(body.form_id, 64) || "unknown";
    const first_name = cap(body.first_name, 80).trim();
    const last_name = cap(body.last_name, 80).trim();
    const job_title = cap(body.job_title, 120).trim();

    if (!isValidEmail(email)) {
      logEvent({ evt: "lead_reject", reason: "invalid_email", ip: getClientIp(req), form_id });
      return new Response(
        JSON.stringify({ error: "A valid email is required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    // Known-abusive senders (BLOCKED_EMAILS secret, comma-separated). Treated
    // like the honeypot: benign success shape, nothing persisted or relayed,
    // so the sender cannot tell they are blocked.
    if (parseEmailBlocklist(Deno.env.get("BLOCKED_EMAILS")).has(email)) {
      logEvent({ evt: "lead_reject", reason: "blocklisted", ip: getClientIp(req), form_id });
      return new Response(
        JSON.stringify({ ok: true }),
        { headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (!isAllowedCompanyType(company_type)) {
      logEvent({ evt: "lead_reject", reason: "invalid_company_type", ip: getClientIp(req), form_id, company_type });
      return new Response(
        JSON.stringify({ error: "Invalid company_type" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (!first_name || !last_name) {
      logEvent({ evt: "lead_reject", reason: "missing_name", ip: getClientIp(req), form_id });
      return new Response(
        JSON.stringify({ error: "First and last name are required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    // job_title is required only for forms that collect it (builder-pricing,
    // start-building). Other lead pages don't collect it, so a global requirement
    // would reject them.
    if ((form_id === "builder-pricing" || form_id === "start-building") && !job_title) {
      logEvent({ evt: "lead_reject", reason: "missing_job_title", ip: getClientIp(req), form_id });
      return new Response(
        JSON.stringify({ error: "Job title is required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    // Call-now is a follow-up signal fired after the lead was already submitted
    // (user clicks "call me now"). Relay only the WantsCallNow flag to the lead
    // downstream; do not create a second lead_sessions row and do not let the
    // ip+email idempotency window drop it.
    if (body.wants_call_now === true) {
      const cnRelay = await relayToWebhook({
        company_type,
        company_type_label: COMPANY_TYPE_LABELS[company_type] || company_type,
        domain: cap(body.domain, 253),
        email,
        mobile: cap(body.mobile, 40),
        first_name,
        last_name,
        job_title,
        company_name: cap(body.company_name, 200),
        integration_needs: cap(body.integration_needs, 4000),
        page_title: cap(body.source_page, 500),
        wants_call_now: true,
      });
      logEvent({
        evt: "lead_accept",
        form_id,
        event: "call_now",
        relay: cnRelay.skipped ? "skipped" : (cnRelay.ok ? "ok" : "failed"),
        relay_status: cnRelay.status ?? null,
        ip: getClientIp(req),
      });
      return new Response(
        JSON.stringify({ ok: true }),
        { headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    // Replay / double-submit protection: dedupe on ip+email over a short window.
    // A duplicate is treated as success (benign) but is NOT persisted or relayed
    // again, so a double-click or retry cannot create duplicate leads.
    const idem = await checkRateLimit(req, {
      bucket: "submit-lead-idem",
      subject: email,
      max: 1,
      windowSeconds: 120,
    });
    if (!idem.ok) {
      logEvent({ evt: "lead_reject", reason: "duplicate", ip: getClientIp(req), form_id });
      return new Response(
        JSON.stringify({ ok: true, duplicate: true }),
        { headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const domain = cap(body.domain, 253);
    const company_description = cap(body.company_description, 2000);
    const detected_type = cap(body.detected_type, 32);
    const company_name = cap(body.company_name, 200);
    const integration_needs = cap(body.integration_needs, 4000);
    const source_page = cap(body.source_page, 500);
    const mobile = cap(body.mobile, 40);

    const supabase = getServiceClient();
    const session_id = generateSessionId();

    const { error } = await supabase.from("lead_sessions").insert({
      session_id,
      company_type,
      domain,
      company_description,
      detected_type,
      contact_email: email,
      contact_name: [first_name, last_name].filter(Boolean).join(" "),
      company_name,
      integration_needs,
      source_page,
    });

    if (error) {
      console.error("submit-lead insert error:", error.code || "unknown");
      return new Response(
        JSON.stringify({ error: "Failed to save lead" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    try {
      await supabase.from("qualified_leads").insert({
        company_type,
        domain,
        domain_verified: !!company_description,
        verification_result: company_description
          ? { description: company_description, detected_type }
          : null,
        work_email: email,
        company_name,
        integration_needs,
        source_page,
      });
    } catch { /* non-critical */ }

    // Relay a minimal, validated copy to the downstream iPaaS webhook. Env-gated
    // (APIANT_LEAD_WEBHOOK_URL); failures are logged but never fail the request
    // because the lead is already persisted above.
    const relay = await relayToWebhook({
      company_type,
      company_type_label: COMPANY_TYPE_LABELS[company_type] || company_type,
      domain,
      email,
      mobile,
      first_name,
      last_name,
      job_title,
      company_name,
      integration_needs,
      page_title: source_page,
    });

    // Structured tracing line: one JSON object per accepted lead so the source
    // page and form can be recovered from logs without DB access.
    logEvent({
      evt: "lead_accept",
      session_id,
      form_id,
      company_type,
      // Prefer the validated client URL (full path) over Referer, which is
      // usually trimmed to origin-only by the browser's referrer policy.
      source_url: source.clientUrl || source.refererUrl || null,
      source_page,
      origin_allowed: originAllowed,
      relay: relay.skipped ? "skipped" : (relay.ok ? "ok" : "failed"),
      relay_status: relay.status ?? null,
      ip: getClientIp(req),
    });

    return new Response(
      JSON.stringify({ session_id }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("submit-lead error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
