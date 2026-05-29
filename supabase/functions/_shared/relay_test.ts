/**
 * Tests for the webhook relay payload builder.
 * Run with: deno test supabase/functions/_shared/relay_test.ts
 */
import { assertEquals } from "https://deno.land/std@0.168.0/testing/asserts.ts";
import { buildRelayParams } from "./relay.ts";

const lead = {
  company_type: "saas",
  company_type_label: "SaaS Company",
  domain: "acme.com",
  email: "a@acme.com",
  mobile: "+14155550123",
  company_name: "Acme",
  integration_needs: "Sync HubSpot to our app",
  page_title: "APIANT | Start Building",
};

Deno.test("relay maps validated lead to legacy CQ_FORM_DATA field names", () => {
  const p = buildRelayParams(lead);
  assertEquals(p.get("CompanyType"), "saas");
  assertEquals(p.get("CompanyTypeLabel"), "SaaS Company");
  assertEquals(p.get("CompanyDomain"), "acme.com");
  assertEquals(p.get("WorkEmail"), "a@acme.com");
  assertEquals(p.get("Mobile"), "+14155550123");
  assertEquals(p.get("Company"), "Acme");
  assertEquals(p.get("IntegrationNeeds"), "Sync HubSpot to our app");
  assertEquals(p.get("PageTitle"), "APIANT | Start Building");
});

Deno.test("relay preserves a non-empty Mobile value", () => {
  const p = buildRelayParams({ ...lead, mobile: "+447911123456" });
  assertEquals(p.get("Mobile"), "+447911123456");
});

Deno.test("missing/empty Mobile becomes empty string, never 'null'/'undefined'", () => {
  // Regression guard: the AI-page bug sent no mobile, and a naive `|| null`
  // would serialize to the literal string "null" in the urlencoded body.
  const empty = buildRelayParams({ ...lead, mobile: "" });
  assertEquals(empty.get("Mobile"), "");
  // deno-lint-ignore no-explicit-any
  const missing = buildRelayParams({ ...lead, mobile: undefined as any });
  assertEquals(missing.get("Mobile"), "");
  assertEquals(missing.get("Mobile") === "null" || missing.get("Mobile") === "undefined", false);
});

Deno.test("relay surface is minimal: no internal fields leak", () => {
  const p = buildRelayParams(lead);
  assertEquals(p.has("turnstile_token"), false);
  assertEquals(p.has("company_url"), false);
  assertEquals(p.has("form_id"), false);
  assertEquals(p.has("source_url"), false);
  // Exactly the 8 expected keys.
  assertEquals([...p.keys()].sort().join(","),
    "Company,CompanyDomain,CompanyType,CompanyTypeLabel,IntegrationNeeds,Mobile,PageTitle,WorkEmail");
});
