/**
 * Pure, dependency-free validation helpers for lead submissions.
 *
 * Kept separate from the edge-function handler so the rules can be unit-tested
 * without spinning up an HTTP server or hitting Supabase. See leadvalidate_test.ts.
 */

export const ALLOWED_COMPANY_TYPES = new Set([
  "saas",
  "si",
  "enterprise",
  "fitness",
  "healthcare",
  "nonprofit",
  "other",
]);

// Deliberately simple: structural check only, not RFC-complete.
export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/** Apex domains whose pages are allowed to originate a lead. */
const ALLOWED_LEAD_HOSTS = ["apiant.com", "apiant-website.vercel.app"];

export function normalizeEmail(v: unknown): string {
  return typeof v === "string" ? v.slice(0, 254).trim().toLowerCase() : "";
}

export function isValidEmail(email: string): boolean {
  return !!email && EMAIL_RE.test(email);
}

export function normalizeCompanyType(v: unknown): string {
  return typeof v === "string" ? v.slice(0, 32).trim().toLowerCase() : "";
}

export function isAllowedCompanyType(t: string): boolean {
  return ALLOWED_COMPANY_TYPES.has(t);
}

/**
 * Returns the host of a URL if it parses and belongs to an allowed APIANT
 * property (or any subdomain of one). Returns null otherwise.
 * localhost is allowed only when isDev is true.
 */
export function allowedUrlHost(
  raw: unknown,
  isDev = false,
): string | null {
  if (typeof raw !== "string" || !raw) return null;
  let u: URL;
  try {
    u = new URL(raw);
  } catch {
    return null;
  }
  if (u.protocol !== "https:" && u.protocol !== "http:") return null;
  const host = u.hostname.toLowerCase();
  if (isDev && (host === "localhost" || host === "127.0.0.1")) return host;
  for (const h of ALLOWED_LEAD_HOSTS) {
    if (host === h || host.endsWith("." + h)) return host;
  }
  return null;
}

/**
 * Parse a comma-separated blocklist (e.g. the BLOCKED_EMAILS secret) into a
 * set of normalized emails. Unknown/empty input yields an empty set.
 */
export function parseEmailBlocklist(raw: unknown): Set<string> {
  if (typeof raw !== "string" || !raw) return new Set();
  return new Set(
    raw.split(",").map((s) => s.trim().toLowerCase()).filter(Boolean),
  );
}

export interface SourceContext {
  /** Authoritative URL observed server-side from the Referer header. */
  refererUrl: string | null;
  /** Client-supplied URL (window.location.href), secondary / advisory. */
  clientUrl: string | null;
  /** Whether the request looked like it came from a real browser context. */
  hasBrowserContext: boolean;
}

/**
 * Resolve where a submission came from using server-observed headers first,
 * falling back to the client-supplied source_url. originAllowed should be the
 * result of cors.isOriginAllowed(req).
 */
export function resolveSource(
  headers: { origin: string | null; referer: string | null },
  clientSourceUrl: unknown,
  originAllowed: boolean,
  isDev = false,
): SourceContext {
  const refererHost = allowedUrlHost(headers.referer, isDev);
  const clientHost = allowedUrlHost(clientSourceUrl, isDev);
  return {
    refererUrl: refererHost ? (headers.referer as string) : null,
    clientUrl: clientHost ? (clientSourceUrl as string) : null,
    // A genuine browser submission carries an allowed Origin and/or a Referer
    // from one of our pages. Direct scripted calls usually have neither.
    hasBrowserContext: originAllowed || !!refererHost,
  };
}
