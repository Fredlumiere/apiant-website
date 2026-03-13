/**
 * check-availability
 *
 * Checks if the admin is available for a live call right now.
 * Considers both the manual toggle and configured business hours.
 *
 * GET or POST (no body needed)
 * Returns {
 *   available: boolean,
 *   calendly_url: string,
 *   reason: "available" | "after_hours" | "unavailable"
 * }
 *
 * POST { action: "toggle", password: string } - Toggle availability
 * POST { action: "update_settings", password: string, ...settings } - Update settings
 * POST { action: "get_settings", password: string } - Get current settings
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

function isWithinBusinessHours(
  timezone: string,
  startTime: string,
  endTime: string,
  businessDays: number[]
): boolean {
  try {
    const now = new Date();
    const formatter = new Intl.DateTimeFormat("en-US", {
      timeZone: timezone,
      hour: "numeric",
      minute: "numeric",
      hour12: false,
      weekday: "short",
    });

    const parts = formatter.formatToParts(now);
    const hour = parseInt(parts.find((p) => p.type === "hour")?.value || "0");
    const minute = parseInt(parts.find((p) => p.type === "minute")?.value || "0");
    const weekday = parts.find((p) => p.type === "weekday")?.value || "";

    const dayMap: Record<string, number> = {
      Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6,
    };
    const currentDay = dayMap[weekday] ?? new Date().getDay();

    if (!businessDays.includes(currentDay)) return false;

    const currentMinutes = hour * 60 + minute;
    const [startH, startM] = startTime.split(":").map(Number);
    const [endH, endM] = endTime.split(":").map(Number);
    const startMinutes = startH * 60 + startM;
    const endMinutes = endH * 60 + endM;

    return currentMinutes >= startMinutes && currentMinutes < endMinutes;
  } catch (e) {
    console.error("Business hours check failed:", e);
    return false;
  }
}

async function verifyAdmin(supabase: ReturnType<typeof getServiceClient>, password: string, email?: string): Promise<boolean> {
  const { data } = await supabase
    .from("admin_settings")
    .select("admin_password_hash, admin_email")
    .eq("id", 1)
    .single();

  if (!data?.admin_password_hash) return false;

  if (email && data.admin_email && email.toLowerCase() !== data.admin_email.toLowerCase()) {
    return false;
  }

  const encoder = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest("SHA-256", encoder.encode(password));
  const hashHex = Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  return hashHex === data.admin_password_hash;
}

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const supabase = getServiceClient();

    // Handle admin actions
    if (req.method === "POST") {
      let body: Record<string, unknown> = {};
      try { body = await req.json(); } catch { /* empty body is fine for availability check */ }

      if (body.action) {
        // Admin actions require password
        if (!body.password || !(await verifyAdmin(supabase, body.password as string, body.email as string | undefined))) {
          return new Response(
            JSON.stringify({ error: "Unauthorized" }),
            { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
          );
        }

        if (body.action === "toggle") {
          const { data: current } = await supabase
            .from("admin_settings")
            .select("available")
            .eq("id", 1)
            .single();

          const newValue = !(current?.available ?? false);

          await supabase
            .from("admin_settings")
            .update({ available: newValue, updated_at: new Date().toISOString() })
            .eq("id", 1);

          return new Response(
            JSON.stringify({ success: true, available: newValue }),
            { headers: { ...corsHeaders, "Content-Type": "application/json" } }
          );
        }

        if (body.action === "get_settings") {
          const { data } = await supabase
            .from("admin_settings")
            .select("available, timezone, business_hours_start, business_hours_end, business_days, calendly_url")
            .eq("id", 1)
            .single();

          return new Response(
            JSON.stringify(data || {}),
            { headers: { ...corsHeaders, "Content-Type": "application/json" } }
          );
        }

        if (body.action === "update_settings") {
          const updates: Record<string, unknown> = { updated_at: new Date().toISOString() };
          if (body.timezone !== undefined) updates.timezone = body.timezone;
          if (body.business_hours_start !== undefined) updates.business_hours_start = body.business_hours_start;
          if (body.business_hours_end !== undefined) updates.business_hours_end = body.business_hours_end;
          if (body.business_days !== undefined) updates.business_days = body.business_days;
          if (body.calendly_url !== undefined) updates.calendly_url = body.calendly_url;
          if (body.available !== undefined) updates.available = body.available;

          await supabase
            .from("admin_settings")
            .update(updates)
            .eq("id", 1);

          return new Response(
            JSON.stringify({ success: true }),
            { headers: { ...corsHeaders, "Content-Type": "application/json" } }
          );
        }
      }
    }

    // Public availability check
    const { data: settings } = await supabase
      .from("admin_settings")
      .select("available, timezone, business_hours_start, business_hours_end, business_days, calendly_url")
      .eq("id", 1)
      .single();

    if (!settings) {
      return new Response(
        JSON.stringify({ available: false, calendly_url: "", reason: "unavailable" }),
        { headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const withinHours = isWithinBusinessHours(
      settings.timezone,
      settings.business_hours_start,
      settings.business_hours_end,
      settings.business_days
    );

    let available = false;
    let reason = "unavailable";

    if (!withinHours) {
      reason = "after_hours";
    } else if (!settings.available) {
      reason = "unavailable";
    } else {
      available = true;
      reason = "available";
    }

    return new Response(
      JSON.stringify({
        available,
        calendly_url: settings.calendly_url || "",
        reason,
      }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("check-availability error:", e);
    return new Response(
      JSON.stringify({ available: false, calendly_url: "", reason: "error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
