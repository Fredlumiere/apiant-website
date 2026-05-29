/**
 * Server-side relay to the legacy APIANT iPaaS lead webhook.
 *
 * Historically the browser POSTed the qualification popup straight to
 * apiant.com/webhook/<id> (CQ_FORM_DATA). That path bypassed all validation
 * and anti-bot checks. We now forward server-side from submit-lead AFTER the
 * payload has been validated, so the downstream automation (which feeds the
 * CRM) receives only clean, origin-checked data.
 *
 * The target URL is read from APIANT_LEAD_WEBHOOK_URL. If it is unset the relay
 * is a no-op (returns {skipped:true}) so the function is safe to deploy before
 * the secret is configured. Relay failures are reported but never thrown:
 * the lead is already persisted in lead_sessions, so a webhook hiccup must not
 * fail the user's submission.
 */

export interface RelayLead {
  company_type: string;
  company_type_label: string;
  domain: string;
  email: string;
  mobile: string;
  company_name: string;
  integration_needs: string;
  page_title: string;
}

/**
 * Build the form-urlencoded body for the downstream webhook using the SAME
 * field names the legacy browser payload used (CQ_FORM_DATA), so the existing
 * automation keeps working unchanged. Minimal surface: only the fields the
 * automation consumed — no turnstile token, honeypot, or internal fields.
 */
export function buildRelayParams(lead: RelayLead): URLSearchParams {
  return new URLSearchParams({
    PageTitle: lead.page_title || "",
    CompanyType: lead.company_type || "",
    CompanyTypeLabel: lead.company_type_label || "",
    CompanyDomain: lead.domain || "",
    WorkEmail: lead.email || "",
    Mobile: lead.mobile || "",
    Company: lead.company_name || "",
    IntegrationNeeds: lead.integration_needs || "",
  });
}

export interface RelayResult {
  ok: boolean;
  skipped?: boolean;
  status?: number;
  reason?: string;
}

export async function relayToWebhook(lead: RelayLead): Promise<RelayResult> {
  const url = Deno.env.get("APIANT_LEAD_WEBHOOK_URL");
  if (!url) return { ok: false, skipped: true, reason: "no_url_configured" };

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: buildRelayParams(lead).toString(),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    return { ok: res.ok, status: res.status };
  } catch (e) {
    clearTimeout(timeout);
    return { ok: false, reason: (e as Error).name === "AbortError" ? "timeout" : "fetch_error" };
  }
}
