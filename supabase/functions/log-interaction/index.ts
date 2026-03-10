import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

Deno.serve(async (req: Request) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }

  try {
    const body = await req.json();
    const { session_id, event_type, event_data, source_page } = body;

    if (!session_id || !event_type) {
      return new Response(
        JSON.stringify({ error: "session_id and event_type required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    // Extract IP from request headers (Supabase edge functions provide this)
    const ip_address =
      req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
      req.headers.get("cf-connecting-ip") ||
      req.headers.get("x-real-ip") ||
      "unknown";

    const user_agent = req.headers.get("user-agent") || "";
    const referrer = req.headers.get("referer") || "";

    const supabase = getServiceClient();

    const { error } = await supabase.from("interaction_logs").insert({
      session_id,
      event_type,
      event_data: event_data || {},
      source_page: source_page || "",
      ip_address,
      user_agent,
      referrer,
    });

    if (error) {
      console.error("Insert error:", error);
      return new Response(
        JSON.stringify({ error: "Failed to log interaction" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ success: true }),
      { status: 200, headers: { ...cors, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("Error:", e);
    return new Response(
      JSON.stringify({ error: "Server error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } }
    );
  }
});
