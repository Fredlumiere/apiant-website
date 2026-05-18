/**
 * blog-list-posts
 *
 * GET-style POST endpoint. Lists blog posts.
 *
 * Public callers (no auth): only live posts are returned.
 * Authenticated editors: all posts, optionally filtered by status.
 *
 * POST {
 *   status?:   "draft" | "saved" | "publishing" | "live" | "failed" | "all",
 *   category?: string (slug),
 *   limit?:    number (default 50, max 200),
 *   offset?:   number (default 0)
 * }
 *
 * Returns { posts: [...] } with: id, slug, title, excerpt, hero_image_url,
 * status, published_at, updated_at, category {slug,name}, author {slug,display_name},
 * tags [{slug,name}].
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { resolveEditor } from "../_shared/blog_auth.ts";

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const body = req.method === "POST" ? await req.json().catch(() => ({})) : {};
    const limit = Math.min(Math.max(Number(body.limit) || 50, 1), 200);
    const offset = Math.max(Number(body.offset) || 0, 0);
    const status = typeof body.status === "string" ? body.status : "live";
    const categorySlug = typeof body.category === "string" ? body.category : "";

    // Auth is optional. Editors can request any status; public can only get live.
    const authHeader = req.headers.get("Authorization") || "";
    let isEditor = false;
    if (authHeader.startsWith("Bearer ")) {
      const result = await resolveEditor(req);
      isEditor = result.ok;
    }

    const supabase = getServiceClient();
    let q = supabase
      .from("blog_posts")
      .select(`
        id, slug, title, excerpt, hero_image_url, status,
        published_at, updated_at,
        category:blog_categories(slug, name),
        author:blog_authors(slug, display_name),
        tags:blog_post_tags(blog_tags(slug, name))
      `)
      .order("published_at", { ascending: false, nullsFirst: false })
      .order("updated_at", { ascending: false })
      .range(offset, offset + limit - 1);

    if (!isEditor) {
      q = q.eq("status", "live");
    } else if (status !== "all") {
      q = q.eq("status", status);
    }

    if (categorySlug) {
      const { data: cat } = await supabase
        .from("blog_categories")
        .select("id")
        .eq("slug", categorySlug)
        .single();
      if (cat) q = q.eq("category_id", cat.id);
    }

    const { data, error } = await q;
    if (error) {
      console.error("blog-list-posts error:", error.code || error.message);
      return new Response(
        JSON.stringify({ error: "Failed to list posts" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    // Flatten tag rows from the nested join shape.
    const posts = (data || []).map((p: any) => ({
      ...p,
      tags: (p.tags || []).map((t: any) => t.blog_tags).filter(Boolean),
    }));

    return new Response(
      JSON.stringify({ posts }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("blog-list-posts error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
