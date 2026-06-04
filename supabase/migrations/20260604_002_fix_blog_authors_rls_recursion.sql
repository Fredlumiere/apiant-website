-- Fix: "infinite recursion detected in policy for relation blog_authors" (42P17)
-- on every authenticated read of blog_authors, which surfaced as the Blog CMS
-- "Unauthorized user" screen for legitimate authors/admins.
--
-- Root cause: two RLS policies on blog_authors referenced blog_authors inside
-- their own USING clause:
--   "authors read self or admin read any"  (SELECT TO authenticated)
--   "authors update self or admin update any" (UPDATE TO authenticated)
-- Each contained `EXISTS (SELECT 1 FROM blog_authors WHERE ... role = 'admin')`.
-- Evaluating a policy on blog_authors that itself queries blog_authors recurses,
-- so Postgres aborts with 42P17. Anon reads were unaffected because both
-- policies are TO authenticated; the public USING(true) read policy served anon.
--
-- Fix:
--   1. SELECT: the recursive policy is redundant (the "public reads authors"
--      USING(true) policy already permits all reads), so drop it.
--   2. UPDATE: replace the recursive admin subquery with a SECURITY DEFINER
--      helper that reads blog_authors with RLS bypassed, so no recursion.

CREATE OR REPLACE FUNCTION public.is_blog_admin()
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
STABLE
SET search_path = public, pg_temp
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.blog_authors
    WHERE auth_user_id = auth.uid() AND role = 'admin'
  );
$$;

-- 1. Drop the recursive SELECT policy; public read already covers it.
DROP POLICY IF EXISTS "authors read self or admin read any" ON blog_authors;

-- 2. Recreate the UPDATE policy without self-recursion.
DROP POLICY IF EXISTS "authors update self or admin update any" ON blog_authors;
CREATE POLICY "authors update self or admin update any" ON blog_authors
  FOR UPDATE TO authenticated
  USING (
    auth_user_id = auth.uid()
    OR public.is_blog_admin()
  );
