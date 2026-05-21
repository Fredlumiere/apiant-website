# Implementation Plan — New AI-First Homepage (index3 baseline)

Created: 2026-05-20
Skill: agent-skills:planning-and-task-breakdown
Status: AWAITING HUMAN REVIEW

> Note: a prior, unrelated blocked plan (API Apps blog rewrite) was archived to
> `tasks/plan-blog-rewrite.md` / `tasks/todo-blog-rewrite.md` before this file
> was written. It was not deleted.

## Goal

Ship a new main homepage that launches the AI-first Claude Code platform
positioning. Baseline is `index3.html`. Three concrete deltas are required:

1. Remove the "One prompt. 6 minutes. Zero human edits." proof-strip section
   entirely.
2. Add the crossed-out "8,000+ apps" -> "Any App" / "Any Endpoint" motif from
   `index2.html`.
3. Add the gold "PATENT PENDING" pill that appears under the logo on scroll,
   matching `index2.html` behavior.

No code changes are made by this plan. This is the plan only.

---

## 1. Files to inspect

### Primary
- `index3.html` (215 KB) — the baseline. All structure and content start here.
- `index2.html` (380 KB) — donor for the crossed-out motif and the patent-pill
  reference behavior.
- `index.html` (331 KB) — the currently live homepage. Replaced at promotion
  time; back it up first.

### Shared assets (referenced, NOT modified)
- `css/normalize.css`, `css/components.css`, `css/apiant.css` — global
  stylesheets, linked by all three files. No edits.
- `js/reveal.js` — scroll-reveal animations. Loaded by both index2 and index3.
- `js/i18n.js` — language detection / switcher. Loaded last.
- `js/cookie-consent.js`, `js/apiant.js` — consent + sign-in button state.
- `videos/1-transcode.mp4|.webm`, `videos/1-poster-00001.jpg` — index2 hero
  video. NOT needed here; the crossed-out strip is text-only.

### Findings from inspection (these change the plan materially)

- **index3 already contains the patent CSS and JS.** `index3.html` has
  `.patent-badge` and `.patent-badge-compact` CSS rules (lines ~206-215) and the
  scroll JS IIFE (lines ~1301-1321) already copied in. But there are **no
  matching HTML elements** in the body, so the JS is inert
  (`if(!hero||!compact)return;`). The work is to add the two HTML elements — not
  to port CSS or JS.
- **index3's logo is `img.brand`** (line ~570). The patent JS aligns the compact
  pill to `document.querySelector('img.brand')` — this selector already resolves
  in index3. No JS change needed.
- **The crossed-out strip in index2 (lines ~1912-1930) is built with inline
  styles** referencing `var(--hp2-font)` and `var(--hp2-green)` — index2's
  design tokens. index3 does NOT define those. The strip must be **refactored**
  to index3's tokens (`var(--font)`, `var(--green)`) and to a class-based rule,
  since index3's convention is class-based CSS in the `<head>` `<style>` block.
- **The proof-strip uses `.pt-*` classes that collide by name with the
  pricing-tiers section.** Proof terminal CSS is lines ~785-813 (`.proof-strip`,
  `.proof-*`, `.pt-bar`, `.pt-line`, `.pt-summary`...). The pricing section at
  lines ~864-875 also uses a `.pt-` prefix (`.pt-grid`, `.pt-tier`,
  `.pt-tier-name`). Unrelated despite the shared prefix. Only remove 785-813;
  never touch 864+.

---

## 2. What to copy vs. refactor

| Element | Source | Action |
|---|---|---|
| Patent CSS (`.patent-badge`, `.patent-badge-compact`) | already in index3 | Keep as-is. No copy. |
| Patent scroll JS | already in index3 | Keep as-is. No copy. |
| `.patent-badge` hero element (gold "PATENT PENDING TECHNOLOGY") | index2 line 1414 (`.hp2-badge` variant) | Refactor: add a `.patent-badge` element to index3's hero. The `.patent-badge` class is already styled gold in index3. Place it above the `.eyebrow` in `.hero-home`. |
| `.patent-badge-compact` fixed pill | index2 line 1409 | Copy markup verbatim: `<div aria-hidden="true" class="patent-badge-compact"><span class="pill">⚖ PATENT PENDING</span></div>`. Place immediately after the closing nav/header block, before `<section class="hero">`. |
| Crossed-out "8,000+ apps / Any App / Any Endpoint" strip | index2 lines 1912-1930 | Refactor: rebuild as an index3-native block. `var(--hp2-font)`->`var(--font)`, `var(--hp2-green)`->`var(--green)`. Move inline styles into a new `.killshot-strip` CSS rule in index3's `<style>` block. Preserve the effect: line-through on "8,000+ apps" with a red-tinted strike color, green for the two "Any" columns, vertical divider rules between the three columns. |
| Proof-strip section ("One prompt. 6 minutes...") | index3 lines ~1083-1140 | DELETE the entire `<section class="s proof-strip">...</section>`. |
| Proof-strip CSS | index3 lines ~785-813 | DELETE rules 785-813 only (`.proof-strip`, `.proof-head`, `.proof-terminal`, `.pt-bar*`, `.pt-line`, `.pt-prompt`...`.pt-summary b`). Do NOT delete `.pt-grid`/`.pt-tier*` at 864+. |

