/**
 * blog-get-post
 *
 * Returns one blog post by slug or id, with full body.
 *
 * Public callers: only live posts.
 * Authenticated editors: any status.
 *
 * POST { slug?: string, id?: string }
 *
 * Returns { post } with everything in blog-list-posts plus body_md, body_html,
 * subtitle, hero_image_alt, SEO fields, scheduled_for, publish_status_msg.
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { resolveEditor } from "../_shared/blog_auth.ts";

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const body = await req.json().catch(() => ({}));
    const slug = typeof body.slug === "string" ? body.slug.trim() : "";
    const id = typeof body.id === "string" ? body.id.trim() : "";

    if (!slug && !id) {
      return new Response(
        JSON.stringify({ error: "slug or id required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    // Optional auth: editors can see drafts; public can only see live posts.
    let isEditor = false;
    if ((req.headers.get("Authorization") || "").startsWith("Bearer ")) {
      const result = await resolveEditor(req);
      isEditor = result.ok;
    }

    const supabase = getServiceClient();
    let q = supabase
      .from("blog_posts")
      .select(`
        id, slug, title, subtitle, excerpt, body_md, body_html,
        hero_image_url, hero_image_alt,
        seo_title, seo_description, canonical_url, og_image_url,
        status, publish_status_msg, published_at, scheduled_for,
        created_at, updated_at,
        category:blog_categories(id, slug, name, description),
        author:blog_authors(id, slug, display_name, role_title, avatar_url, bio),
        tags:blog_post_tags(blog_tags(id, slug, name))
      `)
      .limit(1);

    if (slug) q = q.eq("slug", slug);
    if (id) q = q.eq("id", id);
    if (!isEditor) q = q.eq("status", "live");

    const { data, error } = await q;
    if (error) {
      console.error("blog-get-post error:", error.code || error.message);
      return new Response(
        JSON.stringify({ error: "Failed to load post" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (!data || data.length === 0) {
      return new Response(
        JSON.stringify({ error: "Not found" }),
        { status: 404, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const post: any = data[0];
    post.tags = (post.tags || []).map((t: any) => t.blog_tags).filter(Boolean);

    return new Response(
      JSON.stringify({ post }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("blog-get-post error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
