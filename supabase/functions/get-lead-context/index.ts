/**
 * get-lead-context
 *
 * Retrieves lead session data for ElevenLabs agent.
 * Called by the agent when a new WhatsApp conversation starts.
 *
 * POST { session_id: "apt_XXXXXXXX" }
 * Returns full lead context or 404.
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  // Allow GET with query param or POST with body
  let session_id = "";

  if (req.method === "GET") {
    const url = new URL(req.url);
    session_id = url.searchParams.get("session_id") || "";
  } else {
    try {
      const body = await req.json();
      session_id = body.session_id || "";
    } catch {
      // fall through
    }
  }

  if (!session_id || !session_id.startsWith("apt_")) {
    return new Response(
      JSON.stringify({ error: "Invalid session ID" }),
      { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }

  try {
    const supabase = getServiceClient();

    const { data, error } = await supabase
      .from("lead_sessions")
      .select("*")
      .eq("session_id", session_id)
      .single();

    if (error || !data) {
      return new Response(
        JSON.stringify({ error: "Session not found" }),
        { status: 404, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Mark as opened on first retrieval
    if (!data.whatsapp_opened) {
      await supabase
        .from("lead_sessions")
        .update({
          whatsapp_opened: true,
          agent_conversation_status: "active",
          updated_at: new Date().toISOString(),
        })
        .eq("session_id", session_id);
    }

    return new Response(
      JSON.stringify({
        session_id: data.session_id,
        company_type: data.company_type,
        domain: data.domain,
        company_description: data.company_description,
        detected_type: data.detected_type,
        contact_email: data.contact_email,
        contact_name: data.contact_name,
        company_name: data.company_name,
        integration_needs: data.integration_needs,
        source_page: data.source_page,
      }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("get-lead-context error:", e);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
