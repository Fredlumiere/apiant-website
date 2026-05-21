# Claude Code Repositioning — Site Revision Plan

**Date:** 2026-05-21
**Trigger:** New AI / Claude-Code-first homepage went live 2026-05-20. A press release on the new capability is planned; the rest of the site must match the homepage before that PR runs.
**Scope:** 12 platform-related pages. Excluded by direction: homepage, API App product pages (`apipartners/**`), legal, blog.
**Method:** Five parallel specialist reviews — Marketing/messaging (Ava), Visual design (Zoe), Sales/positioning (Gil), Engineering/technical accuracy (Sam), UX/IA (Pete).

---

## 1. Headline finding

All five reviews converged on the same conclusion: **the repositioning exists only on the homepage.** "Claude Code" does not appear in substantive copy on 10 of the 12 in-scope pages. `ai-operability.html` is the only other on-message page. Every nav click from the new homepage currently lands a visitor on a page that describes the old, human-operated platform ("the Builder's Integration Platform", "assign a workflow architect").

A press release amplifies this: it drives a traffic spike straight into the contradiction. Tier 1 pages must be revised before the PR.

---

## 2. Quick wins — fix immediately, independent of the larger effort

The reviews surfaced live errors and credibility risks that should be fixed now:

1. **`ai-operability.html` `<title>` says "40 Skills, 127 MCP Tools".** Every other page and the homepage say 42 skills / 138 MCP tools. Stale number on the canonical page, visible in Google SERPs. (Sam)
2. **`for-enterprises.html`: "No engineer touched it."** Directly contradicts the site's own human-review FAQ on `ai.html`. Factual overclaim. (Sam)
3. **`assembly-editor.html`: Co-Pilot "generates code".** Contradicts the homepage's core claim — "structured data, not compiled code." Reword to "builds structured connector configurations through live API discovery." (Sam)
4. **`platform/index.html`: image alt text "APIANT Unified XML Engine".** Violates the Data Engine messaging rule (never expose internals). Change to "unified data processing engine." (Sam)
5. **`apps.html`: title says "250+ apps", meta says "500+ connectors".** Internal contradiction; standardize. (Ava)
6. **`for-saas.html` / `for-enterprises.html` comparison tables: unqualified "builds it autonomously" cells.** Add the human-review qualifier already used in the `ai.html` FAQ. (Sam)

Effort: ~1 day total. No dependencies.

---

## 3. Cross-cutting workstreams

These patterns repeat on nearly every page and should be handled as consistent passes, not per-page improvisation.

### 3a. Messaging (Ava)
- Thread Claude Code through every page: each page should state, in its hero or immediately below, that Claude Code operates the relevant capability via 42 skills / 138 MCP tools.
- **Retire the "workflow architect as operator" framing.** It appears on `platform/index.html`, `for-saas.html`, `for-si.html`. Under the new positioning the architect is an oversight/strategy role; Claude Code is the builder.
- **Standardize one "first" claim.** Three competing ones exist today ("first of its kind in iPaaS", "first integration platform in the world with this capability", "first iPaaS Claude Code can fully operate"). Pick the homepage's and use it everywhere.
- Fix terminology drift: connector counts, skill/tool counts, "AI Co-Pilot" used inconsistently as a feature vs. a product.

### 3b. Visual design (Zoe)
- **Accent-color fragmentation is the most visible break.** Audience pages use blue (`for-saas`), amber (`for-si`), purple (`for-enterprises`), cyan (`ai.html`, `chatbot.html`). The homepage system is green `#1ab759`. Unify all to green. Most are inline-SVG color swaps — low effort, high impact.
- **9 of 12 pages have no hero visual.** The homepage set the bar with the Claude Code terminal mockup + animated dataflow SVG. Tier 1 pages need hero visuals in that language.
- Add a Claude Code terminal / agent-operator motif to the six highest-traffic SVG diagrams (currently none depict Claude Code as the operator).
- Unify the monospace/terminal font stack across all code blocks.

