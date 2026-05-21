# Plan: Rewrite API Apps Blog Posts for Non-Technical Business Users

Created: 2026-05-20
Skill: agent-skills:planning-and-task-breakdown
Status: AWAITING HUMAN REVIEW

## Goal

Rewrite a pilot batch of API Apps blog posts so they speak to non-technical
business owners (gym owners, spa owners, yoga studio marketers, multi-location
marketing managers) instead of developers. Plain language, benefits-first, real
use cases, honest limitations, setup expectations, clear calls to action.
Preserve SEO value (topic intent, headings, metadata).

## Critical context discovered (read before approving)

This task description assumes things that are not true of the codebase. The
plan is built around the real architecture, not the assumptions.

1. **`blog/posts/*/index.html` is a build artifact, not a source file.**
   `scripts/build_blog.py` fetches each post's markdown (`body_md`) from a
   **Supabase `blog_posts` table** and renders the HTML. Every blog publish
   triggers a full rebuild (`build_blog.py --all`) that overwrites all post
   HTML plus `feed.xml`, `search-index.json`, and category pages. Editing the
   HTML directly is silently reverted on the next publish.
   **=> Rewrites must change the Supabase `body_md`, then rebuild.**

2. **No Supabase credentials are present locally.** `build_blog.py` needs
   `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY`. `~/.apiant_keys` does not
   exist. Securing write access is a Phase 0 prerequisite (see Task 0.1).

3. **Posts contain no product-UI screenshots.** Existing post images are
   AI-generated lifestyle photos in Supabase Storage
   (`blog-media/posts/migrated/<slug>/`). There is nothing to "replace." Real
   product screenshots (dashboard, config, workflow) require a logged-in
   APIANT product instance, which is not available. `uisnap`
   (`/opt/homebrew/bin/uisnap`) only *processes* existing screenshots into AI
   asset reference material; it cannot capture them.
   **=> Screenshots are a conditional phase (Phase 4), not a blocker on copy.**

4. **"Recent API apps posts" is ~88 posts** (the entire `api-apps` category).
   This plan covers a **7-post pilot** to prove the format before scaling.

## Assumptions (correct now or the plan proceeds on these)

- A1. Rewrites are made to Supabase `body_md` and the HTML is regenerated via
  `build_blog.py`. If Supabase access cannot be obtained, the work stops at the
  Phase 0 checkpoint rather than making throwaway HTML edits.
- A2. Pilot scope = 7 Mindbody posts (personas use Mindbody; DonorPerfect =
  nonprofits and Cliniko = clinics are off-persona and excluded from the pilot).
- A3. Facts come from the local `apipartners/mindbody/*.html` app pages and the
  existing post content only. No Claude Code project internals inspected.
- A4. Screenshots are deferred unless a logged-in product environment is
  provided (Phase 4 is conditional).
- A5. After English `body_md` changes and rebuild, localized locales are
  regenerated via `scripts/localize.py` / `scripts/update_translations.sh`.

## Pilot post set and app-page mapping

| # | Blog post slug | App page (facts source) |
|---|---|---|
| 1 | mindbody-hubspot-failed-autopay-recovery | apipartners/mindbody/mindbody-hubspot-integration-and-automation-apiant.html |
| 2 | mindbody-klaviyo-welcome-flow | apipartners/mindbody/mindbody-klaviyo-integration-and-automation-apiant.html |
| 3 | mindbody-activecampaign-trial-onboarding | apipartners/mindbody/mindbody-activecampaign-integration-and-automation-apiant.html |
| 4 | mindbody-shopify-effortless-product-sync | apipartners/mindbody/mindbody-shopify-integration-and-automation-apiant.html |
| 5 | mindbody-zoom-automatic-meetings | apipartners/mindbody/mindbody-zoom-integration-and-automation-apiant.html |
| 6 | mindbody-calendly-realtime-appointments | apipartners/mindbody/mindbody-calendly-integration-and-automation-apiant.html |
| 7 | mindbody-keap-winback-21-days | apipartners/mindbody/mindbody-keap-integration-and-automation-apiant.html |

## Dependency graph

```
0.1 Supabase access ──┐
0.2 Voice style guide ─┼──> 1.x Pilot post #1 (full vertical slice)
0.3 Working branch ───┘            │
                                   v  [CHECKPOINT A: review post #1]
                          2.1..2.6 Posts #2-#7 (parallel-safe)
                                   │
                                   v  [CHECKPOINT B: review all 7]
                          3.1 Rebuild + 3.2 Validation
                                   │
                                   v
                          4.x Screenshots (conditional)
                                   │
                                   v
                          5.1 Localization regen + 5.2 Report
```

Per-post tasks (1.x, 2.x) are vertical slices: each takes one post from
fact-gathering through rewritten `body_md` to verified rebuilt HTML. They do
not share state and can be done in any order after Checkpoint A.

