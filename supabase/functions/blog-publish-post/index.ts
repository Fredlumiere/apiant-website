/**
 * blog-publish-post
 *
 * Flip a post's status to 'publishing'. The database trigger
 * trigger_blog_publish_workflow() fires repository_dispatch to GitHub
 * Actions, which runs build_blog.py, regenerates the static HTML, commits,
 * and the deploy workflow ships it. build_blog.py calls blog-mark-live at
 * the end to flip the status to 'live' or 'failed'.
 *
 * As a belt-and-braces fallback, if the pg_net dispatch fails silently
 * (e.g. vault secret missing), this function also POSTs the dispatch
 * directly if GH_DISPATCH_PAT is set in the edge function env.
 *
 * Auth: required (editor for own posts, admin for any).
 *
 * POST { id: string }
 *
 * Returns { id, status: 'publishing' }.
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { resolveEditor, unauthorized } from "../_shared/blog_auth.ts";

const GITHUB_REPO = "Fredlumiere/apiant-website";

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const auth = await resolveEditor(req);
    if (!auth.ok) return unauthorized(cors, auth.status, auth.error);
    const { editor } = auth;

    const body = await req.json().catch(() => ({}));
    const id = typeof body.id === "string" ? body.id : "";
    if (!id) {
      return new Response(
        JSON.stringify({ error: "id required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const supabase = getServiceClient();
    const { data: existing, error: exErr } = await supabase
      .from("blog_posts")
      .select("id, slug, title, author_id, status")
      .eq("id", id)
      .single();
    if (exErr || !existing) {
      return new Response(
        JSON.stringify({ error: "Post not found" }),
        { status: 404, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    const isOwner = existing.author_id === editor.author.id;
    const isAdmin = editor.author.role === "admin";
    if (!isOwner && !isAdmin) return unauthorized(cors, 403, "Not your post");
    if (existing.status === "publishing") {
      return new Response(
        JSON.stringify({ id: existing.id, status: "publishing" }),
        { headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (!existing.title) {
      return new Response(
        JSON.stringify({ error: "Title required before publish" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    // Flip status. This fires trigger_blog_publish_workflow() inside Postgres
    // which posts to GitHub via pg_net. We also do a direct POST below as a
    // fallback so a missing/expired Vault secret doesn't silently break things.
    const { error: updErr } = await supabase
      .from("blog_posts")
      .update({ status: "publishing", publish_status_msg: null })
      .eq("id", id);
    if (updErr) {
      console.error("blog-publish-post update error:", updErr.code || updErr.message);
      return new Response(
        JSON.stringify({ error: "Failed to flip status" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const ghPat = Deno.env.get("GH_DISPATCH_PAT");
    if (ghPat) {
      try {
        const resp = await fetch(
          `https://api.github.com/repos/${GITHUB_REPO}/dispatches`,
          {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${ghPat}`,
              "Accept": "application/vnd.github+json",
              "Content-Type": "application/json",
              "User-Agent": "apiant-blog-publisher",
            },
            body: JSON.stringify({
              event_type: "blog_publish",
              client_payload: { post_id: id, slug: existing.slug },
            }),
          },
        );
        if (!resp.ok) {
          console.warn(
            "blog-publish-post fallback dispatch non-2xx:",
            resp.status,
            await resp.text().catch(() => ""),
          );
        }
      } catch (e) {
        console.warn("blog-publish-post fallback dispatch error:", (e as Error).message);
      }
    }

    return new Response(
      JSON.stringify({ id, status: "publishing" }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("blog-publish-post error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
