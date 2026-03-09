/**
 * verify-otp
 *
 * Verifies a 6-digit OTP code against the stored code for a session.
 *
 * POST { code: string, session_id: string }
 * Returns { verified: true } or { error: string }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { code, session_id } = await req.json();

    if (!code || !session_id) {
      return new Response(
        JSON.stringify({ error: "code and session_id are required" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = getServiceClient();

    // Find the most recent unexpired, unverified OTP for this session
    const { data: otpRow, error: fetchErr } = await supabase
      .from("otp_codes")
      .select("*")
      .eq("session_id", session_id)
      .eq("verified", false)
      .gte("expires_at", new Date().toISOString())
      .order("created_at", { ascending: false })
      .limit(1)
      .maybeSingle();

    if (fetchErr) {
      console.error("OTP fetch error:", fetchErr);
      throw new Error("Verification failed");
    }

    if (!otpRow) {
      return new Response(
        JSON.stringify({ error: "Code expired or not found. Please request a new one." }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Check max attempts (5)
    if (otpRow.attempts >= 5) {
      return new Response(
        JSON.stringify({ error: "Too many incorrect attempts. Please request a new code." }),
        { status: 429, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Increment attempts
    await supabase
      .from("otp_codes")
      .update({ attempts: otpRow.attempts + 1 })
      .eq("id", otpRow.id);

    // Verify code
    if (otpRow.code !== code.trim()) {
      const remaining = 4 - otpRow.attempts;
      return new Response(
        JSON.stringify({
          error: remaining > 0
            ? `Incorrect code. ${remaining} attempt${remaining === 1 ? "" : "s"} remaining.`
            : "Too many incorrect attempts. Please request a new code.",
        }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Mark as verified
    await supabase
      .from("otp_codes")
      .update({ verified: true })
      .eq("id", otpRow.id);

    console.log(`[otp] Verified ${otpRow.contact_type} for session ${session_id}`);

    return new Response(
      JSON.stringify({ verified: true }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("verify-otp error:", e);
    return new Response(
      JSON.stringify({ error: e instanceof Error ? e.message : "Verification failed" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
