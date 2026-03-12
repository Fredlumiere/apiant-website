import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

serve(async (req: Request) => {
  const cors = getCorsHeaders(req);

  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: cors });
  }

  try {
    const { integration_need, source_page, domain, company_type } =
      await req.json();

    if (!integration_need || integration_need.trim().length === 0) {
      return new Response(
        JSON.stringify({ error: "integration_need is required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const sb = getServiceClient();
    const { error } = await sb.from("forum_requests").insert({
      integration_need: integration_need.trim(),
      source_page: source_page || null,
      domain: domain || null,
      company_type: company_type || null,
    });

    if (error) throw error;

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...cors, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: (err as Error).message }), {
      status: 500,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }
});
