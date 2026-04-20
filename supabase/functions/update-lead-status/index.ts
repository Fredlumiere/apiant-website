/**
 * update-lead-status
 *
 * Updates a lead session's conversation status.
 * Called by ElevenLabs agent during/after conversations.
 *
 * POST { session_id, status, handed_off_to? }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { timingSafeEqual } from "../_shared/auth.ts";

function checkBearer(req: Request): boolean {
  const expected = Deno.env.get("AGENT_BEARER_TOKEN");
  if (!expected) return false;
  const header = req.headers.get("Authorization") || "";
  const match = header.match(/^Bearer\s+(.+)$/i);
  if (!match) return false;
  return timingSafeEqual(match[1].trim(), expected);
}

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  if (!checkBearer(req)) {
    return new Response(
      JSON.stringify({ error: "Unauthorized" }),
      { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }

  try {
    const body = await req.json();
    const { session_id, status, handed_off_to } = body;

    if (!session_id || !/^apt_[A-Za-z0-9]{4,32}$/.test(session_id)) {
      return new Response(
        JSON.stringify({ error: "session_id required" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const validStatuses = ["active", "completed", "handed_off"];
    if (!validStatuses.includes(status)) {
      return new Response(
        JSON.stringify({ error: "Invalid status. Must be: active, completed, handed_off" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = getServiceClient();

    const safe_handed_off_to =
      typeof handed_off_to === "string" ? handed_off_to.slice(0, 200) : null;

    const { error } = await supabase
      .from("lead_sessions")
      .update({
        agent_conversation_status: status,
        handed_off_to: safe_handed_off_to,
        updated_at: new Date().toISOString(),
      })
      .eq("session_id", session_id);

    if (error) {
      console.error("update error:", error);
      return new Response(
        JSON.stringify({ error: "Update failed" }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("update-lead-status error:", e);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
