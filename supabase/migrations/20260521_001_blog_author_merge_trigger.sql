-- Update handle_new_blog_user so that if a placeholder blog_authors row
-- exists (auth_user_id IS NULL, matching slug derived from email), it's
-- updated rather than duplicated when the real Supabase Auth user signs in.
--
-- This lets us pre-seed authors for content migration (e.g. Fred) before
-- they ever sign in, without ending up with duplicate rows later.

CREATE OR REPLACE FUNCTION handle_new_blog_user()
RETURNS TRIGGER AS $$
DECLARE
  v_slug TEXT;
  v_existing UUID;
BEGIN
  IF NEW.email LIKE '%@apiant.com' THEN
    v_slug := split_part(NEW.email, '@', 1);

    -- Try to claim a placeholder row for this email's slug.
    SELECT id INTO v_existing
    FROM blog_authors
    WHERE auth_user_id IS NULL AND slug = v_slug
    LIMIT 1;

    IF v_existing IS NOT NULL THEN
      UPDATE blog_authors
      SET auth_user_id = NEW.id
      WHERE id = v_existing;
    ELSE
      INSERT INTO blog_authors (auth_user_id, slug, display_name, role)
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
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
