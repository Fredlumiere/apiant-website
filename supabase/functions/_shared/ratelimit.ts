/**
 * Per-IP rate limiter backed by the rate_limits table.
 *
 * Each call inserts a row; then a count-in-window query decides whether to
 * allow. Old rows are purged opportunistically on every call. This is a
 * simple fixed-window counter and is "good enough" for abuse defense in
 * front of costly APIs (Firecrawl, Claude, Twilio, Resend).
 *
 * The table must exist — see migration 20260418_001_rate_limits.sql.
 */
import { getServiceClient } from "./supabase.ts";
import { getClientIp } from "./turnstile.ts";

export interface RateLimitOptions {
  /** Unique key for the endpoint ("submit-lead", "verify-company-type", etc.) */
  bucket: string;
  /** Max requests within windowSeconds before returning ok:false */
  max: number;
  /** Window in seconds */
  windowSeconds: number;
  /** Optional extra key (e.g. normalized email / domain) to segment further */
  subject?: string;
}

export interface RateLimitResult {
  ok: boolean;
  retryAfterSec?: number;
  count: number;
}

export async function checkRateLimit(
  req: Request,
  opts: RateLimitOptions,
): Promise<RateLimitResult> {
  const ip = getClientIp(req);
  const key = opts.subject ? `${ip}|${opts.subject}` : ip;
  const windowStart = new Date(Date.now() - opts.windowSeconds * 1000).toISOString();
  const sb = getServiceClient();

  try {
    // Count existing hits in window
    const { count } = await sb
      .from("rate_limits")
      .select("*", { count: "exact", head: true })
      .eq("bucket", opts.bucket)
      .eq("key", key)
      .gte("created_at", windowStart);

    const currentCount = count ?? 0;

    if (currentCount >= opts.max) {
      return {
        ok: false,
        retryAfterSec: opts.windowSeconds,
        count: currentCount,
      };
    }

    // Record this hit (non-blocking semantics — if insert fails we still allow)
    await sb.from("rate_limits").insert({ bucket: opts.bucket, key });

    // Opportunistic cleanup: remove rows older than 24h for this bucket.
    // Don't await aggressively to avoid slowing the hot path.
    sb.from("rate_limits")
      .delete()
      .lt(
        "created_at",
        new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      )
      .then(() => {}, () => {});

    return { ok: true, count: currentCount + 1 };
  } catch (e) {
    console.error("rate limit error:", (e as Error).message);
    // Fail open so an outage in the limiter doesn't take down all traffic.
    return { ok: true, count: 0 };
  }
}

export function rateLimitResponse(
  cors: Record<string, string>,
  retryAfterSec?: number,
): Response {
  const headers: Record<string, string> = {
    ...cors,
    "Content-Type": "application/json",
  };
  if (retryAfterSec) headers["Retry-After"] = String(retryAfterSec);
  return new Response(
    JSON.stringify({ error: "Too many requests. Please wait and try again." }),
    { status: 429, headers },
  );
}
