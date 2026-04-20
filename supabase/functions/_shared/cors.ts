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
export function getCorsHeaders(req: Request): Record<string, string> {
  const origin = req.headers.get("Origin") || "";
  const isDev = (Deno.env.get("ENV") || "").toLowerCase() === "dev";

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

  const devAllowed = isDev && origin.startsWith("http://localhost");
  const isAllowed = allowed.has(origin) || devAllowed;

  return {
    "Access-Control-Allow-Origin": isAllowed ? origin : "https://apiant.com",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}
