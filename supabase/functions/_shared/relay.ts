/**
 * Server-side relays to the legacy APIANT iPaaS webhooks.
 *
 * Historically the browser POSTed forms straight to apiant.com/webhook/<id>,
 * bypassing all validation and anti-bot checks. We now forward server-side
 * AFTER the payload is validated, so the downstream automation (which feeds
 * the CRM) receives only clean, origin-checked data. Field names are preserved
 * exactly so the existing automations keep working unchanged.
 *
 * Two families, two destinations (distinct env vars):
 *   - main lead (+ call-now)  -> APIANT_LEAD_WEBHOOK_URL    (relayToWebhook)
 *   - Contact Us / apiapps     -> APIANT_APIAPPS_WEBHOOK_URL (relayContact)
 *
 * If the relevant URL is unset the relay is a no-op ({skipped:true}) so the
 * functions are safe to deploy before secrets are configured. Relay failures
 * are reported, never thrown.
 */

export interface RelayResult {
  ok: boolean;
  skipped?: boolean;
  status?: number;
  reason?: string;
}

async function postForm(url: string, params: URLSearchParams): Promise<RelayResult> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    return { ok: res.ok, status: res.status };
  } catch (e) {
    clearTimeout(timeout);
    return { ok: false, reason: (e as Error).name === "AbortError" ? "timeout" : "fetch_error" };
  }
}

/* ----------------------------- Main lead family ---------------------------- */

export interface RelayLead {
  company_type: string;
  company_type_label: string;
  domain: string;
  email: string;
  mobile: string;
  first_name: string;
  last_name: string;
  company_name: string;
  integration_needs: string;
  page_title: string;
  wants_call_now?: boolean;
}

/**
 * Build the form-urlencoded body using the SAME field names the legacy browser
 * payload used (CQ_FORM_DATA). Minimal surface: no turnstile/honeypot/internal
 * fields. WantsCallNow is included only for the call-now event.
 */
export function buildRelayParams(lead: RelayLead): URLSearchParams {
  const p = new URLSearchParams({
    PageTitle: lead.page_title || "",
    CompanyType: lead.company_type || "",
    CompanyTypeLabel: lead.company_type_label || "",
    CompanyDomain: lead.domain || "",
    WorkEmail: lead.email || "",
    Mobile: lead.mobile || "",
    FirstName: lead.first_name || "",
    LastName: lead.last_name || "",
    Company: lead.company_name || "",
    IntegrationNeeds: lead.integration_needs || "",
  });
  if (lead.wants_call_now) p.set("WantsCallNow", "yes");
  return p;
}

export async function relayToWebhook(lead: RelayLead): Promise<RelayResult> {
  const url = Deno.env.get("APIANT_LEAD_WEBHOOK_URL");
  if (!url) return { ok: false, skipped: true, reason: "no_url_configured" };
  return await postForm(url, buildRelayParams(lead));
}

/* --------------------------- Contact Us / apiapps -------------------------- */

export interface RelayContact {
  page_title: string;
  first_name: string;
  last_name: string;
  company: string;
  email: string;
  mobile: string;
  country: string;
  integration_needs: string;
}

/** Preserves the legacy Contact Us (#contact-us-form) field names exactly. */
export function buildContactParams(c: RelayContact): URLSearchParams {
  return new URLSearchParams({
    PageTitle: c.page_title || "",
    FirstName: c.first_name || "",
    LastName: c.last_name || "",
    Company: c.company || "",
    WorkEmail: c.email || "",
    Mobile: c.mobile || "",
    Country: c.country || "",
    IntegrationNeeds: c.integration_needs || "",
  });
}

export async function relayContact(c: RelayContact): Promise<RelayResult> {
  const url = Deno.env.get("APIANT_APIAPPS_WEBHOOK_URL");
  if (!url) return { ok: false, skipped: true, reason: "no_url_configured" };
  return await postForm(url, buildContactParams(c));
}
