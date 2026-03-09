/**
 * verify-company-type
 *
 * Scrapes a company's website via Firecrawl and uses AI to verify
 * whether the company matches the claimed type (SaaS, SI, Enterprise).
 *
 * POST { domain: string, claimed_type: "saas" | "si" | "enterprise" }
 * Returns { verified: boolean, confidence: string, reason: string }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";

const FIRECRAWL_API_KEY = Deno.env.get("FIRECRAWL_API_KEY");
const OPENAI_API_KEY = Deno.env.get("OPENAI_API_KEY");  // or use Anthropic/Gemini

const TYPE_LABELS: Record<string, string> = {
  saas: "SaaS Company (a company that sells software as a service)",
  si: "System Integrator (a company that builds integrations or IT solutions for clients)",
  enterprise: "Enterprise (a large organization that needs internal system integration)",
};

async function scrapeHomepage(domain: string): Promise<string> {
  if (!FIRECRAWL_API_KEY) {
    throw new Error("FIRECRAWL_API_KEY not configured");
  }

  const url = domain.startsWith("http") ? domain : `https://${domain}`;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);

  try {
    const res = await fetch("https://api.firecrawl.dev/v1/scrape", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${FIRECRAWL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url,
        formats: ["markdown"],
        onlyMainContent: true,
      }),
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (!res.ok) {
      const errText = await res.text().catch(() => "");
      console.error(`Firecrawl error: ${res.status} ${errText}`);
      if (res.status === 422) throw new Error("Could not access this website. Check the URL and try again.");
      if (res.status === 429) throw new Error("Rate limited. Please wait a moment and try again.");
      throw new Error(`Could not scrape website (HTTP ${res.status})`);
    }

    const data = await res.json();
    const markdown = data?.data?.markdown || data?.markdown || "";
    if (!markdown) throw new Error("No content found on this website.");
    return markdown.substring(0, 6000);
  } catch (e) {
    clearTimeout(timeout);
    if (e instanceof DOMException && e.name === "AbortError") {
      throw new Error("Website took too long to respond. Try again.");
    }
    throw e;
  }
}

async function classifyCompany(
  content: string,
  domain: string,
  claimedType: string
): Promise<{ verified: boolean; confidence: string; reason: string }> {
  const typeLabel = TYPE_LABELS[claimedType] || claimedType;

  const prompt = `You are a company classifier for APIANT, an integration platform. Analyze this website content and determine if the company matches the claimed type.

CLAIMED TYPE: ${typeLabel}
DOMAIN: ${domain}

WEBSITE CONTENT:
${content}

CLASSIFICATION RULES:
- SaaS Company: Sells software/platform as a service. Has product pages, pricing, sign-up flows. Their customers use their software.
- System Integrator: Provides IT consulting, custom development, or integration services to other businesses. May be a consulting firm, agency, or managed services provider.
- Enterprise: A large organization (not primarily a software or consulting company) that would need integrations for internal operations. Could be healthcare, manufacturing, retail, finance, etc.

IMPORTANT: Be reasonably generous. If the website plausibly fits the claimed type, verify it. Only reject if the website clearly contradicts the claim (e.g., a personal blog claiming to be an Enterprise, or a restaurant claiming to be a SaaS company).

Respond with ONLY a JSON object:
{
  "verified": true or false,
  "confidence": "high", "medium", or "low",
  "reason": "One sentence explaining why"
}`;

  // Use Anthropic Claude API for classification
  const ANTHROPIC_API_KEY = Deno.env.get("ANTHROPIC_API_KEY");

  if (ANTHROPIC_API_KEY) {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 256,
        messages: [{ role: "user", content: prompt }],
      }),
    });

    if (!res.ok) {
      console.error("Anthropic API error:", res.status, await res.text().catch(() => ""));
      throw new Error("AI classification temporarily unavailable");
    }

    const data = await res.json();
    const text = data?.content?.[0]?.text || "";
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error("Could not parse AI response");
    return JSON.parse(jsonMatch[0]);
  }

  // Fallback: if no AI key, accept all (log warning)
  console.warn("No AI API key configured. Auto-verifying.");
  return { verified: true, confidence: "low", reason: "Auto-verified (no AI key configured)" };
}

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { domain, claimed_type } = await req.json();

    if (!domain || typeof domain !== "string") {
      return new Response(
        JSON.stringify({ error: "domain is required" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (!["saas", "si", "enterprise"].includes(claimed_type)) {
      return new Response(
        JSON.stringify({ error: "claimed_type must be saas, si, or enterprise" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Clean domain
    const cleanDomain = domain
      .replace(/^https?:\/\//, "")
      .replace(/\/.*$/, "")
      .replace(/^www\./, "")
      .toLowerCase()
      .trim();

    if (!cleanDomain || !cleanDomain.includes(".")) {
      return new Response(
        JSON.stringify({ error: "Please enter a valid domain (e.g., acme.com)" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log(`[verify] Checking ${cleanDomain} as ${claimed_type}`);

    const content = await scrapeHomepage(cleanDomain);
    const result = await classifyCompany(content, cleanDomain, claimed_type);

    console.log(`[verify] ${cleanDomain}: verified=${result.verified}, confidence=${result.confidence}`);

    return new Response(
      JSON.stringify(result),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("verify-company-type error:", e);
    const message = e instanceof Error ? e.message : "Verification failed";
    return new Response(
      JSON.stringify({ error: message }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
