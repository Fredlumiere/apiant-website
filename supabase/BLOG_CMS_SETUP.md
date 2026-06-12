# Blog CMS — One-Time Setup

Steps that have to happen by hand (can't be encoded in SQL migrations).

## 1. Apply migrations

```bash
# Push to Supabase project kereljzjgeerrdnssttu
supabase db push
# Or apply manually in Studio SQL editor:
#   supabase/migrations/20260518_001_blog.sql
#   supabase/migrations/20260518_002_blog_storage.sql
```

## 2. Enable required extensions (one-time)

In Supabase Studio → Database → Extensions, enable:

- `pg_net` (for the publish trigger's HTTP POST to GitHub)
- `vault` (for storing the GitHub PAT)

## 3. Create a GitHub fine-grained PAT

GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new.

- Repository: `Fredlumiere/apiant-website`
- Permissions:
  - `Contents`: Read and write
  - `Actions`: Read and write
- Expiration: 1 year, set a calendar reminder to rotate.

Copy the token (`github_pat_...`).

## 4. Store the PAT in Supabase Vault

Supabase Studio → Settings → Vault → New secret.

- Name: `github_dispatch_pat`
- Secret: paste the GitHub PAT
- Save.

The `trigger_blog_publish_workflow()` function reads it via `vault.decrypted_secrets`.

## 5. Add GitHub repo secrets

GitHub → repo → Settings → Secrets and variables → Actions → New secret.

| Name                          | Value                                                  |
| ----------------------------- | ------------------------------------------------------ |
| `SUPABASE_URL`                | `https://kereljzjgeerrdnssttu.supabase.co`             |
| `SUPABASE_SERVICE_ROLE_KEY`   | Supabase Studio → Settings → API → `service_role` key  |

These are read by `scripts/build_blog.py` to fetch posts during the rebuild workflow.

## 6. Configure Supabase Auth

Studio → Authentication → Providers:

- Enable Email, **disable password sign-in**, enable Magic Links.
- Redirect URL: `https://apiant.com/admin/blog/`
- Site URL: `https://apiant.com`

Studio → Authentication → Sign In / Up:

- Add an email domain allowlist hook (or use the `handle_new_blog_user` trigger
  in the migration, which already silently ignores non-`@apiant.com` signups
  by skipping the `blog_authors` insert. The trigger is the safety net; the
  allowlist hook is the early-rejection layer).

## 7. Seed an admin author for Fred

```sql
-- Run in Studio SQL editor after Fred signs in once via magic link
UPDATE blog_authors
SET role = 'admin',
    display_name = 'Fred Lumiere',
    role_title = 'Founder & CEO',
    bio = 'Founder of APIANT. Integration platform builder for two decades.'
WHERE auth_user_id = (SELECT id FROM auth.users WHERE email = 'fred@apiant.com');
```

## 8. Paste the anon key into the admin SPA

The admin UI at `/admin/blog/index.html` needs the Supabase **anon key** to
run magic-link sign-in and the Realtime subscription. Anon keys are
designed to be public; RLS policies are what gate access.

Studio → Settings → API → copy the `anon` key (NOT the `service_role` key).

Then in `admin/blog/index.html`, replace `PASTE_ANON_KEY_HERE` with the
value. One line, one place.

## 9. Verify the publish trigger works

```sql
-- Insert a dummy post in 'publishing' state to fire the trigger
INSERT INTO blog_posts (slug, title, body_md, author_id, status)
SELECT 'webhook-smoke-test', 'Webhook smoke test', '# hi', id, 'publishing'
FROM blog_authors WHERE role = 'admin' LIMIT 1;

-- Watch GitHub Actions for a `blog_publish` dispatch.
-- Then clean up:
DELETE FROM blog_posts WHERE slug = 'webhook-smoke-test';
```

## 10. Unpublishing or deleting a post

The CMS has no delete button. Use the repo script, which handles Supabase,
storage, and the generated HTML (English + all locales) in one pass:

```bash
# Take a post off the site but keep it as a CMS draft (row + media kept):
python3 scripts/delete_blog_post.py --slug <slug> --unpublish

# Permanently delete the row and its blog-media/<slug>/ images:
python3 scripts/delete_blog_post.py --slug <slug> --delete

# Then commit and push; deploy.yml's scoped rsync --delete removes the
# folders from apiant.com.
```

## 11. Social share (og:image) convention

Social scrapers (Facebook, LinkedIn, X) do not decode AVIF. Page heroes can
be `.avif`, but `og_image_url` must point to a JPEG or PNG copy (ideally
~1200x630). Convention: upload the hero as `01-hero.avif` plus a JPEG
sibling `01-hero-og.jpg` in the same `blog-media/<slug>/` folder and set
`og_image_url` to the `.jpg`. `build_blog.py` prints a WARN at build time
for any live post whose og:image is `.avif`.
