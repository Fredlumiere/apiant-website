import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { verifyTurnstile } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

const MAX_LEN = 4000;
const EMAIL_MAX_LEN = 254;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const REF_CODE_ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"; // no 0/O/1/I/l to avoid confusion
const REF_CODE_LEN = 4;

function generateRefCode(): string {
  const bytes = new Uint8Array(REF_CODE_LEN);
  crypto.getRandomValues(bytes);
  let out = "";
  for (const b of bytes) {
    out += REF_CODE_ALPHABET[b % REF_CODE_ALPHABET.length];
  }
  return out;
}

async function notifyDiscord(params: {
  integration_need: string;
  source_page: string | null;
  domain: string | null;
  company_type: string | null;
  ref_code: string;
  has_email: boolean;
}): Promise<void> {
  const url = Deno.env.get("DISCORD_FORUM_WEBHOOK_URL");
  if (!url) return;

  const fields = [
    { name: "Company Domain", value: params.domain || "unknown", inline: true },
    { name: "Company Type", value: params.company_type || "unknown", inline: true },
    { name: "Ref", value: params.ref_code, inline: true },
    { name: "Source Page", value: params.source_page || "unknown", inline: false },
  ];
  if (params.has_email) {
    fields.push({
      name: "Contact",
      value: "Poster left an email; APIANT will follow up directly if no community response.",
      inline: false,
    });
  }

  const embed = {
    title: "New Connector Request",
    description: params.integration_need,
    color: 0x1ab759,
    fields,
    timestamp: new Date().toISOString(),
  };

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "APIANT Website", embeds: [embed] }),
  });
  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    console.error("discord_fanout_failed", res.status, txt.slice(0, 200));
  }
}

serve(async (req: Request) => {
  const cors = getCorsHeaders(req);

  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: cors });
  }

  try {
    const body = await req.json();
    const turnstile = await verifyTurnstile(body.turnstile_token, req);
    if (!turnstile.ok) {
      return new Response(
        JSON.stringify({ error: "Verification failed. Please retry." }),
        { status: 403, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const rl = await checkRateLimit(req, { bucket: "save-forum-request", max: 10, windowSeconds: 3600 });
    if (!rl.ok) return rateLimitResponse(cors, rl.retryAfterSec);

    const integration_need = String(body.integration_need ?? "").trim().slice(0, MAX_LEN);
    const source_page = body.source_page ? String(body.source_page).slice(0, 500) : null;
    const domain = body.domain ? String(body.domain).slice(0, 253) : null;
    const company_type = body.company_type ? String(body.company_type).slice(0, 64) : null;

    // Email is optional but validated when present. Invalid addresses are
    // discarded silently so a typo doesn't block the submission.
    const rawEmail = body.email ? String(body.email).trim().slice(0, EMAIL_MAX_LEN) : "";
    const email = rawEmail && EMAIL_RE.test(rawEmail) ? rawEmail : null;

    if (!integration_need) {
      return new Response(
        JSON.stringify({ error: "integration_need is required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const ref_code = generateRefCode();

    const sb = getServiceClient();
    const { error } = await sb.from("forum_requests").insert({
      integration_need,
      source_page,
      domain,
      company_type,
      email,
      ref_code,
    });

    if (error) throw error;

    // Fan out to Discord server-side so the webhook URL never reaches the
    // client. Email is intentionally omitted from the Discord embed; only the
    // ref_code is public so admins can correlate a post back to the DB row.
    // Failure here must not break the user flow.
    try {
      await notifyDiscord({
        integration_need,
        source_page,
        domain,
        company_type,
        ref_code,
        has_email: !!email,
      });
    } catch (_) { /* silent */ }

    return new Response(JSON.stringify({ success: true, ref_code }), {
      headers: { ...cors, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: (err as Error).message }), {
      status: 500,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }
});
