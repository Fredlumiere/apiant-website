-- Fix: "Database error saving new user" on blog magic-link signup.
--
-- handle_new_blog_user() runs as a SECURITY DEFINER trigger on auth.users,
-- invoked by the supabase_auth_admin role during signup. It had no
-- `SET search_path`, so the unqualified `blog_authors` reference could not be
-- resolved under the auth admin's search_path. The resulting exception aborted
-- the auth.users INSERT, so no user was ever created (Auth had 0 users).
--
-- Two changes:
--   1. Pin search_path and schema-qualify every table reference.
--   2. Wrap the body so author auto-provisioning can NEVER block authentication
--      again; on any failure we warn and let the signup proceed.
CREATE OR REPLACE FUNCTION handle_new_blog_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
  v_slug TEXT;
  v_existing UUID;
BEGIN
  IF NEW.email LIKE '%@apiant.com' THEN
    v_slug := split_part(NEW.email, '@', 1);

    -- Claim a pre-seeded placeholder row for this email's slug, if one exists.
    SELECT id INTO v_existing
    FROM public.blog_authors
    WHERE auth_user_id IS NULL AND slug = v_slug
    LIMIT 1;

    IF v_existing IS NOT NULL THEN
      UPDATE public.blog_authors
      SET auth_user_id = NEW.id
      WHERE id = v_existing;
    ELSE
      INSERT INTO public.blog_authors (auth_user_id, slug, display_name, role)
      VALUES (
        NEW.id,
        v_slug,
        COALESCE(NEW.raw_user_meta_data->>'name', v_slug),
        'editor'
      )
      ON CONFLICT (auth_user_id) DO NOTHING;
    END IF;
  END IF;
  RETURN NEW;
EXCEPTION WHEN OTHERS THEN
  -- Bookkeeping must never break auth. Log and let the user be created.
  RAISE WARNING 'handle_new_blog_user failed for %: %', NEW.email, SQLERRM;
  RETURN NEW;
END;
$$;
