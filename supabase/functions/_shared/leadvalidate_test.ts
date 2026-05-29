/**
 * Tests for lead validation helpers.
 * Run with: deno test supabase/functions/_shared/leadvalidate_test.ts
 */
import { assertEquals } from "https://deno.land/std@0.168.0/testing/asserts.ts";
import {
  allowedUrlHost,
  isAllowedCompanyType,
  isValidEmail,
  normalizeCompanyType,
  normalizeEmail,
  resolveSource,
} from "./leadvalidate.ts";

Deno.test("email: valid and normalized", () => {
  assertEquals(normalizeEmail("  Fred@APIANT.com "), "fred@apiant.com");
  assertEquals(isValidEmail(normalizeEmail("a@b.co")), true);
  assertEquals(isValidEmail(normalizeEmail("not-an-email")), false);
  assertEquals(isValidEmail(normalizeEmail(123)), false);
});

Deno.test("company_type: allowlist enforced", () => {
  assertEquals(isAllowedCompanyType(normalizeCompanyType("SaaS")), true);
  assertEquals(isAllowedCompanyType(normalizeCompanyType("enterprise")), true);
  assertEquals(isAllowedCompanyType(normalizeCompanyType("hacker")), false);
  assertEquals(isAllowedCompanyType(normalizeCompanyType("")), false);
});

Deno.test("allowedUrlHost: only APIANT hosts, https/http only", () => {
  assertEquals(allowedUrlHost("https://apiant.com/for-saas"), "apiant.com");
  assertEquals(allowedUrlHost("https://www.apiant.com/ai"), "www.apiant.com");
  assertEquals(allowedUrlHost("https://x.apiant-website.vercel.app/"), "x.apiant-website.vercel.app");
  assertEquals(allowedUrlHost("https://evil.com/apiant.com"), null);
  assertEquals(allowedUrlHost("javascript:alert(1)"), null);
  assertEquals(allowedUrlHost("http://localhost:3000/", false), null);
  assertEquals(allowedUrlHost("http://localhost:3000/", true), "localhost");
});

Deno.test("resolveSource: browser context from allowed origin", () => {
  const s = resolveSource(
    { origin: "https://apiant.com", referer: null },
    null,
    true,
  );
  assertEquals(s.hasBrowserContext, true);
});

Deno.test("resolveSource: browser context from referer when origin missing", () => {
  const s = resolveSource(
    { origin: null, referer: "https://apiant.com/for-si" },
    null,
    false,
  );
  assertEquals(s.hasBrowserContext, true);
  assertEquals(s.refererUrl, "https://apiant.com/for-si");
});

Deno.test("resolveSource: scripted call (no origin, no referer) has no browser context", () => {
  const s = resolveSource({ origin: null, referer: null }, null, false);
  assertEquals(s.hasBrowserContext, false);
  assertEquals(s.refererUrl, null);
});

Deno.test("resolveSource: forged foreign referer is not accepted", () => {
  const s = resolveSource(
    { origin: null, referer: "https://evil.com/x" },
    "https://evil.com/x",
    false,
  );
  assertEquals(s.hasBrowserContext, false);
  assertEquals(s.clientUrl, null);
});
