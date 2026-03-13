/**
 * submit-lead
 *
 * Saves a qualified lead to lead_sessions and returns a session ID
 * for WhatsApp handoff to ElevenLabs agent.
 *
 * POST {
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

function generateSessionId(): string {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";
  let result = "apt_";
  for (let i = 0; i < 8; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const body = await req.json();
    const {
      company_type,
      domain,
      company_description,
      detected_type,
      email,
      first_name,
      last_name,
      company_name,
      integration_needs,
      source_page,
    } = body;

    if (!email || !company_type) {
      return new Response(
        JSON.stringify({ error: "Email and company_type are required" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = getServiceClient();
    const session_id = generateSessionId();

    const { error } = await supabase.from("lead_sessions").insert({
      session_id,
      company_type,
      domain: domain || "",
      company_description: company_description || "",
      detected_type: detected_type || "",
      contact_email: email,
      contact_name: [first_name, last_name].filter(Boolean).join(" "),
      company_name: company_name || "",
      integration_needs: integration_needs || "",
      source_page: source_page || "",
    });

    if (error) {
      console.error("insert error:", error);
      return new Response(
        JSON.stringify({ error: "Failed to save lead" }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Also save to qualified_leads for backward compat with admin dashboard
    try {
      await supabase.from("qualified_leads").insert({
        company_type,
        domain: domain || "",
        domain_verified: !!company_description,
        verification_result: company_description
          ? { description: company_description, detected_type }
          : null,
        work_email: email,
        company_name: company_name || "",
        integration_needs: integration_needs || "",
        source_page: source_page || "",
      });
    } catch { /* non-critical */ }

    return new Response(
      JSON.stringify({ session_id }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("submit-lead error:", e);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
