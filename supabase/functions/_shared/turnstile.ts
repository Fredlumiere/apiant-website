/**
 * Cloudflare Turnstile server-side verification.
 *
 * Call verifyTurnstile() with the token the client submitted and reject
 * the request if it returns false. The secret lives in TURNSTILE_SECRET_KEY.
 *
 * In dev (ENV=dev) verification is skipped so local testing isn't blocked.
 */
const SITEVERIFY_URL =
  "https://challenges.cloudflare.com/turnstile/v0/siteverify";

export function getClientIp(req: Request): string {
  return (
    req.headers.get("cf-connecting-ip") ||
    req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    req.headers.get("x-real-ip") ||
    "0.0.0.0"
  );
}

export async function verifyTurnstile(
  token: string | undefined,
  req: Request,
): Promise<{ ok: boolean; reason?: string }> {
  // Turnstile is disabled for now: the offscreen widget blocked any
  // visitor Cloudflare chose to challenge. Verification is bypassed
  // site-wide until a replacement bot check (e.g. honeypot) is in place.
  // Re-enable by removing this short-circuit.
  return { ok: true };

  const secret = Deno.env.get("TURNSTILE_SECRET_KEY");
  const isDev = (Deno.env.get("ENV") || "").toLowerCase() === "dev";

  if (isDev && !secret) {
    return { ok: true };
  }

  if (!secret) {
    console.error("TURNSTILE_SECRET_KEY not configured");
    return { ok: false, reason: "server_misconfigured" };
  }

  if (!token || typeof token !== "string") {
    return { ok: false, reason: "missing_token" };
  }

  try {
    const body = new URLSearchParams({
      secret,
      response: token,
      remoteip: getClientIp(req),
    });

    const res = await fetch(SITEVERIFY_URL, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });

    if (!res.ok) return { ok: false, reason: "verify_http_error" };
    const data = await res.json();
    if (data.success === true) return { ok: true };
    return {
      ok: false,
      reason: Array.isArray(data["error-codes"])
        ? data["error-codes"].join(",")
        : "invalid_token",
    };
  } catch (e) {
    console.error("turnstile verify failed:", (e as Error).message);
    return { ok: false, reason: "verify_exception" };
  }
}
