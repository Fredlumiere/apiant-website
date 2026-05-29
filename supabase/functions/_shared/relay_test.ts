/**
 * Tests for the webhook relay payload builder.
 * Run with: deno test supabase/functions/_shared/relay_test.ts
 */
import { assertEquals } from "https://deno.land/std@0.168.0/testing/asserts.ts";
import { buildContactParams, buildRelayParams } from "./relay.ts";

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

/* ---- apiapps (Contact Us) builder + routing selection ---- */

const contact = {
  page_title: "Mindbody + HubSpot | APIANT",
  first_name: "Jane",
  last_name: "Doe",
  company: "FitStudio",
  email: "jane@fitstudio.com",
  mobile: "+14155550199",
  country: "United States",
  integration_needs: "Sync clients to HubSpot",
};

Deno.test("apiapps relay maps Contact Us fields with legacy names", () => {
  const p = buildContactParams(contact);
  assertEquals(p.get("FirstName"), "Jane");
  assertEquals(p.get("LastName"), "Doe");
  assertEquals(p.get("WorkEmail"), "jane@fitstudio.com");
  assertEquals(p.get("Mobile"), "+14155550199");
  assertEquals(p.get("Country"), "United States");
  assertEquals(p.get("Company"), "FitStudio");
  assertEquals(p.get("IntegrationNeeds"), "Sync clients to HubSpot");
  assertEquals(p.get("PageTitle"), "Mindbody + HubSpot | APIANT");
});

Deno.test("apiapps: empty Mobile/Country become empty string, never null/undefined", () => {
  const p = buildContactParams({ ...contact, mobile: "", country: "" });
  assertEquals(p.get("Mobile"), "");
  assertEquals(p.get("Country"), "");
});

Deno.test("call-now flag is included only when set (lead family)", () => {
  assertEquals(buildRelayParams({ ...lead, wants_call_now: true }).get("WantsCallNow"), "yes");
  assertEquals(buildRelayParams(lead).has("WantsCallNow"), false);
});

Deno.test("routing selection: families produce distinct field sets", () => {
  const leadKeys = [...buildRelayParams(lead).keys()].sort().join(",");
  const apiappsKeys = [...buildContactParams(contact).keys()].sort().join(",");
  // lead family carries CompanyType/CompanyDomain; apiapps carries FirstName/LastName/Country
  assertEquals(leadKeys.includes("CompanyType"), true);
  assertEquals(leadKeys.includes("FirstName"), false);
  assertEquals(apiappsKeys.includes("FirstName"), true);
  assertEquals(apiappsKeys.includes("CompanyType"), false);
});
