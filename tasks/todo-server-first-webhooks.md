# Todo: Server-first webhook relay

Created: 2026-05-29
Plan: `tasks/plan-server-first-webhooks.md`
Status legend: [ ] pending  [~] in progress  [x] done  [!] blocked
(Saved here, not tasks/todo.md, which holds the unrelated AI-First Homepage todo.)

## Phase 0 — Confirm (gate)
- [ ] T0 Confirm `9d4c71be` = apiapps downstream; `a09f77e9` stays dead (or get real URL)

## Phase 1 — Server (apiapps path end-to-end)  [blocked by T0]
- [ ] T1 relay.ts: buildContactParams() + parameterize relayToWebhook(url/envKey) + tests
- [ ] T2 leadvalidate.ts: validateContact() (name req, email valid, phone preserved) + tests
- [ ] T3 submit-apiapps/index.ts: guards + relay → APIANT_APIAPPS_WEBHOOK_URL + logs; config.toml verify_jwt=false
- [ ] T4 submit-lead: call-now event/wants_call_now passthrough to relay + test

## CHECKPOINT A (human + live)  [blocked by T1-T4]
- [ ] Set APIANT_APIAPPS_WEBHOOK_URL secret (9d4c71be value)
- [ ] Deploy submit-lead + submit-apiapps
- [ ] Submit 1 real Contact Us + 1 main lead; confirm relay:"ok" to CORRECT downstream + CRM receipt
- [ ] GATE: if not verified, STOP (no frontend changes)

## Phase 2 — Frontend (remove legacy calls)  [blocked by Checkpoint A]
- [ ] T5 Contact Us (17 pages): fetch submit-apiapps; remove 9d4c71be; keep client guards; add form_id
- [ ] T6 Main lead + call-now (33 pages): remove e68fef48 blocks; route call-now via submit-lead flag
- [ ] T7 CI grep guard: fail build if apiant.com/webhook/ in non-backup English source

## CHECKPOINT B (live)  [blocked by T5-T7]
- [ ] Push → CI translate+rsync
- [ ] Verify homepage, /ai, partner page, apiapps page: mobile present, only functions/v1 calls, zero webhook URLs
- [ ] Confirm downstream routing per family via logs

## Verification (cross-cutting)
- [ ] Static grep: no apiant.com/webhook in English source
- [ ] Deno tests pass (relay builders, validators, routing, phone non-null); node sim fallback
- [ ] Live curl + Supabase logs confirm correct downstream per family
