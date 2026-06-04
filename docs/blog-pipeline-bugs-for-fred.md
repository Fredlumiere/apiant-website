# Blog publish pipeline: two bugs that need Fred's access to fix

_Written by Claude (working with Marc) on 2026-06-04, after publishing Marc's first blog post through the real pipeline for the first time._

## TL;DR

Marc's post ("How to Add a Mindbody Booking Widget to Your Shopify Store", slug `add-mindbody-booking-widget-to-shopify`) is **live on apiant.com**. But it only got there because I did two steps by hand that the pipeline is supposed to do automatically. Both bugs will break **every** future publish until fixed, and **neither can be fixed without access that only Fred has** (the Supabase project's Edge Function secrets, and a GitHub PAT identity). Details, evidence, and exact fixes below.

**Reference IDs:** build run `26965326946`, deploy run `26965529955`, publish commit `3aa613367`, post id `b2e5e31b-b811-4e5d-877a-135eba5b7776`.

---

## How the pipeline is supposed to work (context for whoever picks this up)

1. Admin/editor publishes a post in the CMS, or a row in Supabase `blog_posts` is flipped to `status = 'publishing'`.
2. A Postgres trigger (`trigger_blog_publish_workflow`) fires `repository_dispatch` (`event_type = blog_publish`) to GitHub, using the PAT in Supabase Vault (`github_dispatch_pat`).
3. `.github/workflows/build-blog.yml` runs `scripts/build_blog.py --post-id <id>`, which renders the post HTML, then **POSTs to the `blog-mark-live` edge function to flip the post `publishing -> live`**.
4. `build-blog.yml` commits the generated HTML to `main` and pushes.
5. That push is supposed to trigger `.github/workflows/deploy.yml`, which runs `build_blog.py --all` (rebuilds the hub/category/search/RSS from all `live` posts), regenerates the 20 localizations, and rsyncs to apiant.com.

**Steps 3 and 5 are both broken.** Here is what fails, what I verified, and what to do.

---

## Bug 1 — `blog-mark-live` 401s, so posts never flip to `live`

### Symptom
In build run `26965326946`, `build_blog.py` logged:

```
WARN blog-mark-live non-2xx (401): {"error":"service role required"}
OK wrote blog/posts/add-mindbody-booking-widget-to-shopify/index.html
```

The post HTML built fine, but the status stayed at `publishing`. That matters because `build_blog.py --all` (run by every deploy) only includes `status = 'live'` posts in the hub, category pages, search index, and RSS. A post stuck at `publishing` deploys its own page but is **invisible in the blog index**. I flipped Marc's post to `live` manually with the service key via PostgREST.

### Root cause (sharpened with direct evidence)
`supabase/functions/blog-mark-live/index.ts` (lines 30-35) authorizes by exact string match:

```ts
const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
const provided   = authHeader.startsWith("Bearer ") ? authHeader.slice(7).trim() : "";
if (!serviceKey || provided !== serviceKey) {
  return 401 { error: "service role required" };
}
```

So the caller's bearer token must be **byte-for-byte equal** to whatever `SUPABASE_SERVICE_ROLE_KEY` resolves to inside the edge function's runtime.

**What I tested:**
- `build_blog.py` sends the GitHub Actions secret `SUPABASE_SERVICE_ROLE_KEY` (set 2026-05-18) -> **401**.
- I then called `blog-mark-live` directly with the **current service_role key copied fresh from the Supabase dashboard** (the same key that works against PostgREST, Storage, and the Auth Admin API in this very session) -> **also 401** (`{"error":"service role required"}`).

That second result is the important one: a known-good, currently-valid service_role key is still rejected. So the value the edge function compares against (`Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")` **inside the function**) is **not** the project's real service_role key. The most likely cause is a **custom Edge Function secret named `SUPABASE_SERVICE_ROLE_KEY` that overrides the platform-injected one** with a stale/wrong value (e.g. left over from the legacy-vs-new API key migration or a JWT secret rotation). The GitHub Actions copy has drifted too, but the edge side is the real culprit.

### Why we can't fix it
Reading or correcting an Edge Function's secret requires the **Supabase dashboard (Edge Functions -> Secrets / Manage secrets)** or a **Supabase Management API access token**. The project service_role key does **not** grant that. Marc has neither. So this is Fred-only.

