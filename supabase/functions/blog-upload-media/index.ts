/**
 * blog-upload-media
 *
 * Issues a signed upload URL for the blog-media bucket so the admin SPA can
 * PUT files directly to Supabase Storage (paste-an-image-and-it-uploads UX).
 *
 * Auth: required (any editor or admin).
 *
 * POST {
 *   filename: string,
 *   content_type: string,
 *   post_id?: string,           // for posts/<post-id>/inline/...
 *   purpose?: "hero" | "inline" | "avatar"   // path convention
 * }
 *
 * Returns {
 *   path:       "posts/<id>/inline/<uuid>.<ext>",
 *   upload_url: signed PUT URL (valid 60s),
 *   public_url: final public URL
 * }
 *
 * Note: client uploads the bytes via PUT to upload_url, then writes
 * public_url into the markdown. We don't proxy bytes through the function.
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { resolveEditor, unauthorized } from "../_shared/blog_auth.ts";

const BUCKET = "blog-media";
const MAX_BYTES = 10 * 1024 * 1024;
const ALLOWED_MIME = new Set([
  "image/png",
  "image/jpeg",
  "image/webp",
  "image/avif",
  "image/svg+xml",
  "image/gif",
]);

function extFor(mime: string, filename: string): string {
  const fromName = filename.includes(".")
    ? filename.split(".").pop()!.toLowerCase().replace(/[^a-z0-9]/g, "")
    : "";
  if (fromName && fromName.length <= 5) return fromName;
  switch (mime) {
    case "image/png": return "png";
    case "image/jpeg": return "jpg";
    case "image/webp": return "webp";
    case "image/avif": return "avif";
    case "image/svg+xml": return "svg";
    case "image/gif": return "gif";
    default: return "bin";
  }
}

function uuid(): string {
  return crypto.randomUUID().replace(/-/g, "").slice(0, 16);
}

serve(async (req) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const auth = await resolveEditor(req);
    if (!auth.ok) return unauthorized(cors, auth.status, auth.error);
    const { editor } = auth;

    const body = await req.json().catch(() => ({}));
    const filename = typeof body.filename === "string" ? body.filename : "file";
    const content_type = (typeof body.content_type === "string" ? body.content_type : "").toLowerCase();
    const post_id = typeof body.post_id === "string" ? body.post_id : "";
    const purpose = ["hero", "inline", "avatar"].includes(body.purpose) ? body.purpose : "inline";

    if (!ALLOWED_MIME.has(content_type)) {
      return new Response(
        JSON.stringify({ error: "Unsupported mime type" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const supabase = getServiceClient();

    let path: string;
    if (purpose === "avatar") {
      path = `authors/${editor.author.id}/avatar.${extFor(content_type, filename)}`;
    } else {
      if (!post_id) {
        return new Response(
          JSON.stringify({ error: "post_id required for hero or inline uploads" }),
          { status: 400, headers: { ...cors, "Content-Type": "application/json" } },
        );
      }
      // Verify the editor owns the post (or is admin).
      const { data: post } = await supabase
        .from("blog_posts")
        .select("author_id")
        .eq("id", post_id)
        .single();
      if (!post) {
        return new Response(
          JSON.stringify({ error: "Post not found" }),
          { status: 404, headers: { ...cors, "Content-Type": "application/json" } },
        );
      }
      const isOwner = post.author_id === editor.author.id;
      const isAdmin = editor.author.role === "admin";
      if (!isOwner && !isAdmin) return unauthorized(cors, 403, "Not your post");

      const ext = extFor(content_type, filename);
      path = purpose === "hero"
        ? `posts/${post_id}/hero.${ext}`
        : `posts/${post_id}/inline/${uuid()}.${ext}`;
    }

    const { data: signed, error: signErr } = await supabase
      .storage
      .from(BUCKET)
      .createSignedUploadUrl(path);
    if (signErr || !signed) {
      console.error("blog-upload-media sign error:", signErr?.message);
      return new Response(
        JSON.stringify({ error: "Failed to create upload URL" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
      );
    }

    const { data: pub } = supabase.storage.from(BUCKET).getPublicUrl(path);

    return new Response(
      JSON.stringify({
        path,
        upload_url: signed.signedUrl,
        token: signed.token,
        public_url: pub.publicUrl,
        max_bytes: MAX_BYTES,
      }),
      { headers: { ...cors, "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error("blog-upload-media error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } },
    );
  }
});
