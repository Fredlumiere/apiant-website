-- APIANT Blog CMS storage bucket
-- Bucket: blog-media (public read, authenticated write)
-- Holds: hero images, inline post images, author avatars.
-- Path conventions enforced by the application:
--   posts/<post-id>/hero.<ext>
--   posts/<post-id>/inline/<uuid>.<ext>
--   authors/<author-id>/avatar.<ext>

INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'blog-media',
  'blog-media',
  true,
  10485760,  -- 10 MB
  ARRAY[
    'image/png',
    'image/jpeg',
    'image/webp',
    'image/avif',
    'image/svg+xml',
    'image/gif'
  ]
)
ON CONFLICT (id) DO UPDATE
  SET public = EXCLUDED.public,
      file_size_limit = EXCLUDED.file_size_limit,
      allowed_mime_types = EXCLUDED.allowed_mime_types;

-- Public read access (already implied by public=true but make it explicit)
DROP POLICY IF EXISTS "blog-media public read" ON storage.objects;
CREATE POLICY "blog-media public read" ON storage.objects
  FOR SELECT
  USING (bucket_id = 'blog-media');

-- Authenticated editors can upload (one row in blog_authors).
DROP POLICY IF EXISTS "blog-media editors insert" ON storage.objects;
CREATE POLICY "blog-media editors insert" ON storage.objects
  FOR INSERT TO authenticated
  WITH CHECK (
    bucket_id = 'blog-media'
    AND EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid())
  );

-- Editors can update/delete only files they uploaded (owner-checked by Supabase).
-- Admins can update/delete any.
DROP POLICY IF EXISTS "blog-media editors update own or admin any" ON storage.objects;
CREATE POLICY "blog-media editors update own or admin any" ON storage.objects
  FOR UPDATE TO authenticated
  USING (
    bucket_id = 'blog-media'
    AND (
      owner = auth.uid()
      OR EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid() AND role = 'admin')
    )
  );

DROP POLICY IF EXISTS "blog-media editors delete own or admin any" ON storage.objects;
CREATE POLICY "blog-media editors delete own or admin any" ON storage.objects
  FOR DELETE TO authenticated
  USING (
    bucket_id = 'blog-media'
    AND (
      owner = auth.uid()
      OR EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid() AND role = 'admin')
    )
  );
