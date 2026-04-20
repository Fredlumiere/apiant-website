import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";
import { getClientIp } from "../_shared/turnstile.ts";

const MAX_EVENT_DATA_CHARS = 4096;
const VALID_EVENT = /^[a-z0-9_\-.]{1,64}$/i;

Deno.serve(async (req: Request) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }

  try {
    const body = await req.json();
    const { session_id, event_type, event_data, source_page } = body;

    if (!session_id || typeof session_id !== "string" || session_id.length > 64) {
      return new Response(
        JSON.stringify({ error: "session_id required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (!event_type || typeof event_type !== "string" || !VALID_EVENT.test(event_type)) {
      return new Response(
        JSON.stringify({ error: "Invalid event_type" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    // Cap event_data size to prevent table bloat / DoS
    let safeEventData: unknown = {};
    if (event_data != null) {
      const serialized = JSON.stringify(event_data);
      if (serialized.length > MAX_EVENT_DATA_CHARS) {
        return new Response(
          JSON.stringify({ error: "event_data too large" }),
          { status: 413, headers: { ...cors, "Content-Type": "application/json" } },
        );
      }
      safeEventData = event_data;
    }

    const rl = await checkRateLimit(req, {
      bucket: "log-interaction",
      max: 120,
      windowSeconds: 60,
    });
    if (!rl.ok) return rateLimitResponse(cors, rl.retryAfterSec);

    const ip_address = getClientIp(req);
    const user_agent = (req.headers.get("user-agent") || "").slice(0, 500);
    const referrer = (req.headers.get("referer") || "").slice(0, 500);
    const safeSourcePage =
      typeof source_page === "string" ? source_page.slice(0, 500) : "";

    const supabase = getServiceClient();

    const { error } = await supabase.from("interaction_logs").insert({
      session_id: session_id.slice(0, 64),
      event_type,
      event_data: safeEventData,
      source_page: safeSourcePage,
      ip_address,
      user_agent,
      referrer,
    });

    if (error) {
      console.error("log-interaction insert error:", error.code || "unknown");
      return new Response(
        JSON.stringify({ error: "Failed to log interaction" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    return new Response(
      JSON.stringify({ success: true }),
      { status: 200, headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("log-interaction error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Server error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
