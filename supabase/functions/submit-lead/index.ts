/**
 * submit-lead
 *
 * Saves a qualified lead to lead_sessions and returns a session ID for
 * WhatsApp handoff to the ElevenLabs agent. Public endpoint.
 *
 * POST {
 *   turnstile_token,
 *   company_type, domain, company_description, detected_type,
 *   email, first_name, last_name, company_name,
 *   integration_needs, source_page
 * }
 *
 * Returns { session_id: "apt_XXXXXXXX" }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { verifyTurnstile } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

const SESSION_ID_BYTES = 8;
const SESSION_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";
const ALLOWED_COMPANY_TYPES = new Set([
  "saas", "si", "enterprise", "fitness", "healthcare", "nonprofit", "other",
]);
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

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

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const body = await req.json();
    const turnstile = await verifyTurnstile(body.turnstile_token, req);
    if (!turnstile.ok) {
      return new Response(
        JSON.stringify({ error: "Verification failed. Please retry." }),
        { status: 403, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const rl = await checkRateLimit(req, { bucket: "submit-lead", max: 10, windowSeconds: 3600 });
    if (!rl.ok) return rateLimitResponse(cors, rl.retryAfterSec);

    const email = cap(body.email, 254).trim().toLowerCase();
    const company_type = cap(body.company_type, 32).trim().toLowerCase();

    if (!email || !EMAIL_RE.test(email)) {
      return new Response(
        JSON.stringify({ error: "A valid email is required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (!ALLOWED_COMPANY_TYPES.has(company_type)) {
      return new Response(
        JSON.stringify({ error: "Invalid company_type" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const domain = cap(body.domain, 253);
    const company_description = cap(body.company_description, 2000);
    const detected_type = cap(body.detected_type, 32);
    const first_name = cap(body.first_name, 80);
    const last_name = cap(body.last_name, 80);
    const company_name = cap(body.company_name, 200);
    const integration_needs = cap(body.integration_needs, 4000);
    const source_page = cap(body.source_page, 500);

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
