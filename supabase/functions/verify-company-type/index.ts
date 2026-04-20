/**
 * verify-company-type
 *
 * Scrapes a company's website via Firecrawl and uses AI to analyze
 * what the company does and whether it matches the claimed type.
 *
 * POST { domain: string, claimed_type: "saas" | "si" | "enterprise" }
 * Returns {
 *   description: string,        // 1-2 sentence description of the company
 *   detected_type: string,      // saas, si, enterprise, fitness, healthcare, nonprofit, other
 *   verified: boolean,          // true if detected_type matches claimed_type
 *   confidence: string,         // high, medium, low
 *   reason: string,             // explanation
 *   suggested_vertical: string  // mindbody, cliniko, donorperfect, or "" if none
 * }
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { verifyTurnstile } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

const FIRECRAWL_API_KEY = Deno.env.get("FIRECRAWL_API_KEY");

/** Hostnames that must never be scraped via our paid backend. */
const BLOCKED_HOSTS = [
  "localhost", "127.0.0.1", "0.0.0.0",
  "apiant.com", "www.apiant.com",
  "supabase.co", "supabase.net",
];
const BLOCKED_TLDS = [".local", ".internal", ".lan", ".test"];
const IPV4_RE = /^\d{1,3}(\.\d{1,3}){3}$/;

function isDisallowedHost(host: string): boolean {
  if (!host) return true;
  if (IPV4_RE.test(host)) return true;
  if (BLOCKED_HOSTS.includes(host)) return true;
  for (const tld of BLOCKED_TLDS) if (host.endsWith(tld)) return true;
  for (const blocked of BLOCKED_HOSTS) if (host.endsWith("." + blocked)) return true;
  return false;
}

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

interface ClassificationResult {
  description: string;
  company_name: string;
  detected_type: string;
  verified: boolean;
  confidence: string;
  reason: string;
  suggested_vertical: string;
}

async function classifyCompany(
  content: string,
  domain: string,
  claimedType: string
): Promise<ClassificationResult> {
  const typeLabel = TYPE_LABELS[claimedType] || claimedType;

  const prompt = `You are a company classifier for APIANT, an integration platform. Analyze this website content and determine what the company does and whether it matches the claimed type.

CLAIMED TYPE: ${typeLabel}
DOMAIN: ${domain}

WEBSITE CONTENT:
${content}

INSTRUCTIONS:
1. Extract the company's official name as it appears on their website (e.g., "Acme Corp", "FitLife Studio"). Use the name from the site, not the domain.
2. Write a 1-2 sentence description of what this company actually does. Be specific and concise.
3. Determine the company's actual type from these categories:
   - "saas": Sells software/platform as a service. Has product pages, pricing, sign-up flows.
   - "si": System Integrator. Provides IT consulting, custom development, or integration services.
   - "enterprise": Large organization needing internal integrations. Could be healthcare org, manufacturer, retailer, financial institution, etc.
   - "fitness": Gym, fitness studio, wellness center, yoga studio, personal training, strength training, martial arts, pilates, etc.
   - "healthcare": Medical clinic, physiotherapy, chiropractic, allied health practice, dental, optometry, etc.
   - "nonprofit": Nonprofit, charity, foundation, NGO, fundraising organization, church, school, etc.
   - "other": None of the above (restaurant, retail shop, personal blog, freelancer, etc.)
4. Check if the detected type matches the claimed type.
5. If the detected type is "fitness", set suggested_vertical to "mindbody".
   If "healthcare", set suggested_vertical to "cliniko".
   If "nonprofit", set suggested_vertical to "donorperfect".
   Otherwise set suggested_vertical to "".

Be accurate. A strength training studio is "fitness", not "saas". A physiotherapy clinic is "healthcare", not "enterprise". A charity is "nonprofit", not "enterprise".

Respond with ONLY a JSON object:
{
  "company_name": "The company's official name",
  "description": "One to two sentences describing what this company does",
  "detected_type": "saas|si|enterprise|fitness|healthcare|nonprofit|other",
  "verified": true or false,
  "confidence": "high|medium|low",
  "reason": "One sentence explaining why",
  "suggested_vertical": "mindbody|cliniko|donorperfect|"
}`;

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
        max_tokens: 512,
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

  // Fallback: if no AI key, return basic result
  console.warn("No AI API key configured. Returning unverified result.");
  return {
    description: "We could not analyze this website (AI classification not configured).",
    detected_type: "other",
    verified: false,
    confidence: "low",
    reason: "AI classification not available",
    suggested_vertical: "",
  };
}

serve(async (req) => {
  const corsHeaders = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const body = await req.json();
    const { domain, claimed_type, turnstile_token } = body;

    const turnstile = await verifyTurnstile(turnstile_token, req);
    if (!turnstile.ok) {
      return new Response(
        JSON.stringify({ error: "Verification failed. Please retry." }),
        { status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const rl = await checkRateLimit(req, { bucket: "verify-company-type", max: 5, windowSeconds: 600 });
    if (!rl.ok) return rateLimitResponse(corsHeaders, rl.retryAfterSec);

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
      .slice(0, 253)
      .replace(/^https?:\/\//, "")
      .replace(/\/.*$/, "")
      .replace(/[?#].*$/, "")
      .replace(/:\d+$/, "")
      .replace(/^www\./, "")
      .toLowerCase()
      .trim();

    if (!cleanDomain || !cleanDomain.includes(".") || cleanDomain.length > 253) {
      return new Response(
        JSON.stringify({ error: "Please enter a valid domain (e.g., acme.com)" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (isDisallowedHost(cleanDomain)) {
      return new Response(
        JSON.stringify({ error: "That domain cannot be verified here." }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log(`[verify] Checking ${cleanDomain} as ${claimed_type}`);

    const content = await scrapeHomepage(cleanDomain);
    const result = await classifyCompany(content, cleanDomain, claimed_type);

    console.log(`[verify] ${cleanDomain}: detected=${result.detected_type}, verified=${result.verified}, confidence=${result.confidence}`);

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
