# Todo: New AI-First Homepage (index3 baseline)

Created: 2026-05-20
Plan: `tasks/plan.md`
Status legend: [ ] pending  [~] in progress  [x] done  [!] blocked

> A prior unrelated todo (blog rewrite) was archived to
> `tasks/todo-blog-rewrite.md`.

---

## [ ] Task 0 — Branch, backup, working copy
Depends on: nothing
Do:
- Create branch `feature/ai-first-homepage` from `main`.
- Copy `index.html` -> `backup/index-backup-pre-ai-homepage.html`.
- Copy `index3.html` -> `index-new.html` (working copy; all edits go here).

Acceptance:
- Branch exists and is checked out.
- `backup/index-backup-pre-ai-homepage.html` is a byte-identical copy of the
  current `index.html`.
- `index-new.html` is a byte-identical copy of `index3.html`.

Verify:
- `git branch --show-current` -> `feature/ai-first-homepage`.
- `diff index3.html index-new.html` -> no output.
- `git status` shows only new files; `index.html` and `index3.html` unmodified.

>>> CHECKPOINT A <<<

---

## [ ] Task 1 — Remove the proof-strip section
Depends on: Task 0
Do:
- In `index-new.html`, delete the entire `<section class="s proof-strip">...
  </section>` block (the "One prompt. 6 minutes. Zero human edits." section,
  ~lines 1083-1140 in index3).
- Delete the proof-strip CSS rules only: `.proof-strip` through `.pt-summary b`
  (~lines 785-813). Do NOT delete `.pt-grid` / `.pt-tier*` (pricing, ~864+).

Acceptance: plan A1, A2, A3, A4.

Verify:
- `grep -ic "one prompt\|6 minutes\|zero human\|0 human edits" index-new.html` -> 0.
- `grep -c "proof-strip" index-new.html` -> 0.
- `grep -c "pt-tier" index-new.html` -> same count as `index3.html`.
- Visual: section flow goes hero -> "What just changed" with no gap.

---

## [ ] Task 2 — Add the patent-pending pills (hero + scrolling compact)
Depends on: Task 0 (independent of Tasks 1, 3)
Do:
- Add the hero badge: `<div class="patent-badge">⚖ PATENT PENDING
  TECHNOLOGY</div>` inside `.hero-home`, just above the existing `.eyebrow`.
  The `.patent-badge` CSS class already exists in index3.
- Add the compact fixed pill markup immediately after the closing nav/header
  block, before `<section class="hero">`:
  `<div aria-hidden="true" class="patent-badge-compact"><span class="pill">⚖ PATENT PENDING</span></div>`
- Do NOT add CSS or JS — both already exist in index3 (CSS ~206-215, JS IIFE
  ~1301-1321). Confirm the JS targets `.patent-badge`, `.patent-badge-compact`,
  `img.brand`.

Acceptance: plan A9, A10, A11, A12, A13.

Verify:
- `grep -c 'class="patent-badge-compact"' index-new.html` -> exactly 1 HTML element.
- `grep -c 'class="patent-badge"' index-new.html` -> exactly 1 HTML element.
- Browser: hero pill visible on load; compact pill fades in on scroll-down and
  out on scroll-up; centered on logo.
- Only one patent scroll IIFE in the file (no duplicate listeners).

---

## [ ] Task 3 — Add the crossed-out "Any App / Any Endpoint" strip
Depends on: Task 0 (independent of Tasks 1, 2)
Do:
- Add a new CSS rule `.killshot-strip` (+ column / divider / strike / caption
  sub-rules) to index3's `<style>` block, using index3 tokens (`--font`,
  `--green`, `--card`, `--border`). Mirror index2's visual: three columns,
  vertical divider rules, line-through on column 1 with a red-tinted
  `text-decoration-color`, green text for columns 2-3.
- Add the HTML block (refactored from index2 lines 1912-1930) into
  `index-new.html`. Recommended placement: a slim band directly after the hero
  `</section>`, before "What just changed". Three columns:
  1. "8,000+ apps" (struck through) + "Their catalog (endpoints unlisted)"
  2. "Any App" (green) + "AI reads the API docs and builds it"
  3. "Any Endpoint" (green) + "Every trigger and action the API offers"
- Use plain text nodes (no inline `--hp2-*` vars) so i18n extraction picks up
  the copy.

Acceptance: plan A5, A6, A7, A8.

Verify:
- `grep -c "hp2-" index-new.html` -> 0.
- `grep -ic "8,000+ apps" index-new.html` -> 1.
- Browser: strikethrough visible on column 1; columns 2-3 green; dividers
  visible.
- Resize to 480px: columns stack/scale, no horizontal overflow.

>>> CHECKPOINT B <<< (all three deltas applied; run the full grep audit from
plan section 8)

---

## [ ] Task 4 — Local preview + full verification
Depends on: Tasks 1, 2, 3
Do:
- `python3 -m http.server 8000`, open `http://localhost:8000/index-new.html`.
- Run every item in plan section 8: static/grep audit, visual checks,
  responsive checks (1280 / 768 / 560 / 375), runtime checks (console clean, no
  404s), diff-against-baseline check.

Acceptance: plan A14, A15, A16, and all of section 8 passes.

Verify: every checkbox in plan section 8 ticked. Capture screenshots at desktop
+ mobile widths.

>>> CHECKPOINT C <<< — present results to the user. Do not proceed without
approval.

---

## [ ] Task 5 — Promote to index.html (only after approval)
Depends on: Task 4 + explicit user approval
Do:
- Copy `index-new.html` over `index.html`.
- Delete `index-new.html`.
- Re-run the visual + runtime checks (plan section 8) against `index.html`.

Acceptance: `index.html` is identical to the approved `index-new.html`; preview
of `index.html` passes all checks.

Verify:
- `diff` of the approved working copy against `index.html` -> no output.
- Browser preview of `index.html` clean.

>>> CHECKPOINT D <<< — commit/push only if the user explicitly asks. CI handles
localization regen on push to `main`.

---

## Open question for the user
- Placement of the crossed-out strip: this plan recommends a slim band between
  the hero and "What just changed". If you want it inside the hero instead (as
  in index2, where it sits below the hero video), say so before Task 3.