### 3c. Technical accuracy (Sam)
- Resolve the overclaims in Quick Wins #2–#6.
- Keep the builder/executor distinction explicit everywhere: Claude Code *builds* the integration; APIANT's deterministic execution engine *runs* it with error handling, retry, monitoring. This is the answer to "is AI-built logic reliable."
- Enforce Data Engine messaging rules on every revised page.

### 3d. Information architecture (Pete)
- The Platform nav dropdown has 9 items with unclear grouping. Restructure (see Section 6).
- Resolve the `ai.html` / `ai-operability.html` / `mcp-servers.html` three-way redundancy (see Section 5 — decision required).

---

## 4. Per-page revision plan

Consensus gap rating shown. Tier = revision priority.

### TIER 1 — the conversion funnel; revise before the press release

**`platform/index.html` — HIGH (unanimous). The #1 fix.**
First click from the homepage for every "learn more" visitor; still titled "The Builder's Integration Platform."
- Rewrite H1 + meta to lead with Claude Code operability and the 42/138 proof point.
- Move the AI/MCP operability content from section 10 (last) to section 2–3.
- Reframe the "domain expertise, not engineering skill" FAQ — it now contradicts the Claude Code-user buyer persona.
- Replace `platform-ai-copilot-mockup.svg` with a Claude Code terminal + Assembly Editor split visual.
- Two-path CTA: "See how Claude Code drives this" + "Talk to us."

**`for-saas.html` — HIGH.**
- Reframe hero away from "without diverting your engineering team" to "Claude Code builds, deploys, monitors; your team owns the outcome."
- Add a third path to "Two Ways to Work": developer-led build via Claude Code.
- Add a "Claude Code operated" row to the comparison table.
- Add a FAQ: "Are AI-built integrations production-reliable?" (builder/executor answer.)
- Hero icon: blue → green.

**`for-si.html` — HIGH. Highest deal-risk page.**
- **Add a proactive disintermediation answer, high on the page, not buried in FAQ:** Claude Code is the SI's leverage, not their replacement — domain expertise, customer ownership, and productized recurring revenue are still the moat. Silence here reads as confirmation of the fear.
- Reframe "AI Co-Pilot Multiplier" as full Claude Code operability.
- "We Eat Our Own Cooking": state that APIANT runs its own 17 products with Claude Code.
- Hero icon: amber → green.

