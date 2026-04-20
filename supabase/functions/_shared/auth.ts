/**
 * Auth helpers: password hashing/verification and constant-time compares.
 *
 * We store admin passwords in admin_settings.admin_password_hash. Historically
 * those were raw SHA-256 hex (fast, GPU-friendly, unsalted). We now support
 * both bcrypt ($2a$... / $2b$...) and legacy SHA-256, and auto-upgrade to
 * bcrypt on the next successful login.
 */
import * as bcrypt from "https://deno.land/x/bcrypt@v0.4.1/mod.ts";

export async function hashPasswordBcrypt(password: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  return await bcrypt.hash(password, salt);
}

export function isBcryptHash(hash: string): boolean {
  return /^\$2[aby]?\$/.test(hash);
}

async function sha256Hex(input: string): Promise<string> {
  const buf = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(input),
  );
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

/**
 * Constant-time string comparison. Returns true only if both strings are the
 * same length and contain the same bytes.
 */
export function timingSafeEqual(a: string, b: string): boolean {
  const aBytes = new TextEncoder().encode(a);
  const bBytes = new TextEncoder().encode(b);
  if (aBytes.length !== bBytes.length) return false;
  let diff = 0;
  for (let i = 0; i < aBytes.length; i++) diff |= aBytes[i] ^ bBytes[i];
  return diff === 0;
}

/**
 * Verify a plaintext password against a stored hash. Supports bcrypt hashes
 * and legacy SHA-256 hex strings for backward compatibility.
 */
export async function verifyPassword(
  password: string,
  storedHash: string,
): Promise<boolean> {
  if (!storedHash) return false;
  if (isBcryptHash(storedHash)) {
    try {
      return await bcrypt.compare(password, storedHash);
    } catch {
      return false;
    }
  }
  // Legacy SHA-256 hex path
  const candidate = await sha256Hex(password);
  return timingSafeEqual(candidate, storedHash);
}
