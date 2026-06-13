# Editing Blog Content (Important: blog HTML is generated)

**The blog post HTML files in this repo are build artifacts. Do not hand-edit them.**

Every file below is regenerated from Supabase on each deploy. Any manual edit you
make to them will be silently overwritten the next time the site deploys:

- `blog/index.html` (the hub)
- `blog/posts/<slug>/index.html` (every post)
- `blog/category/<slug>/index.html` (category landings)
- `blog/feed.xml` (RSS)
- `blog/search-index.json`
- All localized copies under `<lang>/blog/...`

## Where blog content actually lives

The source of truth is the Supabase table **`blog_posts`**. The post body is the
**`body_md`** column, stored as Markdown. Other fields used by the renderer include
`slug`, `title`, `subtitle`, `excerpt`, `seo_title`, `seo_description`, `canonical_url`,
`hero_image_url`, `hero_image_alt`, `og_image_url`, `status`, `published_at`, and the
related `blog_categories`, `blog_authors`, and `blog_tags` tables (see `POST_SELECT`
in `scripts/build_blog.py`).

`scripts/build_blog.py` fetches the row(s) via the Supabase REST API and renders
`body_md` to HTML with Python-Markdown plus these extensions:

- `tables` (pipe tables, e.g. comparison tables)
- `attr_list`, `fenced_code`, `pymdownx.superfences`
- `smarty` (straight quotes become curly; note `--`/`---` would become en/em dashes,
  so avoid them in `body_md`, consistent with the repo-wide no-em-dash rule)
- `toc` (the in-article table of contents is auto-generated from `##`/`###` headings;
  you do NOT add TOC entries by hand)

Heading anchors are slugified the same way the TOC links are, so a heading like
`## Before and after: the manual hunt` becomes `#before-and-after-the-manual-hunt`.

## How the pipeline overwrites manual edits

`.github/workflows/deploy.yml` runs on every push to `main`. Its first step,
"Refresh blog HTML from Supabase", runs `python scripts/build_blog.py --all` before
translating and deploying. That step rebuilds all post HTML from `body_md`, which is
why editing the generated `index.html` directly does nothing durable: the next deploy
reverts it. (The auto-commit that does this is titled "Auto-regenerate localized
pages [skip ci]".)

## The correct way to change a post

1. Edit the post's `body_md` (and/or other fields) in Supabase. Use the blog admin/CMS
   that feeds `blog_posts`, or a reviewed REST `PATCH` to
   `/rest/v1/blog_posts?id=eq.<post-uuid>`.
2. Regenerate. Either:
   - flip the post `status` to `publishing` (the Supabase trigger fires a
     `repository_dispatch` of type `blog_publish`, which runs `build-blog.yml`), or
   - run the build manually: `gh workflow run build-blog.yml -f post_id=<post-uuid>`,
     or a full rebuild with no input.
3. The workflow commits the regenerated HTML and the deploy rsyncs it to apiant.com.

## Editing locally (read-only against Supabase)

```bash
set -a; source ~/.apiant_keys; set +a        # provides SUPABASE_URL + SERVICE key
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/build_blog.py --all  # GETs from Supabase, writes local HTML
```

`--all` only reads from Supabase (GET) and writes local files; it does not mutate the
database. (`--post-id <uuid>` additionally calls `blog-mark-live` to flip the post's
status, so prefer `--all` for local preview.)

## Temporary code-side injection (escape hatch, avoid)

`build_blog.py` has a `POST_BODY_IMAGES` map that injects Markdown into specific posts
by slug at render time. It exists only for content not yet moved into `body_md` and is
explicitly marked temporary. Do not use it for new content: put content in `body_md`.
