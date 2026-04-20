/**
 * contact-form
 *
 * Receives contact form submissions from the AI Advantage page
 * and sends an email notification via Resend.
 *
 * POST { name, email, company, message }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { verifyTurnstile } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function cap(s: unknown, max: number): string {
  return typeof s === "string" ? s.slice(0, max) : "";
}

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const body = await req.json();
    const turnstile = await verifyTurnstile(body.turnstile_token, req);
    if (!turnstile.ok) {
      return new Response(
        JSON.stringify({ error: "Verification failed. Please retry." }),
        { status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const rl = await checkRateLimit(req, { bucket: "contact-form", max: 5, windowSeconds: 3600 });
    if (!rl.ok) return rateLimitResponse(corsHeaders, rl.retryAfterSec);

    const name = cap(body.name, 120).trim();
    const email = cap(body.email, 254).trim();
    const company = cap(body.company, 200).trim();
    const message = cap(body.message, 4000).trim();

    if (!name || !email || !EMAIL_RE.test(email)) {
      return new Response(
        JSON.stringify({ error: "Name and a valid email are required" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const resendKey = Deno.env.get("RESEND_API_KEY");
    if (!resendKey) {
      throw new Error("RESEND_API_KEY not configured");
    }

    const htmlBody = `
      <h2>New Inquiry from AI Advantage Page</h2>
      <table style="border-collapse:collapse;width:100%;max-width:600px;">
        <tr><td style="padding:8px 12px;border:1px solid #ddd;font-weight:bold;width:120px;">Name</td><td style="padding:8px 12px;border:1px solid #ddd;">${escapeHtml(name)}</td></tr>
        <tr><td style="padding:8px 12px;border:1px solid #ddd;font-weight:bold;">Email</td><td style="padding:8px 12px;border:1px solid #ddd;"><a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a></td></tr>
        ${company ? `<tr><td style="padding:8px 12px;border:1px solid #ddd;font-weight:bold;">Organization</td><td style="padding:8px 12px;border:1px solid #ddd;">${escapeHtml(company)}</td></tr>` : ""}
        ${message ? `<tr><td style="padding:8px 12px;border:1px solid #ddd;font-weight:bold;">Message</td><td style="padding:8px 12px;border:1px solid #ddd;">${escapeHtml(message)}</td></tr>` : ""}
      </table>
      <p style="color:#666;font-size:12px;margin-top:16px;">Sent from apiant-ai-advantage.html</p>
    `;

    const resendRes = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${resendKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "APIANT <verify@apiant.com>",
        to: ["fredl@apiant.com"],
        // reply_to is set from unverified user input; only include it if it parses cleanly.
        ...(EMAIL_RE.test(email) ? { reply_to: email } : {}),
        subject: `AI Advantage Inquiry from ${name}${company ? ` (${company})` : ""}`,
        html: htmlBody,
      }),
    });

    if (!resendRes.ok) {
      const errText = await resendRes.text();
      console.error("Resend error:", errText);
      throw new Error("Failed to send email");
    }

    return new Response(
      JSON.stringify({ success: true }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err) {
    console.error("contact-form error:", err);
    return new Response(
      JSON.stringify({ error: "Failed to send message" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
