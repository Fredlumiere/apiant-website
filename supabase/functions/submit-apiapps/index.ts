/**
 * submit-apiapps
 *
 * Server-side validated endpoint for the Contact Us form (#contact-us-form) on
 * the apiapps / partner product pages. Validates + origin-checks + rate-limits,
 * then relays a minimal validated copy to the apiapps downstream webhook
 * (APIANT_APIAPPS_WEBHOOK_URL). The browser no longer POSTs to apiant.com/webhook.
 *
 * POST { PageTitle, FirstName, LastName, Company, WorkEmail, Mobile, Country,
 *        IntegrationNeeds, company_url (honeypot), form_id }
 * Returns { ok: true }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders, isOriginAllowed } from "../_shared/cors.ts";
import { getClientIp } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";
import { isHoneypotTripped } from "../_shared/honeypot.ts";
import { relayContact } from "../_shared/relay.ts";
import { isValidEmail, normalizeEmail, resolveSource } from "../_shared/leadvalidate.ts";

function cap(s: unknown, max: number): string {
  return typeof s === "string" ? s.slice(0, max) : "";
}

function logEvent(obj: Record<string, unknown>): void {
  console.log(JSON.stringify(obj));
}

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const body = await req.json();
    const form_id = cap(body.form_id, 64) || "contact-us";

    // Honeypot: filled hidden field => bot. Benign success, no relay.
    if (isHoneypotTripped(body)) {
      logEvent({ evt: "apiapps_reject", reason: "honeypot", ip: getClientIp(req), form_id });
      return new Response(JSON.stringify({ ok: true }), { headers: { ...cors, "Content-Type": "application/json" } });
    }

    // Origin / browser-context enforcement (reject scripted/forged POSTs).
    const isDev = (Deno.env.get("ENV") || "").toLowerCase() === "dev";
    const originAllowed = isOriginAllowed(req);
    const source = resolveSource(
      { origin: req.headers.get("Origin"), referer: req.headers.get("Referer") },
      body.source_url,
      originAllowed,
      isDev,
    );
    if (!source.hasBrowserContext) {
      logEvent({ evt: "apiapps_reject", reason: "no_browser_context", ip: getClientIp(req), form_id });
      return new Response(JSON.stringify({ error: "Forbidden" }), { status: 403, headers: { ...cors, "Content-Type": "application/json" } });
    }

    const rl = await checkRateLimit(req, { bucket: "submit-apiapps", max: 8, windowSeconds: 3600 });
    if (!rl.ok) {
      logEvent({ evt: "apiapps_reject", reason: "rate_limited", ip: getClientIp(req), form_id });
      return rateLimitResponse(cors, rl.retryAfterSec);
    }

    const email = normalizeEmail(body.WorkEmail);
    const first_name = cap(body.FirstName, 80).trim();
    const last_name = cap(body.LastName, 80).trim();

    if (!isValidEmail(email)) {
      logEvent({ evt: "apiapps_reject", reason: "invalid_email", ip: getClientIp(req), form_id });
      return new Response(JSON.stringify({ error: "A valid email is required" }), { status: 400, headers: { ...cors, "Content-Type": "application/json" } });
    }
    if (!first_name || !last_name) {
      logEvent({ evt: "apiapps_reject", reason: "missing_name", ip: getClientIp(req), form_id });
      return new Response(JSON.stringify({ error: "First and last name are required" }), { status: 400, headers: { ...cors, "Content-Type": "application/json" } });
    }

    // Replay / double-submit protection: dedupe on ip+email over a short window.
    const idem = await checkRateLimit(req, { bucket: "submit-apiapps-idem", subject: email, max: 1, windowSeconds: 120 });
    if (!idem.ok) {
      logEvent({ evt: "apiapps_reject", reason: "duplicate", ip: getClientIp(req), form_id });
      return new Response(JSON.stringify({ ok: true, duplicate: true }), { headers: { ...cors, "Content-Type": "application/json" } });
    }

    const relay = await relayContact({
      page_title: cap(body.PageTitle, 300),
      first_name,
      last_name,
      company: cap(body.Company, 200),
      email,
      mobile: cap(body.Mobile, 40),
      country: cap(body.Country, 80),
      integration_needs: cap(body.IntegrationNeeds, 4000),
    });

    logEvent({
      evt: "apiapps_accept",
      form_id,
      downstream: "apiapps",
      relay: relay.skipped ? "skipped" : (relay.ok ? "ok" : "failed"),
      relay_status: relay.status ?? null,
      origin_allowed: originAllowed,
      ip: getClientIp(req),
    });

    return new Response(JSON.stringify({ ok: true }), { headers: { ...cors, "Content-Type": "application/json" } });
  } catch (e) {
    console.error("submit-apiapps error:", (e as Error).message);
    return new Response(JSON.stringify({ error: "Internal error" }), { status: 500, headers: { ...cors, "Content-Type": "application/json" } });
  }
});
