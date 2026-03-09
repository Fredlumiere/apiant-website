/**
 * CORS headers for edge functions.
 * Allows requests from apiant.com and Vercel preview deployments.
 */
export function getCorsHeaders(req: Request): Record<string, string> {
  const origin = req.headers.get("Origin") || "";
  const allowed = [
    "https://apiant.com",
    "https://www.apiant.com",
    "https://apiant-website.vercel.app",
  ];

  const isAllowed =
    allowed.includes(origin) ||
    origin.endsWith(".vercel.app") ||
    origin.startsWith("http://localhost");

  return {
    "Access-Control-Allow-Origin": isAllowed ? origin : allowed[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
  };
}
