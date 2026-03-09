/**
 * send-otp
 *
 * Sends a 6-digit verification code via email (Resend) or SMS/WhatsApp (Twilio).
 *
 * POST { contact: string, type: "email" | "sms" | "whatsapp", session_id: string }
 * Returns { success: true, message: string }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY");
const TWILIO_ACCOUNT_SID = Deno.env.get("TWILIO_ACCOUNT_SID");
const TWILIO_AUTH_TOKEN = Deno.env.get("TWILIO_AUTH_TOKEN");
const TWILIO_PHONE_NUMBER = Deno.env.get("TWILIO_PHONE_NUMBER");
const TWILIO_WHATSAPP_NUMBER = Deno.env.get("TWILIO_WHATSAPP_NUMBER");

function generateCode(): string {
  const array = new Uint32Array(1);
  crypto.getRandomValues(array);
  return String(array[0] % 1000000).padStart(6, "0");
}

async function sendEmail(email: string, code: string): Promise<void> {
  if (!RESEND_API_KEY) throw new Error("Email service not configured");

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: "APIANT <verify@apiant.com>",
      to: [email],
      subject: "Your APIANT verification code",
      html: `
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 480px; margin: 0 auto; padding: 40px 20px;">
          <div style="text-align: center; margin-bottom: 32px;">
            <img src="https://apiant.com/images/APIANT-LOGO-V4-Dark-Mode.svg" alt="APIANT" style="height: 32px;" />
          </div>
          <h2 style="color: #1a1a1a; font-size: 20px; margin-bottom: 8px;">Verification Code</h2>
          <p style="color: #666; font-size: 15px; line-height: 1.5; margin-bottom: 24px;">
            Enter this code to verify your identity:
          </p>
          <div style="background: #f5f5f5; border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 24px;">
            <span style="font-size: 36px; font-weight: 700; letter-spacing: 8px; color: #1a1a1a; font-family: monospace;">${code}</span>
          </div>
          <p style="color: #999; font-size: 13px; line-height: 1.4;">
            This code expires in 10 minutes. If you didn't request this, you can safely ignore it.
          </p>
        </div>
      `,
    }),
  });

  if (!res.ok) {
    const err = await res.text().catch(() => "");
    console.error("Resend error:", res.status, err);
    throw new Error("Failed to send verification email");
  }
}

async function sendSMS(phone: string, code: string): Promise<void> {
  if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN || !TWILIO_PHONE_NUMBER) {
    throw new Error("SMS service not configured");
  }

  const url = `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}/Messages.json`;
  const auth = btoa(`${TWILIO_ACCOUNT_SID}:${TWILIO_AUTH_TOKEN}`);

  const body = new URLSearchParams({
    To: phone,
    From: TWILIO_PHONE_NUMBER,
    Body: `Your APIANT verification code is: ${code}. It expires in 10 minutes.`,
  });

  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Basic ${auth}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body.toString(),
  });

  if (!res.ok) {
    const err = await res.text().catch(() => "");
    console.error("Twilio SMS error:", res.status, err);
    throw new Error("Failed to send verification SMS");
  }
}

async function sendWhatsApp(phone: string, code: string): Promise<void> {
  if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN || !TWILIO_WHATSAPP_NUMBER) {
    throw new Error("WhatsApp service not configured");
  }

  const url = `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}/Messages.json`;
  const auth = btoa(`${TWILIO_ACCOUNT_SID}:${TWILIO_AUTH_TOKEN}`);

  const body = new URLSearchParams({
    To: `whatsapp:${phone}`,
    From: `whatsapp:${TWILIO_WHATSAPP_NUMBER}`,
    Body: `Your APIANT verification code is: ${code}. It expires in 10 minutes.`,
  });

  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Basic ${auth}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body.toString(),
  });

  if (!res.ok) {
    const err = await res.text().catch(() => "");
    console.error("Twilio WhatsApp error:", res.status, err);
    throw new Error("Failed to send WhatsApp verification");
  }
}

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { contact, type, session_id } = await req.json();

    if (!contact || !type || !session_id) {
      return new Response(
        JSON.stringify({ error: "contact, type, and session_id are required" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (!["email", "sms", "whatsapp"].includes(type)) {
      return new Response(
        JSON.stringify({ error: "type must be email, sms, or whatsapp" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = getServiceClient();

    // Rate limit: max 3 OTPs per contact per 10 minutes
    const { count } = await supabase
      .from("otp_codes")
      .select("*", { count: "exact", head: true })
      .eq("contact", contact)
      .gte("created_at", new Date(Date.now() - 10 * 60 * 1000).toISOString());

    if ((count || 0) >= 3) {
      return new Response(
        JSON.stringify({ error: "Too many verification attempts. Please wait 10 minutes." }),
        { status: 429, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const code = generateCode();

    // Store OTP
    const { error: insertErr } = await supabase.from("otp_codes").insert({
      contact,
      contact_type: type,
      code,
      session_id,
    });

    if (insertErr) {
      console.error("OTP insert error:", insertErr);
      throw new Error("Failed to create verification code");
    }

    // Send code
    switch (type) {
      case "email":
        await sendEmail(contact, code);
        break;
      case "sms":
        await sendSMS(contact, code);
        break;
      case "whatsapp":
        await sendWhatsApp(contact, code);
        break;
    }

    const maskedContact = type === "email"
      ? contact.replace(/(.{2})(.*)(@.*)/, "$1***$3")
      : contact.replace(/(.{3})(.*)(.{2})/, "$1***$3");

    console.log(`[otp] Sent ${type} code to ${maskedContact}`);

    return new Response(
      JSON.stringify({ success: true, message: `Verification code sent to ${maskedContact}` }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("send-otp error:", e);
    return new Response(
      JSON.stringify({ error: e instanceof Error ? e.message : "Failed to send code" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
