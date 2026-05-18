/**
 * Blog-specific auth helpers.
 *
 * Edge functions in /supabase/functions/blog-* expect a bearer JWT from
 * Supabase Auth in the Authorization header (set by the admin SPA via
 * @supabase/supabase-js after magic-link sign-in).
 *
 * resolveEditor:
 *   - Verifies the JWT, extracts the auth user id.
 *   - Looks up the matching blog_authors row.
 *   - Returns { user, author } on success, or an error reason.
 *
 * The service client is used to read blog_authors so RLS doesn't get in the
 * way. We treat the presence of a blog_authors row as proof of authorization
 * (the handle_new_blog_user trigger only creates one for @apiant.com signups).
 */
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { getServiceClient } from "./supabase.ts";

export type Editor = {
  authUserId: string;
  email: string;
  author: {
    id: string;
    slug: string;
    display_name: string;
    role: "admin" | "editor";
  };
};

export type EditorResult =
  | { ok: true; editor: Editor }
  | { ok: false; status: number; error: string };

export async function resolveEditor(req: Request): Promise<EditorResult> {
  const authHeader = req.headers.get("Authorization") || "";
  if (!authHeader.startsWith("Bearer ")) {
    return { ok: false, status: 401, error: "Missing Authorization header" };
  }
  const token = authHeader.slice("Bearer ".length).trim();
  if (!token) {
    return { ok: false, status: 401, error: "Empty bearer token" };
  }

  // Verify the JWT against Supabase Auth.
  const url = Deno.env.get("SUPABASE_URL")!;
  const anon = Deno.env.get("SUPABASE_ANON_KEY")!;
  const userClient = createClient(url, anon, {
    global: { headers: { Authorization: `Bearer ${token}` } },
  });
  const { data, error } = await userClient.auth.getUser(token);
  if (error || !data?.user) {
    return { ok: false, status: 401, error: "Invalid or expired token" };
  }

  const email = (data.user.email || "").toLowerCase();
  if (!email.endsWith("@apiant.com")) {
    return { ok: false, status: 403, error: "Not an authorized email domain" };
  }

  const service = getServiceClient();
  const { data: author, error: authorErr } = await service
    .from("blog_authors")
    .select("id, slug, display_name, role")
    .eq("auth_user_id", data.user.id)
    .single();

  if (authorErr || !author) {
    return {
      ok: false,
      status: 403,
      error: "No blog_authors row for this user",
    };
  }

  return {
    ok: true,
    editor: {
      authUserId: data.user.id,
      email,
      author: author as Editor["author"],
    },
  };
}

export function unauthorized(
  cors: Record<string, string>,
  status: number,
  error: string,
): Response {
  return new Response(
    JSON.stringify({ error }),
    { status, headers: { ...cors, "Content-Type": "application/json" } },
  );
}
