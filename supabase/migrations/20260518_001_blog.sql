-- APIANT Blog CMS schema
-- Tables: authors, categories, tags, posts, post_tags (join), post_revisions (history)
-- Auth model: Supabase Auth (magic link), domain-restricted to @apiant.com
-- Post bodies stay English-only; hub/category pages localize via existing pipeline.

-- ---------------------------------------------------------------------------
-- AUTHORS
-- Standalone table linked to auth.users so we can keep display names,
-- avatars, and bios independent of Supabase Auth profile fields, and so
-- posts stay attributable if a user is deactivated.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS blog_authors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  auth_user_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE SET NULL,
  slug TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  role_title TEXT,                                -- e.g. "Founder & CEO"
  bio TEXT,
  avatar_url TEXT,
  role TEXT NOT NULL DEFAULT 'editor' CHECK (role IN ('admin', 'editor')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_blog_authors_auth_user ON blog_authors (auth_user_id);

-- ---------------------------------------------------------------------------
-- CATEGORIES (4 mutually-exclusive top-level buckets)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS blog_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Seed the four launch categories
INSERT INTO blog_categories (slug, name, description, sort_order) VALUES
  ('use-cases',          'Use Cases',          'Real integration problems solved with the APIANT platform.', 1),
  ('customer-stories',   'Customer Stories',   'How real builders and companies shipped with APIANT.', 2),
  ('builder-playbooks',  'Builder Playbooks',  'Reproducible how-tos for SaaS engineers and SI partners.', 3),
  ('platform-deep-dives','Platform Deep Dives','Technical explainers of APIANT capabilities and architecture.', 4)
ON CONFLICT (slug) DO NOTHING;

-- ---------------------------------------------------------------------------
-- TAGS (free-form, but the launch set follows Joy's 4 axes: vertical,
-- partner, audience, capability)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS blog_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO blog_tags (slug, name) VALUES
  -- vertical
  ('fitness-wellness', 'Fitness & Wellness'),
  ('healthcare',       'Healthcare'),
  ('nonprofit',        'Nonprofit'),
  ('cross-vertical',   'Cross-Vertical'),
  -- integration partner
  ('mindbody',     'Mindbody'),
  ('cliniko',      'Cliniko'),
  ('donorperfect', 'DonorPerfect'),
  ('hubspot',      'HubSpot'),
  ('salesforce',   'Salesforce'),
  ('stripe',       'Stripe'),
  ('shopify',      'Shopify'),
  -- audience
  ('for-saas',       'For SaaS'),
  ('for-si',         'For SIs'),
  ('for-enterprise', 'For Enterprise'),
  -- capability
  ('ai-copilot',         'AI Co-Pilot'),
  ('assembly-editor',    'Assembly Editor'),
  ('formapps',           'FormApps'),
  ('mcp-servers',        'MCP Servers'),
  ('data-engine',        'Data Engine'),
  ('bi-directional-sync','Bi-Directional Sync')
ON CONFLICT (slug) DO NOTHING;

-- ---------------------------------------------------------------------------
-- POSTS
-- status state machine: draft -> saved -> publishing -> live | failed
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS blog_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  subtitle TEXT,
  excerpt TEXT,
  body_md TEXT NOT NULL DEFAULT '',
  body_html TEXT,                                  -- rendered cache, refreshed on save
  hero_image_url TEXT,
  hero_image_alt TEXT,
  category_id UUID REFERENCES blog_categories(id),
  author_id UUID NOT NULL REFERENCES blog_authors(id),
  -- SEO overrides; fall back to title/excerpt/hero when null
  seo_title TEXT,
  seo_description TEXT,
  canonical_url TEXT,
  og_image_url TEXT,
  -- publish lifecycle
  status TEXT NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'saved', 'publishing', 'live', 'failed')),
  publish_status_msg TEXT,                         -- failure reason or progress note
  published_at TIMESTAMPTZ,
  scheduled_for TIMESTAMPTZ,
  -- timestamps
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_blog_posts_status_published ON blog_posts (status, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_blog_posts_category ON blog_posts (category_id);
CREATE INDEX IF NOT EXISTS idx_blog_posts_author ON blog_posts (author_id);

-- updated_at trigger
CREATE OR REPLACE FUNCTION blog_posts_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_blog_posts_updated_at ON blog_posts;
CREATE TRIGGER trg_blog_posts_updated_at
  BEFORE UPDATE ON blog_posts
  FOR EACH ROW EXECUTE FUNCTION blog_posts_set_updated_at();

-- ---------------------------------------------------------------------------
-- POST <-> TAGS JOIN
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS blog_post_tags (
  post_id UUID NOT NULL REFERENCES blog_posts(id) ON DELETE CASCADE,
  tag_id  UUID NOT NULL REFERENCES blog_tags(id)  ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

CREATE INDEX IF NOT EXISTS idx_blog_post_tags_tag ON blog_post_tags (tag_id);

-- ---------------------------------------------------------------------------
-- POST REVISIONS (history)
-- Written by edge function blog-save-post on every successful save.
-- Keep last 50 per post (enforced by application, not trigger, so we keep
-- the SQL surface small).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS blog_post_revisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES blog_posts(id) ON DELETE CASCADE,
  author_id UUID REFERENCES blog_authors(id),
  title TEXT NOT NULL,
  body_md TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_blog_post_revisions_post
  ON blog_post_revisions (post_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- AUTH HOOK: auto-create a blog_authors row when an @apiant.com user signs up
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION handle_new_blog_user()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.email LIKE '%@apiant.com' THEN
    INSERT INTO blog_authors (auth_user_id, slug, display_name, role)
    VALUES (
      NEW.id,
      split_part(NEW.email, '@', 1),
      COALESCE(NEW.raw_user_meta_data->>'name', split_part(NEW.email, '@', 1)),
      'editor'
    )
    ON CONFLICT (auth_user_id) DO NOTHING;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created_blog ON auth.users;
CREATE TRIGGER on_auth_user_created_blog
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_blog_user();

-- ---------------------------------------------------------------------------
-- ROW LEVEL SECURITY
-- - Public can read live posts, live tags, all categories, public author info.
-- - Authenticated users with a blog_authors row can read/write per-row rules.
-- - Service role bypasses RLS (used by build_blog.py and blog-mark-live).
-- ---------------------------------------------------------------------------
ALTER TABLE blog_posts          ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_post_revisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_post_tags      ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_authors        ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_categories     ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_tags           ENABLE ROW LEVEL SECURITY;

-- Public reads
DROP POLICY IF EXISTS "public reads live posts" ON blog_posts;
CREATE POLICY "public reads live posts" ON blog_posts
  FOR SELECT
  USING (status = 'live');

DROP POLICY IF EXISTS "public reads live post tags" ON blog_post_tags;
CREATE POLICY "public reads live post tags" ON blog_post_tags
  FOR SELECT
  USING (EXISTS (SELECT 1 FROM blog_posts p WHERE p.id = post_id AND p.status = 'live'));

DROP POLICY IF EXISTS "public reads categories" ON blog_categories;
CREATE POLICY "public reads categories" ON blog_categories FOR SELECT USING (true);

DROP POLICY IF EXISTS "public reads tags" ON blog_tags;
CREATE POLICY "public reads tags" ON blog_tags FOR SELECT USING (true);

DROP POLICY IF EXISTS "public reads authors" ON blog_authors;
CREATE POLICY "public reads authors" ON blog_authors FOR SELECT USING (true);

-- Authenticated editors: read all posts (including drafts)
DROP POLICY IF EXISTS "editors read all posts" ON blog_posts;
CREATE POLICY "editors read all posts" ON blog_posts
  FOR SELECT TO authenticated
  USING (EXISTS (SELECT 1 FROM blog_authors a WHERE a.auth_user_id = auth.uid()));

-- Authenticated editors: insert posts with themselves as author
DROP POLICY IF EXISTS "editors insert own posts" ON blog_posts;
CREATE POLICY "editors insert own posts" ON blog_posts
  FOR INSERT TO authenticated
  WITH CHECK (author_id = (SELECT id FROM blog_authors WHERE auth_user_id = auth.uid()));

-- Editors update their own drafts; admins update any post
DROP POLICY IF EXISTS "editors update own or admin update any" ON blog_posts;
CREATE POLICY "editors update own or admin update any" ON blog_posts
  FOR UPDATE TO authenticated
  USING (
    author_id = (SELECT id FROM blog_authors WHERE auth_user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid() AND role = 'admin')
  );

-- Editors delete their own drafts; admins delete any
DROP POLICY IF EXISTS "editors delete own or admin delete any" ON blog_posts;
CREATE POLICY "editors delete own or admin delete any" ON blog_posts
  FOR DELETE TO authenticated
  USING (
    author_id = (SELECT id FROM blog_authors WHERE auth_user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid() AND role = 'admin')
  );

-- Revisions: editors read their own posts' revisions, admins read all
DROP POLICY IF EXISTS "editors read own revisions or admin read any" ON blog_post_revisions;
CREATE POLICY "editors read own revisions or admin read any" ON blog_post_revisions
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM blog_posts p
      JOIN blog_authors a ON a.id = p.author_id
      WHERE p.id = post_id
        AND (a.auth_user_id = auth.uid()
             OR EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid() AND role = 'admin'))
    )
  );

