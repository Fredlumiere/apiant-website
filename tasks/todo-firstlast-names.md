# Todo: require first_name + last_name on lead/contact forms
Plan: tasks/plan-firstlast-names.md   [ ]=pending [x]=done

## Phase 1 server
- [ ] T1 relay.ts: FirstName/LastName on lead builder
- [ ] T2 submit-lead: require names + map to relay (incl. call-now)
- [ ] T3 submit-apiapps: require BOTH names
- [ ] T4 tests: fix key-count assertion + name cases
- [ ] CHECKPOINT A: deploy functions

## Phase 2 frontend
- [ ] T5 popup: add First/Last name required inputs (33 pages)
- [ ] T6 handler: read+require names, set CQ_FORM_DATA
- [ ] T7 leadData: add first_name/last_name
- [ ] T8 Contact Us/#stc: ensure required attrs
- [ ] CHECKPOINT B: guard + deploy static + live verify
