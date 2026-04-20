import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { verifyTurnstile } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

const MAX_LEN = 4000;

async function notifyDiscord(params: {
  integration_need: string;
  source_page: string | null;
  domain: string | null;
  company_type: string | null;
}): Promise<void> {
  const url = Deno.env.get("DISCORD_FORUM_WEBHOOK_URL");
  if (!url) return;

  const embed = {
    title: "New Connector Request",
    description: params.integration_need,
    color: 0x1ab759,
    fields: [
      { name: "Company Domain", value: params.domain || "unknown", inline: true },
      { name: "Company Type", value: params.company_type || "unknown", inline: true },
      { name: "Source Page", value: params.source_page || "unknown", inline: false },
    ],
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

    if (!integration_need) {
      return new Response(
        JSON.stringify({ error: "integration_need is required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const sb = getServiceClient();
    const { error } = await sb.from("forum_requests").insert({
      integration_need,
      source_page,
      domain,
      company_type,
    });

    if (error) throw error;

    // Fan out to Discord server-side so the webhook URL never reaches the client.
    // Failure here must not break the user flow.
    try {
      await notifyDiscord({ integration_need, source_page, domain, company_type });
    } catch (_) { /* silent */ }

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...cors, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: (err as Error).message }), {
      status: 500,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }
});