-- Revisions: only inserted by edge functions (service role); no anon/auth insert policy.
-- Same for blog_post_tags writes — edge function handles them.

-- Authors table: users can read their own row; admins can update any
DROP POLICY IF EXISTS "authors read self or admin read any" ON blog_authors;
CREATE POLICY "authors read self or admin read any" ON blog_authors
  FOR SELECT TO authenticated
  USING (
    auth_user_id = auth.uid()
    OR EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid() AND role = 'admin')
  );

DROP POLICY IF EXISTS "authors update self or admin update any" ON blog_authors;
CREATE POLICY "authors update self or admin update any" ON blog_authors
  FOR UPDATE TO authenticated
  USING (
    auth_user_id = auth.uid()
    OR EXISTS (SELECT 1 FROM blog_authors WHERE auth_user_id = auth.uid() AND role = 'admin')
  );

-- ---------------------------------------------------------------------------
-- DATABASE TRIGGER: when a post transitions to 'publishing', call the
-- GitHub repository_dispatch endpoint via pg_net.
-- The GH token is stored in Supabase Vault as 'github_dispatch_pat'.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trigger_blog_publish_workflow()
RETURNS TRIGGER AS $$
DECLARE
  v_token TEXT;
BEGIN
  IF NEW.status = 'publishing'
     AND (TG_OP = 'INSERT' OR OLD.status IS DISTINCT FROM 'publishing') THEN
    -- Read GitHub PAT from Vault. If absent (e.g. local dev), skip silently.
    SELECT decrypted_secret INTO v_token
    FROM vault.decrypted_secrets
    WHERE name = 'github_dispatch_pat'
    LIMIT 1;

    IF v_token IS NULL THEN
      RAISE NOTICE 'github_dispatch_pat not in vault; skipping repository_dispatch';
      RETURN NEW;
    END IF;

    PERFORM net.http_post(
      url := 'https://api.github.com/repos/Fredlumiere/apiant-website/dispatches',
      headers := jsonb_build_object(
        'Authorization', 'Bearer ' || v_token,
        'Accept', 'application/vnd.github+json',
        'Content-Type', 'application/json',
        'User-Agent', 'apiant-blog-publisher'
      ),
      body := jsonb_build_object(
        'event_type', 'blog_publish',
        'client_payload', jsonb_build_object(
          'post_id', NEW.id::text,
          'slug', NEW.slug
        )
      )
    );
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trg_blog_publish_dispatch ON blog_posts;
CREATE TRIGGER trg_blog_publish_dispatch
  AFTER INSERT OR UPDATE OF status ON blog_posts
  FOR EACH ROW EXECUTE FUNCTION trigger_blog_publish_workflow();

-- ---------------------------------------------------------------------------
-- HOUSEKEEPING: revision pruning function (call from edge function or cron)
-- Keep the 50 most recent revisions per post.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION prune_blog_revisions(p_post_id UUID, p_keep INTEGER DEFAULT 50)
RETURNS INTEGER AS $$
DECLARE
  v_deleted INTEGER;
BEGIN
  WITH ranked AS (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY post_id ORDER BY created_at DESC) AS rn
    FROM blog_post_revisions
    WHERE post_id = p_post_id
  )
  DELETE FROM blog_post_revisions
  WHERE id IN (SELECT id FROM ranked WHERE rn > p_keep);
  GET DIAGNOSTICS v_deleted = ROW_COUNT;
  RETURN v_deleted;
END;
$$ LANGUAGE plpgsql;