---

## 3. Dependency graph

```
                  ┌─────────────────────────┐
                  │  Task 0: Backup + branch │
                  └────────────┬────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
 ┌──────▼───────┐     ┌─────────▼────────┐    ┌────────▼─────────┐
 │ Task 1       │     │ Task 2           │    │ Task 3           │
 │ Remove       │     │ Add patent pill  │    │ Add crossed-out  │
 │ proof-strip  │     │ (HTML elements   │    │ "Any App" strip  │
 │ (HTML + CSS) │     │  only — CSS/JS   │    │ (HTML + new CSS) │
 │              │     │  already present)│    │                  │
 └──────┬───────┘     └─────────┬────────┘    └────────┬─────────┘
        │                       │                      │
        └───────────────────────┼──────────────────────┘
                               │
                  ┌────────────▼────────────┐
                  │ Task 4: Local preview +  │
                  │ verification checklist   │
                  └────────────┬────────────┘
                               │
                  ┌────────────▼────────────┐
                  │ Task 5: Promote to       │
                  │ index.html (on approval) │
                  └─────────────────────────┘
```

Tasks 1, 2, 3 are independent of each other (different regions of the file) and
can be done in any order, but each is a complete vertical slice (markup +
styling + verify). Task 4 gates everything. Task 5 only runs after human
approval.

### Concrete dependencies to satisfy

- **Crossed-out text effect** needs: `text-decoration: line-through` +
  `text-decoration-color` (red-tinted), index3 tokens `--font` and `--green`.
  No JS, no assets, no images. `text-decoration-color` is supported in all
  current browsers — no fallback needed.
- **Scrolling pill behavior** needs: (a) a `.patent-badge` element in the hero
  for the JS to measure `getBoundingClientRect().bottom < 60`; (b) a
  `.patent-badge-compact` element for the JS to toggle `.visible` on; (c)
  `img.brand` logo present (it is). CSS uses `position:fixed`, `backdrop-filter`
  (already has `-webkit-` fallback), and a `--logo-center` custom property set
  by JS. All three already exist in index3 except the two HTML elements. Confirm
  exactly one copy of the patent IIFE exists after edits (no duplicate scroll
  listeners).
- **No new fonts, images, or JS files.** Everything required is already loaded
  by index3.

---

## 4. Task breakdown

See `tasks/todo.md`. Each task is a vertical slice: markup + style +
self-verification, with acceptance criteria and verification steps.

---

## 5. Checkpoints between phases

- **Checkpoint A — after Task 0:** working branch created, `index.html` backed
  up, working copy `index-new.html` created from `index3.html`. `git status`
  shows only the new files.
- **Checkpoint B — after Tasks 1-3:** all three deltas applied to
  `index-new.html`. Run the grep audit (section 8) to confirm the proof-strip is
  gone and both new motifs are present. No promotion yet.
- **Checkpoint C — after Task 4:** local preview verified against the full
  checklist (visual, responsive, console-clean). Present results to the user.
- **Checkpoint D — Task 5:** only on explicit user approval, promote
  `index-new.html` to `index.html`. Final preview pass on `index.html`.

---

## 6. Safe approach

1. **Branch.** Currently on `main`. Create `feature/ai-first-homepage` before
   any file write (project rule: branch first when on default branch).
2. **Back up the live file.** Copy `index.html` to
   `backup/index-backup-pre-ai-homepage.html`. The `backup/` directory is the
   documented place for staging copies.
3. **Work on a copy, not the live file.** Copy `index3.html` to `index-new.html`
   and apply all edits there. The live `index.html` is untouched until the final
   promotion step, so a broken intermediate state never reaches a served file.
4. **Integrate the three deltas** into `index-new.html` (Tasks 1-3).
5. **Verify locally** with `python3 -m http.server` and a browser / Chrome
   DevTools MCP (Task 4).
6. **Promote only on approval:** copy `index-new.html` over `index.html`, delete
   `index-new.html`, re-verify `index.html` in preview.
7. **Localization note:** the site auto-translates on push to `main` via CI. Do
   NOT hand-edit `/{lang}/` files. Editing English `index.html` and pushing is
   sufficient. Keep the crossed-out strip copy in plain text nodes so string
   extraction picks it up.
8. **Commit/push only when the user asks.** This plan does not commit.

---

## 7. Acceptance criteria

Done when all of the following hold on `index-new.html` (and then `index.html`):

### Removal
- A1. No text "One prompt", "6 minutes", "Zero human edits", "0 human edits"
  anywhere in the file.
- A2. The `<section class="s proof-strip">` element no longer exists.
- A3. The proof-terminal CSS rules (785-813) are removed; pricing-tier `.pt-*`
  rules (864+) still exist and the pricing section still renders.
