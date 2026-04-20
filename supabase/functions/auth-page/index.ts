import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { timingSafeEqual } from "../_shared/auth.ts";
import { verifyTurnstile } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

const ALLOWED_SLUGS = ["apiant-ai-advantage", "market-opportunity", "activecampaign-pricing"];

function slugEnvKey(slug: string): string {
  return slug.replace(/[^a-zA-Z0-9]/g, "_").toUpperCase();
}

Deno.serve(async (req: Request) => {
  const cors = getCorsHeaders(req);

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  try {
    const body = await req.json();
    const { username, password, page_slug, turnstile_token } = body;

    if (!username || !password || !page_slug) {
      return new Response(JSON.stringify({ error: "Missing fields" }), {
        status: 400,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    }

    if (!ALLOWED_SLUGS.includes(page_slug)) {
      return new Response(JSON.stringify({ error: "Invalid page" }), {
        status: 400,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    }

    // Require Turnstile to make brute force cost real work per attempt.
    const turnstile = await verifyTurnstile(turnstile_token, req);
    if (!turnstile.ok) {
      return new Response(JSON.stringify({ error: "Verification failed. Please retry." }), {
        status: 403,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    }

    // Per-IP rate limit: 10 attempts per 10 min across all protected pages.
    const rl = await checkRateLimit(req, { bucket: "auth-page", max: 10, windowSeconds: 600 });
    if (!rl.ok) return rateLimitResponse(cors, rl.retryAfterSec);

    // Per-slug credentials preferred, generic fallback for legacy pages.
    const slugKey = slugEnvKey(page_slug);
    const validUser =
      Deno.env.get(`PROTECTED_PAGE_USER_${slugKey}`) ||
      Deno.env.get("PROTECTED_PAGE_USER") || "";
    const validPass =
      Deno.env.get(`PROTECTED_PAGE_PASS_${slugKey}`) ||
      Deno.env.get("PROTECTED_PAGE_PASS") || "";

    // Constant-time compare on both fields. Note: this also still leaks
    // existence of the username through whether the comparison uses the empty
    // fallback. Since there's only one expected user, that's acceptable here.
    const userOk = timingSafeEqual(String(username), validUser);
    const passOk = timingSafeEqual(String(password), validPass);

    if (!userOk || !passOk || !validUser || !validPass) {
      return new Response(JSON.stringify({ error: "Invalid credentials" }), {
        status: 401,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    }

    const supabase = getServiceClient();
    const { data, error } = await supabase.storage
      .from("protected-pages")
      .download(`${page_slug}.html`);

    if (error || !data) {
      return new Response(JSON.stringify({ error: "Content not found" }), {
        status: 404,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    }

    const html = await data.text();

    return new Response(JSON.stringify({ html }), {
      status: 200,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  } catch {
    return new Response(JSON.stringify({ error: "Server error" }), {
      status: 500,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }
});
