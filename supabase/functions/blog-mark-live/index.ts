/**
 * blog-mark-live
 *
 * Terminal status setter, called by scripts/build_blog.py at the end of the
 * GitHub Actions build job. Sets status to 'live' (success) or 'failed'
 * (with publish_status_msg).
 *
 * Auth: service-role only. We require the caller to pass the
 * SUPABASE_SERVICE_ROLE_KEY in the Authorization header. JWT verification is
 * skipped on Supabase Edge when verify_jwt = false (configured in
 * supabase/config.toml for this function).
 *
 * POST {
 *   id: string,
 *   status: "live" | "failed",
 *   msg?: string                 // failure reason, surfaced in admin UI
 * }
 *
 * Returns { ok: true }.
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
    const authHeader = req.headers.get("Authorization") || "";
    const provided = authHeader.startsWith("Bearer ")
      ? authHeader.slice("Bearer ".length).trim()
      : "";
    if (!serviceKey || provided !== serviceKey) {
      return new Response(
        JSON.stringify({ error: "service role required" }),
        { status: 401, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const body = await req.json().catch(() => ({}));
    const id = typeof body.id === "string" ? body.id : "";
    const status = body.status === "live" || body.status === "failed" ? body.status : "";
    const msg = typeof body.msg === "string" ? body.msg.slice(0, 1000) : null;
    if (!id || !status) {
      return new Response(
        JSON.stringify({ error: "id and status required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const supabase = getServiceClient();
    const patch: Record<string, unknown> = {
      status,
      publish_status_msg: msg,
    };
    if (status === "live") patch.published_at = new Date().toISOString();

    const { error } = await supabase
      .from("blog_posts")
      .update(patch)
      .eq("id", id);

    if (error) {
      console.error("blog-mark-live error:", error.code || error.message);
      return new Response(
        JSON.stringify({ error: "Failed to update status" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    return new Response(
      JSON.stringify({ ok: true }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("blog-mark-live error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
