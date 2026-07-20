/**
 * get-calendly-url
 *
 * Returns the Calendly scheduling URL for a named event type. Public endpoint,
 * but the URL is no longer published in static HTML: pages ship a placeholder
 * and js/calendly-loader.js fetches the URL here when the scheduler becomes
 * visible.
 *
 * Why: the CRMConnect discovery link was scraped from page source and used for
 * repeated spam bookings (the slug had already been rotated once). Serving the
 * URL at runtime lets us (1) keep it out of the HTML that scrapers see,
 * (2) rate limit disclosure per IP, and (3) rotate the slug at Calendly by
 * updating a single secret, with no site redeploy.
 *
 * GET /get-calendly-url?event=crmconnect
 * Returns { url: "https://calendly.com/..." } or 4xx.
 *
 * Event keys map to env secrets:
 *   crmconnect             -> CALENDLY_URL_CRMCONNECT
 *   calendarconnect        -> CALENDLY_URL_CALENDARCONNECT
 *   zoomconnect-onboarding -> CALENDLY_URL_ZOOMCONNECT_ONBOARDING
 *   shopconnect-onboarding -> CALENDLY_URL_SHOPCONNECT_ONBOARDING
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getAllowedOrigins, getCorsHeaders, isOriginAllowed } from "../_shared/cors.ts";
import { getClientIp } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

const EVENT_ENV: Record<string, string> = {
  "crmconnect": "CALENDLY_URL_CRMCONNECT",
  "calendarconnect": "CALENDLY_URL_CALENDARCONNECT",
  "zoomconnect-onboarding": "CALENDLY_URL_ZOOMCONNECT_ONBOARDING",
  "shopconnect-onboarding": "CALENDLY_URL_SHOPCONNECT_ONBOARDING",
};

// Same browser-context rule as submit-lead: a genuine request comes from one
// of our pages and carries an allowed Origin and/or Referer. Scripted scrapers
// usually have neither.
function hasBrowserContext(req: Request): boolean {
  if (isOriginAllowed(req)) return true;
  const referer = req.headers.get("Referer") || "";
  if (referer) {
    for (const origin of getAllowedOrigins()) {
      if (referer === origin || referer.startsWith(origin + "/")) return true;
    }
    const isDev = (Deno.env.get("ENV") || "").toLowerCase() === "dev";
    if (isDev && referer.startsWith("http://localhost")) return true;
  }
  return false;
}

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const event = (new URL(req.url).searchParams.get("event") || "").toLowerCase();
    const ip = getClientIp(req);

    if (!hasBrowserContext(req)) {
      console.log(JSON.stringify({ evt: "calendly_url_reject", reason: "no_browser_context", ip, event }));
      return new Response(
        JSON.stringify({ error: "Forbidden" }),
        { status: 403, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const envName = EVENT_ENV[event];
    if (!envName) {
      console.log(JSON.stringify({ evt: "calendly_url_reject", reason: "unknown_event", ip, event }));
      return new Response(
        JSON.stringify({ error: "Unknown event" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const rl = await checkRateLimit(req, { bucket: "get-calendly-url", max: 20, windowSeconds: 3600 });
    if (!rl.ok) {
      console.log(JSON.stringify({ evt: "calendly_url_reject", reason: "rate_limited", ip, event }));
      return rateLimitResponse(cors, rl.retryAfterSec);
    }

    const url = Deno.env.get(envName) || "";
    if (!url.startsWith("https://calendly.com/")) {
      console.error(`get-calendly-url: secret ${envName} missing or not a calendly.com URL`);
      return new Response(
        JSON.stringify({ error: "Unavailable" }),
        { status: 503, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    console.log(JSON.stringify({ evt: "calendly_url_serve", ip, event }));
    return new Response(
      JSON.stringify({ url }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("get-calendly-url error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
