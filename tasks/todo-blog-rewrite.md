# Todo: API Apps Blog Rewrite (Business-User Pilot)

Branch: `blog/api-apps-business-rewrite`
Plan: `tasks/plan.md`
Status legend: [ ] pending  [~] in progress  [x] done  [!] blocked

## Phase 0 — Prerequisites (CHECKPOINT)

- [!] 0.1 Secure Supabase access — BLOCKED. No SUPABASE_URL / SERVICE_ROLE_KEY
      env vars, no .env, no ~/.apiant_keys, Supabase CLI not logged in. Cannot
      read/write blog_posts.body_md or run build_blog.py in this environment.
- [ ] 0.2 Voice guide — not written separately; voice rules applied directly
      in the post #1 draft.
- [ ] 0.3 Branch not created (no repo edits made; draft is a new file only).

## Phase 1 — Pilot post #1 (vertical slice)

- [~] 1.1 Rewrite `mindbody-hubspot-failed-autopay-recovery` — DRAFT COMPLETE,
      NOT APPLIED. Business-owner rewrite + fact-check done; saved to
      tasks/drafts/mindbody-hubspot-failed-autopay-recovery.md. Cannot write to
      Supabase or rebuild (see 0.1). Awaiting Supabase access + human review.
      - source: apipartners/mindbody/mindbody-hubspot-integration-and-automation-apiant.html
      - AC: no jargon; Use Cases + Limitations + Setup Expectations sections;
        clear CTA; seo_title <=60ch; seo_description 120-160ch; topic intent
        preserved.
      - Verify: rebuild single post, links + hero image resolve.
- [ ] CHECKPOINT A — human review of post #1; tune voice guide if needed.

## Phase 2 — Pilot posts #2-#7 (vertical slices, order-independent)

- [ ] 2.1 `mindbody-klaviyo-welcome-flow` <- mindbody-klaviyo app page
- [ ] 2.2 `mindbody-activecampaign-trial-onboarding` <- mindbody-activecampaign app page
- [ ] 2.3 `mindbody-shopify-effortless-product-sync` <- mindbody-shopify app page
- [ ] 2.4 `mindbody-zoom-automatic-meetings` <- mindbody-zoom app page
- [ ] 2.5 `mindbody-calendly-realtime-appointments` <- mindbody-calendly app page
- [ ] 2.6 `mindbody-keap-winback-21-days` <- mindbody-keap app page
      (each: same AC as Task 1.1)
- [ ] CHECKPOINT B — human review of all 7 posts.

## Phase 3 — Build and validation

- [ ] 3.1 `python3 scripts/build_blog.py --all` (exit code 0).
- [ ] 3.2 Validate 7 posts: links resolve, image src 200s, JSON-LD present,
      single H1, HTML well-formed.

## Phase 4 — Screenshots (CONDITIONAL)

- [ ] 4.1 Only if a logged-in product env is provided: capture
      overview/config/workflow screens, upload to Supabase Storage
      `blog-media/posts/<slug>/`, update body_md refs, rebuild.
      Otherwise: skip and log as follow-up.

## Phase 5 — Localization and report

- [ ] 5.1 Regenerate locales (`scripts/localize.py` / `update_translations.sh`).
- [ ] 5.2 Final report: posts updated, app-page URLs cited, screenshots
      added/replaced or deferred, validation outcome.