**`for-enterprises.html` — HIGH.**
- Address the AI-governance questions head-on: audit trail for agent actions, permission scoping for what Claude Code can touch, reversibility in the Admin Console.
- Fix "No engineer touched it." overclaim (Quick Win #2).
- Add a "Claude Code operated" comparison-table row.
- Hero icon: purple → green.

**`ai.html` — HIGH.**
- Today it covers Co-Pilot/Agents/Chatbot/MCP and never mentions Claude Code — the AI page omits the AI story.
- Needs a dedicated "Claude Code as your integration engineer" section linking to `ai-operability.html`.
- Add a hero visual (Claude Code terminal → APIANT platform dataflow).
- Cyan accent → green.
- **Subject to the Section 5 decision.**

### TIER 2 — platform depth and the MCP story; revise soon after Tier 1

**`platform/automation-editor.html` — MEDIUM.** Add "Claude Code composes automations here"; move "Build Once. Deploy to Hundreds." earlier; relocate the Data Engine section to `platform/index.html`; add an FAQ.

**`platform/assembly-editor.html` — MEDIUM/HIGH.** Strongest existing AI page. Distinguish the embedded Co-Pilot (supervised) from Claude Code operating the platform (do not conflate — buyers will notice). Fix "generates code" (Quick Win #3). Recolor the amber Co-Pilot badge to green. Link to `ai-operability.html`.

**`platform/admin-console.html` — LOW/MEDIUM.** Strong as-is. Add: when Claude Code builds/deploys, the Admin Console is where the team reviews, audits, and reverses — this passively answers enterprise objections. Add MCP tool-call visual.

**`mcp-servers.html` — MEDIUM/HIGH.** Architecturally the most relevant page to the repositioning, yet Claude Code appears only in JSON-LD, not visible copy. Foreground Claude Code as the primary operator (not one client among ChatGPT et al.). Add a "Claude Code + APIANT" section. **Subject to the Section 5 decision.**

### TIER 3 — lighter touch

**`chatbot.html` — LOW/MEDIUM.** Add a note that Claude Code can build/deploy chatbots; reduce H1 collision with `ai.html`.
**`formapps.html` — LOW/MEDIUM.** Add a callout that Claude Code can scaffold and wire FormApps.
**`apps.html` — LOW/MEDIUM.** Update subhead to echo the homepage ("Tell Claude Code to build it. It ships to production."); fix the 250/500 discrepancy.

---

## 5. Decision required: `ai.html` vs `ai-operability.html` vs `mcp-servers.html`

These three pages overlap heavily. MCP is explained near-verbatim in three places (`ai.html`, `mcp-servers.html`, `platform/index.html`). `ai.html` and `ai-operability.html` compete for the same conceptual territory with no clear differentiation.

**Recommended resolution (Pete + Ava):**
- `ai-operability.html` = the dedicated Claude Code page (keep, it is the north star).
- `ai.html` = reframed as the platform-native AI customers build *with* (Co-Pilot, Agents, Chatbot) — not the external operability story.
- Collapse the duplicated MCP explainer: `mcp-servers.html` keeps the full MCP/protocol story; `ai.html` and `platform/index.html` get 2–3 sentence teasers that link to it.

This is an IA decision with SEO implications (three URLs, existing rankings). **Needs your steer before we touch those three pages.**

---

## 6. Nav / IA restructure (Pete)

Current Platform dropdown: 9 items, unclear grouping. Proposed:
- **Platform** (how it works): Platform Overview, Automation Editor, Assembly Editor, Admin Console, FormApps
- **AI / Claude Code** (the positioning): AI Operability, AI Capabilities, MCP Servers, AI Chatbot — or surface "AI Operability" as a top-level nav item given it is the headline story.

---

## 7. Per-audience objections the repositioning creates (Gil)

- **System Integrators:** "Does Claude Code replace me?" — `for-si.html` must answer directly.
- **Enterprises:** "Who approved what the AI did?" / "Can we scope its permissions?" / "Vendor risk if Anthropic changes Claude Code?" — answer with audit trail, permission scoping, and the open-MCP-standard point.
- **SaaS:** "Is AI-built logic production-reliable?" / "Who supports it?" / "Does this lock me into Anthropic?" — builder/executor distinction + open MCP standard.

---

## 8. Sequencing with the press release

1. **Now:** Quick wins (Section 2) — ~1 day.
2. **Week 1:** Tier 1 pages (5 pages). Pia drafts the press release in parallel.
3. **Press release ships** once Tier 1 is live.
4. **Week 2:** Tier 2 (4 pages). Tier 3 in parallel as capacity allows.
5. Resolve the Section 5 decision before Tier 1 `ai.html` work begins.

Realistic effort for Tier 1 + Tier 2 done well: 2–3 weeks.

---

## 9. Functional ownership

| Function | Lead | Responsibility |
|----------|------|----------------|
| Messaging / copy | Ava | Rewrites, voice consistency, "first" claim |
| Visual design | Zoe | Accent unification, hero visuals, SVG operator motif |
| Sales / positioning | Gil | Objection handling, comparison tables, CTA paths |
| Technical accuracy | Sam | Overclaim fixes, Data Engine compliance, sign-off |
| UX / IA | Pete | Nav restructure, page structure, redundancy resolution |
| Press release | Pia | PR draft, timed to Tier 1 going live |