## Phases and tasks

### Phase 0 — Prerequisites (CHECKPOINT before any rewrite)

**Task 0.1 — Secure Supabase write access**
- Obtain `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` for the blog project
  (`kereljzjgeerrdnssttu.supabase.co` per existing post image URLs).
- Acceptance: `python3 scripts/build_blog.py --post-id <known-id>` runs without
  an auth error against a no-op fetch.
- Verification: a dry read of one `blog_posts` row returns `body_md`.
- If access cannot be obtained: STOP. Do not edit HTML directly.

**Task 0.2 — Write the business-voice style guide**
- One page: target personas, plain-language rules, banned developer jargon,
  required section pattern (problem -> outcome -> how it works in plain terms
  -> use cases -> limitations -> setup expectations -> CTA), CTA wording.
- Acceptance: `tasks/voice-guide.md` exists and is self-contained.
- Verification: a reviewer can apply it without further questions.

**Task 0.3 — Create working branch**
- `git checkout -b blog/api-apps-business-rewrite`
- Acceptance: branch exists, not `main`.

### Phase 1 — Pilot post #1 (full vertical slice)

**Task 1.1 — Rewrite mindbody-hubspot-failed-autopay-recovery**
- Read the HubSpot app page; extract verified capabilities and limitations.
- Rewrite `body_md` per the voice guide. Preserve: core topic/intent, slug,
  H2/H3 structure (sensible, not jargon), `seo_title`, `seo_description`
  (refresh wording, keep keyword intent), canonical.
- Add an internal note in the post-rewrite summary listing the app-page URL
  used as the fact source.
- Acceptance criteria:
  - No developer jargon (no "webhook", "payload", "API call", "endpoint",
    "field mapping" without plain-language framing).
  - Contains explicit Use Cases, Limitations, and Setup Expectations sections.
  - Ends with a clear CTA to the relevant app page / "Talk to Us".
  - `seo_title` <= 60 chars, `seo_description` 120-160 chars.
  - Topic intent unchanged (still about recovering failed Mindbody auto-pays).
- Verification: rebuild this post (`build_blog.py --post-id`), open the
  generated HTML, confirm headings render, internal links resolve, hero image
  still loads.

**CHECKPOINT A** — Human reviews post #1 before the remaining 6 proceed.
Adjust the voice guide if the reviewer requests changes.

### Phase 2 — Pilot posts #2-#7

**Tasks 2.1-2.6** — One task per remaining post (slugs #2-#7 in the table
above). Each follows the exact Task 1.1 pattern and acceptance criteria
against its mapped app page. Vertical slices; order-independent.

**CHECKPOINT B** — Human reviews all 7 rewritten posts.

### Phase 3 — Build and validation

**Task 3.1 — Full blog rebuild**
- `python3 scripts/build_blog.py --all`
- Acceptance: all 7 posts + hub + category pages + `feed.xml` regenerate with
  exit code 0.

**Task 3.2 — Content/link/image validation**
- Verify each rewritten post: HTML well-formed, all internal links resolve,
  all `<img>` src URLs return 200, JSON-LD present, single H1.
- Acceptance: zero broken links/images across the 7 posts.
- Verification: scripted link/image check over the 7 post directories.

### Phase 4 — Screenshots (CONDITIONAL — only if a product env is provided)

**Task 4.1 — Capture product screens**
- If a logged-in APIANT product URL/credentials are provided: capture
  overview/dashboard, configuration summary, and a representative workflow.
- Process via `uisnap` if asset cleanup is needed; upload web-ready images to
  Supabase Storage under `blog-media/posts/<slug>/` (project convention).
- Update `body_md` image references; rebuild.
- If no environment is provided: skip; log as a follow-up item in the report.

### Phase 5 — Localization and report

**Task 5.1 — Regenerate locales**
- `scripts/localize.py` / `scripts/update_translations.sh` so the 19 locales
  pick up the rewritten English content.
- Acceptance: localized post HTML reflects new structure.

**Task 5.2 — Final report**
- List: posts updated, app-page URLs referenced (internal note), screenshots
  added/replaced (or deferred), validation outcome.

## Destructive-change disclosure

- `build_blog.py --all` (Task 3.1) overwrites all blog post HTML, category
  pages, `feed.xml`, and `search-index.json`. This is the normal build path,
  but it touches files beyond the 7 pilot posts. Listed here per the
  "list destructive changes before applying" requirement.
- Supabase `body_md` updates (Phases 1-2) modify production database rows.
  These should be done on non-live/draft status if the blog workflow supports
  it, or scheduled, to avoid publishing mid-edit.
- No file deletions planned.

## Out of scope

- The other ~81 api-apps posts (scale-up after pilot approval).
- Cliniko and DonorPerfect posts (off-persona).
- Claude Code project internals.
- Real product-UI screenshots unless a logged-in environment is provided.
