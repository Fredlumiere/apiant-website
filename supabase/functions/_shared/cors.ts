/**
 * CORS headers for edge functions.
 *
 * Security model:
 * - apiant.com and www.apiant.com are always allowed in production.
 * - The exact production Vercel project hostname is allowed (not a wildcard).
 * - localhost is only allowed when the edge function is running in the dev
 *   environment (set ENV=dev on the Supabase project to enable local testing).
 *
 * A permissive "*.vercel.app" wildcard used to be here; it was removed
 * because any Vercel preview site could call our endpoints with credentials
 * and amplify other weaknesses (brute force, cost attacks, etc.).
 */
/** The set of browser origins permitted to call our edge functions. */
export function getAllowedOrigins(): Set<string> {
  const allowed = new Set<string>([
    "https://apiant.com",
    "https://www.apiant.com",
    "https://apiant-website.vercel.app",
  ]);

  // Optional extra origins from env, comma-separated (e.g. "https://staging.apiant.com")
  const extra = (Deno.env.get("ALLOWED_ORIGINS") || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  for (const o of extra) allowed.add(o);

  return allowed;
}

/**
 * True if the request carries an Origin we trust. localhost is accepted only
 * when ENV=dev. Used by endpoints that want to hard-reject cross-origin or
 * non-browser callers (CORS headers alone are advisory; browsers enforce them,
 * scripts do not).
 */
export function isOriginAllowed(req: Request): boolean {
  const origin = req.headers.get("Origin") || "";
  const isDev = (Deno.env.get("ENV") || "").toLowerCase() === "dev";
  if (isDev && origin.startsWith("http://localhost")) return true;
  return getAllowedOrigins().has(origin);
}

export function getCorsHeaders(req: Request): Record<string, string> {
  const origin = req.headers.get("Origin") || "";
  const isAllowed = isOriginAllowed(req);

  return {
    "Access-Control-Allow-Origin": isAllowed ? origin : "https://apiant.com",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}
