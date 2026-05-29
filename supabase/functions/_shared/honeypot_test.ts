/**
 * Tests for the honeypot bot trap.
 *
 * Run with: deno test supabase/functions/_shared/honeypot_test.ts
 */
import { assertEquals } from "https://deno.land/std@0.168.0/testing/asserts.ts";
import { HONEYPOT_FIELD, isHoneypotTripped } from "./honeypot.ts";

Deno.test("clean human submission (field absent) is not tripped", () => {
  assertEquals(isHoneypotTripped({ email: "a@b.com" }), false);
});

Deno.test("empty honeypot value is not tripped", () => {
  assertEquals(isHoneypotTripped({ [HONEYPOT_FIELD]: "" }), false);
});

Deno.test("whitespace-only honeypot value is not tripped", () => {
  assertEquals(isHoneypotTripped({ [HONEYPOT_FIELD]: "   " }), false);
});

Deno.test("non-empty honeypot value is tripped (bot)", () => {
  assertEquals(isHoneypotTripped({ [HONEYPOT_FIELD]: "http://spam.example" }), true);
});

Deno.test("non-string honeypot value is not tripped", () => {
  assertEquals(isHoneypotTripped({ [HONEYPOT_FIELD]: 123 }), false);
});

Deno.test("null / non-object body is not tripped", () => {
  assertEquals(isHoneypotTripped(null), false);
  assertEquals(isHoneypotTripped(undefined), false);
  assertEquals(isHoneypotTripped("string-body"), false);
});

Deno.test("custom field name is honored", () => {
  assertEquals(isHoneypotTripped({ trap: "x" }, "trap"), true);
  assertEquals(isHoneypotTripped({ trap: "" }, "trap"), false);
});
