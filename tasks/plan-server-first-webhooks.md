# Plan: Remove legacy browser webhook calls, switch to server-first relay

Created: 2026-05-29
Skill: agent-skills:planning-and-task-breakdown
Status: AWAITING HUMAN REVIEW. No code changed yet (read-only investigation done).
Note: saved here (not tasks/plan.md) because tasks/plan.md holds an unrelated
active plan ("New AI-First Homepage"). Do not clobber that.

## 1. Context and current state (verified)

No SPEC.md; this plan is the spec. Static HTML + Supabase edge functions (Deno).
Standard deploy = push to `main` → CI (`deploy.yml`) regenerates locales + rsyncs.
rsync EXCLUDES `supabase/`, `*.py`, `*.md`, `backup/`, `.claude/`.

### Live webhook families (English source; counts exclude locales/.claude/backup/node_modules)

| ID | Family | Form | Pages | Browser payload | Server status |
|----|--------|------|-------|-----------------|---------------|
| `e68fef48…` | Main lead | qualification popup `#contact-form` + "call now" event | 33 | `CQ_FORM_DATA`: PageTitle, CompanyType, CompanyTypeLabel, CompanyDomain, WorkEmail, Mobile, Company, IntegrationNeeds (+WantsCallNow) | Relayed by `submit-lead` → `APIANT_LEAD_WEBHOOK_URL` (live). Browser call removed on `index.html` main path only. |
| `9d4c71be…` | Contact Us ("apiapps") | `#contact-us-form` | 17 | PageTitle, FirstName, LastName, Company, WorkEmail, Mobile, Country, IntegrationNeeds; client guards: hidden `#cu-website` honeypot + 2s timer | NO server endpoint; browser POSTs directly. |
| `a09f77e9…` | DEAD | — | 0 live (only `backup/`) | n/a | Do NOT wire. |

### Surfaced inconsistency (resolved)
Brief assumes a distinct "apiapps webhook". Only second live family is Contact Us
(`9d4c71be`) on apiapps/product pages — treat that as the apiapps family.
`a09f77e9` is dead (backup only), excluded. If a different live apiapps URL was
meant, STOP and reconcile before Phase 1.

### Env vars
- `APIANT_LEAD_WEBHOOK_URL`: SET (e68fef48 value), live.
- `APIANT_APIAPPS_WEBHOOK_URL`: NOT set; must = `9d4c71be` URL value before its
  browser call is removed.

## 2. Critical risk + safety net
Removing a browser webhook makes CRM delivery depend on the server relay (URL +
field shape). Mitigations: relay reuses EXACT legacy field names (downstream
unchanged); `submit-lead` persists leads regardless of relay; Contact Us has no
persistence today, so its removal is gated behind a live relay check (Checkpoint A).

## 3. Target architecture
- Main lead + call-now → `submit-lead` → `APIANT_LEAD_WEBHOOK_URL` (call-now via an
  `event:"call_now"` flag forwarded by relay; no browser webhook).
- Contact Us → NEW `submit-apiapps` → `APIANT_APIAPPS_WEBHOOK_URL`, mirroring
  submit-lead guards.
- No frontend hardcoded URLs; frontend posts only to `…/functions/v1/{submit-lead,submit-apiapps}`.

## 4. Dependency graph
```
relay.ts (buildContactParams, url param) ┐
leadvalidate.ts (validateContact)        ┼─> submit-apiapps (new) ┐
cors/honeypot/ratelimit (reuse)          ┘                        │
APIANT_APIAPPS_WEBHOOK_URL secret ───────────────────────────────┤
submit-lead (call-now passthrough) ──> deploy fns ──> CHECKPOINT A (relay live-verified)
                                                                  │
frontend: remove e68fef48 + 9d4c71be calls ──> CI grep guard ──> deploy static ──> CHECKPOINT B (live)
```

## 5. Phases / vertical slices (each = one complete path)

### Phase 0 — Confirm assumptions (gate)
- T0 Confirm `9d4c71be`=apiapps downstream; `a09f77e9` stays dead.
  Accept: human confirms or supplies real URL. Verify: decision gate.

### Phase 1 — Server: apiapps path end-to-end
- T1 `relay.ts`: add `buildContactParams(lead)` + parameterize `relayToWebhook(url|envKey)`.
  Accept: exact legacy field names; empty→"". Verify: deno test + node sim (Mobile/Country empty→"" not "null").
- T2 `leadvalidate.ts`: add `validateContact()` (name req, email valid, phone preserved/optional, caps).
  Accept: rejects bad input; preserves non-empty phone. Verify: deno test.
- T3 New `submit-apiapps/index.ts`: origin check, validate, rate limit, honeypot,
  ip+email idempotency, relay → `APIANT_APIAPPS_WEBHOOK_URL`, `apiapps_accept/_reject`
  logs naming the downstream. Add `config.toml` `verify_jwt=false`.
  Accept: valid relayed to apiapps URL, invalid rejected, logs name family. Verify: node sim + deno tests + config entry.
- T4 `submit-lead`: add `event`/`wants_call_now` passthrough to relay.
  Accept: flag forwarded to LEAD url when set, else unchanged. Verify: test.

### CHECKPOINT A (human + live)
Set `APIANT_APIAPPS_WEBHOOK_URL`. Deploy `submit-lead` + `submit-apiapps`. Submit one
real Contact Us + one main lead. Gate: logs show `relay:"ok"` to the CORRECT
downstream and both reach the CRM. Else STOP (no frontend changes).

### Phase 2 — Frontend: route to server, remove legacy calls
- T5 Contact Us (17 pages): `$.ajax` 9d4c71be → `fetch` submit-apiapps; keep client
  guards; add `form_id`. Accept/Verify: no `9d4c71be` in English source; sample page hits submit-apiapps only.
- T6 Main lead + call-now (33 pages): remove remaining `e68fef48` blocks; route
  call-now via submit-lead event flag. Accept/Verify: no `e68fef48` in English source.
- T7 CI guard: grep step failing build if `apiant.com/webhook/` appears in non-backup
  English source. Accept: fails on planted URL, passes clean. Verify: local dry-run.

### CHECKPOINT B (live)
Push → CI translate+rsync. Verify live on homepage, /ai, a partner page, an apiapps
page: `mobile` present; only `functions/v1/...` calls; zero `apiant.com/webhook/`;
evidence main lead→LEAD url, Contact Us→APIAPPS url.

## 6. Verification strategy
- Static grep (absence of webhook URLs in English source).
- Unit: deno tests for both relay builders, validators, routing selection,
  phone/mobile non-null preservation; node sim where deno absent.
- Live: curl representative pages; Supabase logs for correct downstream per family.

## 7. Rollback
Revert the static commit + redeploy to restore browser calls. Server endpoints are
additive; secrets only added, values unchanged.

## 8. Out of scope / retained
- `a09f77e9` dead webhook: not wired.
- `backup/`, `.claude/`: never deployed.
- AI-Advantage `contact-form` (Resend email): unrelated, untouched.
