import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

const ALLOWED_SLUGS = ["apiant-ai-advantage", "market-opportunity"];

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
    const { username, password, page_slug } = await req.json();

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

    const validUser = Deno.env.get("PROTECTED_PAGE_USER");
    const validPass = Deno.env.get("PROTECTED_PAGE_PASS");

    if (username !== validUser || password !== validPass) {
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
