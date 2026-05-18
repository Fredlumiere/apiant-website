/**
 * blog-save-post
 *
 * Upsert a draft. Always sets status to 'saved' (the publish-flip is a
 * separate explicit action via blog-publish-post). Writes a row to
 * blog_post_revisions and prunes to the most recent 50.
 *
 * Auth: required (editor or admin).
 *
 * POST {
 *   id?: string,                 // present = update; absent = insert
 *   slug: string,                // required, kebab-case, [a-z0-9-]+
 *   title: string,               // required
 *   subtitle?: string,
 *   excerpt?: string,
 *   body_md: string,
 *   hero_image_url?: string,
 *   hero_image_alt?: string,
 *   category_id?: string,
 *   tag_ids?: string[],          // replaces existing tags on the post
 *   seo_title?, seo_description?, canonical_url?, og_image_url?,
 *   scheduled_for?: string (ISO),
 * }
 *
 * Returns { id, slug, status, updated_at }.
 *
 * Authorization rules:
 * - Editors can update only their own posts; admins can update any.
 * - New posts always get author_id = caller (RLS-enforced too).
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { resolveEditor, unauthorized } from "../_shared/blog_auth.ts";

const SLUG_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function s(v: unknown, max: number): string {
  return typeof v === "string" ? v.slice(0, max) : "";
}

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const auth = await resolveEditor(req);
    if (!auth.ok) return unauthorized(cors, auth.status, auth.error);
    const { editor } = auth;

    const body = await req.json().catch(() => ({}));
    const id = typeof body.id === "string" ? body.id : null;
    const slug = s(body.slug, 200).trim().toLowerCase();
    const title = s(body.title, 300).trim();
    const body_md = typeof body.body_md === "string" ? body.body_md : "";

    if (!slug || !SLUG_RE.test(slug)) {
      return new Response(
        JSON.stringify({ error: "slug must be kebab-case [a-z0-9-]" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (!title) {
      return new Response(
        JSON.stringify({ error: "title required" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }
    if (body_md.length > 200_000) {
      return new Response(
        JSON.stringify({ error: "body_md too large (200KB max)" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const supabase = getServiceClient();

    // Build the upsert payload. body_html stays null; build_blog.py owns rendering.
    const payload: Record<string, unknown> = {
      slug,
      title,
      subtitle: s(body.subtitle, 300),
      excerpt: s(body.excerpt, 600),
      body_md,
      hero_image_url: s(body.hero_image_url, 500),
      hero_image_alt: s(body.hero_image_alt, 300),
      category_id: typeof body.category_id === "string" ? body.category_id : null,
      seo_title: s(body.seo_title, 300),
      seo_description: s(body.seo_description, 600),
      canonical_url: s(body.canonical_url, 500),
      og_image_url: s(body.og_image_url, 500),
      scheduled_for: typeof body.scheduled_for === "string" ? body.scheduled_for : null,
      status: "saved",
      publish_status_msg: null,
    };

    let postId: string;
    let updatedAt: string;
    let savedStatus: string;

    if (id) {
      // Update existing — authorship check.
      const { data: existing, error: exErr } = await supabase
        .from("blog_posts")
        .select("id, author_id, status")
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
      if (!isOwner && !isAdmin) {
        return unauthorized(cors, 403, "Not your post");
      }
      // Don't reset status if a publish is in flight.
      if (existing.status === "publishing") {
        return new Response(
          JSON.stringify({ error: "Publish in progress; wait for it to finish" }),
          { status: 409, headers: { ...cors, "Content-Type": "application/json" } },
        );
      }
      const { data: upd, error: updErr } = await supabase
        .from("blog_posts")
        .update(payload)
        .eq("id", id)
        .select("id, slug, status, updated_at")
        .single();
      if (updErr || !upd) {
        console.error("blog-save-post update error:", updErr?.code || updErr?.message);
        return new Response(
          JSON.stringify({ error: "Failed to save post" }),
          { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
        );
      }
      postId = upd.id;
      updatedAt = upd.updated_at;
      savedStatus = upd.status;
    } else {
      // Insert new.
      payload.author_id = editor.author.id;
      const { data: ins, error: insErr } = await supabase
        .from("blog_posts")
        .insert(payload)
        .select("id, slug, status, updated_at")
        .single();
      if (insErr || !ins) {
        const msg = insErr?.code === "23505" ? "Slug already in use" : "Failed to create post";
        console.error("blog-save-post insert error:", insErr?.code || insErr?.message);
        return new Response(
          JSON.stringify({ error: msg }),
          { status: insErr?.code === "23505" ? 409 : 500, headers: { ...cors, "Content-Type": "application/json" } },
        );
      }
      postId = ins.id;
      updatedAt = ins.updated_at;
      savedStatus = ins.status;
    }

    // Replace tag set if provided.
    if (Array.isArray(body.tag_ids)) {
      const tagIds = body.tag_ids
        .filter((t: unknown): t is string => typeof t === "string")
        .slice(0, 20);
      await supabase.from("blog_post_tags").delete().eq("post_id", postId);
      if (tagIds.length > 0) {
        const rows = tagIds.map((tid) => ({ post_id: postId, tag_id: tid }));
        await supabase.from("blog_post_tags").insert(rows);
      }
    }

    // Snapshot revision and prune.
    await supabase.from("blog_post_revisions").insert({
      post_id: postId,
      author_id: editor.author.id,
      title,
      body_md,
    });
    await supabase.rpc("prune_blog_revisions", { p_post_id: postId, p_keep: 50 });

    return new Response(
      JSON.stringify({ id: postId, slug, status: savedStatus, updated_at: updatedAt }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("blog-save-post error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