- A4. No broken anchor: the removed section's "See all 127 tools" link is gone;
  no other section linked into `.proof-strip`.

### Crossed-out motif
- A5. A three-column strip renders with "8,000+ apps" struck through
  (line-through, red-tinted strike), and "Any App" + "Any Endpoint" in green.
- A6. Captions render under each column ("Their catalog (endpoints unlisted)",
  "AI reads the API docs and builds it", "Every trigger and action the API
  offers").
- A7. The strip uses index3 design tokens (`--font`, `--green`); no `--hp2-*`
  variables leak in (undefined in index3, would render as fallback/black).
- A8. The strip is responsive: three columns on desktop, gracefully stacks or
  scales on mobile (<=480px) without overflow.

### Patent pill
- A9. A gold "PATENT PENDING" pill is visible in the hero on initial load (the
  `.patent-badge` element).
- A10. On scroll, once the hero patent badge passes above the top of the
  viewport, a compact gold "⚖ PATENT PENDING" pill fades in, fixed just under
  the nav, horizontally centered on the logo.
- A11. On scroll back up, the compact pill fades out.
- A12. The compact pill is hidden at <=560px (per the existing media query) and
  does not overlap nav links.
- A13. Exactly one copy of the patent scroll IIFE exists; no duplicate scroll
  listeners.

### Global
- A14. No JavaScript console errors on load or scroll.
- A15. Nav, footer, cookie banner, popup form all still function (unchanged from
  index3).
- A16. Visual styling is consistent with index3's dark theme; no layout shift or
  orphaned whitespace where the proof-strip used to be.

---

## 8. Verification checklist (Task 4 — how this is verified once implemented)

Run a local server: `python3 -m http.server 8000`, open
`http://localhost:8000/index-new.html`.

### Static / grep audit (before opening a browser)
- [ ] `grep -ic "one prompt\|6 minutes\|zero human\|0 human edits" index-new.html` -> 0.
- [ ] `grep -c "proof-strip" index-new.html` -> 0.
- [ ] `grep -c "pt-tier" index-new.html` -> unchanged from index3 (pricing intact).
- [ ] `grep -c "patent-badge-compact" index-new.html` -> at least 2 (CSS + JS +
  exactly one HTML `<div>`).
- [ ] `grep -c "hp2-" index-new.html` -> 0 (no index2 tokens leaked).
- [ ] `grep -ic "8,000+ apps" index-new.html` -> 1.

### Visual checks (Chrome DevTools MCP — claude-in-chrome per user pref)
- [ ] Hero loads with the gold "PATENT PENDING TECHNOLOGY" pill visible.
- [ ] Scroll down ~600px: compact "⚖ PATENT PENDING" pill fades in under the
  logo, centered on the logo's x-axis.
- [ ] Scroll back to top: compact pill fades out.
- [ ] Crossed-out strip: "8,000+ apps" has a visible strikethrough; the two
  "Any" columns are green; dividers visible between columns.
- [ ] The space where the proof-strip section used to be shows no gap, no
  leftover heading, clean section flow into "What just changed".
- [ ] Pricing-tiers section still renders normally (proves the `.pt-*` removal
  was surgical).

### Responsive checks (resize viewport)
- [ ] 1280px / 1024px: three-column strip holds; pill behavior normal.
- [ ] 768px: strip readable; nav collapses as in index3.
- [ ] 560px and below: compact patent pill hidden (display:none); crossed-out
  strip stacks/scales without horizontal scroll.
- [ ] 375px (mobile): no overflow, no overlapping text, hero pill scales down
  per the `.patent-badge` media query.

### Runtime checks
- [ ] DevTools Console: zero errors, zero new warnings vs. baseline index3.
- [ ] DevTools Network: no 404s for assets.
- [ ] Scroll performance: pill toggle is smooth (listener is `{passive:true}`).
- [ ] Resize the window: compact pill re-centers on the logo (the `resize`
  handler re-runs `alignToLogo`).

### Cross-check against baseline
- [ ] Diff `index-new.html` against `index3.html`: changes confined to (1)
  proof-strip removal, (2) two patent HTML elements, (3) one crossed-out strip
  block + one CSS rule. Nothing else touched.

If every box is checked and Checkpoint C is approved, promote to `index.html`
(Task 5) and re-run the visual + runtime checks against `index.html`.

---

## 9. Destructive-change disclosure

- Task 5 overwrites the live `index.html`. The pre-change file is preserved at
  `backup/index-backup-pre-ai-homepage.html` (Task 0).
- No other file deletions. `index3.html` and `index2.html` are left intact as
  reference.
- No commit/push performed by this plan.

## 10. Out of scope

- index2's hero video, pipeline animation, audience pills, and other `hp2-*`
  sections (not requested; only the crossed-out motif is ported).
- Any change to nav, footer, pricing, or other index3 sections.
- Localized `/{lang}/` files (CI regenerates them on push).