### What Fred needs to do
1. In the Supabase dashboard, go to **Edge Functions -> Manage secrets** and check for a `SUPABASE_SERVICE_ROLE_KEY` override. If present and stale, delete it (so the platform auto-injects the correct one) or set it to the project's current service_role key.
2. Make sure the **GitHub Actions secret** `SUPABASE_SERVICE_ROLE_KEY` (repo `Fredlumiere/apiant-website`) holds that **same** current service_role key, so `build_blog.py` and the function agree.
3. Recommended hardening: replace the brittle full-string equality in `blog-mark-live/index.ts` with a real check (verify the JWT and assert the `role` claim is `service_role`), so a key rotation can't silently 401 the publish step again.
4. Verify: re-publish a test post (or flip one to `publishing`) and confirm it reaches `live` automatically and the build log no longer shows the 401.

---

## Bug 2 — the blog build commits to `main` but never deploys to apiant.com

### Symptom
Build run `26965326946` committed the post (`3aa613367`, "Publish blog post add-mindbody-booking-widget-to-shopify", 7 files changed) and pushed to `main`. **No `Deploy to apiant.com` run fired afterward.** The post was in the repo but 404'd on apiant.com until I triggered the deploy manually (`gh workflow run deploy.yml`, run `26965529955`), which then rsynced it and regenerated the localizations.

### Root cause
`.github/workflows/build-blog.yml` checks out and pushes using the default token (line 34):

```yaml
- uses: actions/checkout@v5
  with:
    fetch-depth: 0
    token: ${{ secrets.GITHUB_TOKEN }}
```

GitHub **by design** does not trigger further workflow runs from events (like `push`) caused by commits made with the built-in `GITHUB_TOKEN`. This is GitHub's recursion guard. So `deploy.yml`'s `on: push` never fires for the blog build's commit, and nothing ships to apiant.com.

### Why we can't fix it cleanly
The standard fix is to push with a **Personal Access Token** (a PAT pushes as a real identity, so the `push` event does trigger downstream workflows). But there is **no PAT in the repo's GitHub Actions secrets** today; the only secrets present are:

```
DEEPL_API_KEY, DEPLOY_HOST, DEPLOY_PATH, DEPLOY_SSH_KEY, DEPLOY_USER,
GOOGLE_TRANSLATE_API_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL
```

(The `github_dispatch_pat` referenced elsewhere lives in **Supabase Vault** for the Postgres -> GitHub dispatch; it is not available as a GitHub Actions secret.) Minting a PAT ties it to a GitHub identity (Fred's, or a dedicated machine account), which is Fred's call, not something I should fabricate.

### What Fred needs to do (pick one)
- **Option A (recommended): push with a PAT.** Create a fine-grained PAT (on a machine account or Fred's account) with `contents:write` + `workflows` on `Fredlumiere/apiant-website`, add it as an Actions secret (e.g. `BLOG_DEPLOY_PAT`), and change `build-blog.yml`'s checkout to `token: ${{ secrets.BLOG_DEPLOY_PAT }}`. The blog commit will then trigger `deploy.yml` normally.
- **Option B: explicitly kick the deploy.** Add a final step to `build-blog.yml` that dispatches `deploy.yml` (`gh workflow run deploy.yml` or a `repository_dispatch`). Note: dispatching with `GITHUB_TOKEN` may hit the same recursion guard, so this still likely needs a PAT; Option A is cleaner.

Once either is in place, verify by publishing a post and confirming a `Deploy to apiant.com` run starts on its own and the post appears on apiant.com.

---

## What is NOT broken (so nobody re-investigates these)
- Fred's two fixes from this morning work: `handle_new_blog_user` (signup) and the `blog_authors` RLS recursion. Marc's auth user and author row were created and auto-linked cleanly.
- The Postgres `publishing` -> `repository_dispatch` trigger works (the build run fired from it).
- `build_blog.py` rendering, the hero upload to the `blog-media` bucket, tags, category, and byline all work. The post itself is correct and live.

The only two gaps are the `blog-mark-live` 401 (Bug 1) and the `GITHUB_TOKEN` non-triggering deploy (Bug 2). Both need Fred's access.
