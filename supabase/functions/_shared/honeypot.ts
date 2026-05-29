/**
 * Honeypot bot trap for public form endpoints.
 *
 * The form renders a visually-hidden, tab-skipped, autocomplete-off field
 * that a human never sees and never fills. Automated form-stuffers, however,
 * tend to fill every input they find. So any request that arrives with a
 * non-empty value in the honeypot field was almost certainly submitted by a
 * bot, and the caller can drop it before spending money on Firecrawl, Claude,
 * Resend, or a database write.
 *
 * This is the lightweight bot check that replaces the currently-disabled
 * Turnstile widget (see _shared/turnstile.ts). It is intentionally silent:
 * callers should return a benign success-shaped response so the bot cannot
 * tell its submission was discarded and learn to evade the trap.
 *
 * Default field key is "company_url" — plausible enough that naive bots fill
 * it, while the markup keeps it off-screen so real users leave it blank.
 */
export const HONEYPOT_FIELD = "company_url";

/**
 * Returns true if the honeypot field carries a non-empty string value,
 * which indicates an automated submission. Missing field, non-string value,
 * or whitespace-only value all return false (treated as a legitimate human).
 */
export function isHoneypotTripped(
  body: unknown,
  field: string = HONEYPOT_FIELD,
): boolean {
  if (!body || typeof body !== "object") return false;
  const v = (body as Record<string, unknown>)[field];
  return typeof v === "string" && v.trim().length > 0;
}
