/**
 * regenerate-skills-section.ts — sync Fred's ai-operability.html card inventory
 * with the current plugin + MCP tool servlets.
 *
 * Usage (apiant-website has no node_modules; borrow apiantdocs's):
 *   cd /Users/rcyeager/appdev_root/apiantdocs
 *   NODE_PATH=./node_modules npx tsx \
 *     /Users/rcyeager/appdev_root/apiant-website/scripts/regenerate-skills-section.ts
 *   # add --write at the end to apply changes (default is dry-run)
 *
 * Single dep: `gray-matter` (already in apiantdocs). If apiant-website ever
 * grows a package.json, add `gray-matter` there and drop the NODE_PATH hop.
 *
 * Sources:
 *   - Plugin skills:  /Users/rcyeager/appdev_root/apiant-claude-plugin/skills/<name>/SKILL.md
 *   - MCP servlets:   /Users/rcyeager/appdev_root/appServer/appServer/ServletMCP{Automation,Assembly}Assistant.java
 *   - Target:         /Users/rcyeager/appdev_root/apiant-website/ai-operability.html
 *
 * Scope — what this script actually does today:
 *   1. SKILLS section: for each existing `<div class="card" data-name="/xxx" ...>`
 *      inside `<section id="inventory-skills">`, rewrite:
 *        - the `data-desc="..."` attribute
 *        - the inner `<p class="desc">...</p>` text
 *      to match the SKILL.md frontmatter description.
 *      Workflow categories, glyphs, example blocks, and tags are left alone.
 *   2. MCP TOOLS section: count each toolset from the servlets and rewrite the
 *      numeric prefix in each `<div class="cat-count" data-cat-count="tools-<toolset>">`.
 *      Individual tool cards (Core + Knowledge Base) are untouched.
 *   3. Skills added in the plugin but missing from the HTML → appended below a
 *      `<!-- NEEDS-MANUAL-PLACEMENT -->` marker at the end of inventory-skills.
 *
 * Out of scope (marked TODO at the relevant hooks):
 *   - Full regeneration of the `<section id="inventory-tools">` per-tool cards.
 *   - Re-authoring `data-example` / `data-when` fields from SKILL.md.
 *   - Translating per-toolset tool-count changes into new individual cards.
 *   Those require editorial choices (animations, tags, example traces) that
 *   live only in Fred's HTML.
 */

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";

const PLUGIN_SKILLS_DIR = "/Users/rcyeager/appdev_root/apiant-claude-plugin/skills";
const AUTOMATION_SERVLET = "/Users/rcyeager/appdev_root/appServer/appServer/ServletMCPAutomationAssistant.java";
const ASSEMBLY_SERVLET   = "/Users/rcyeager/appdev_root/appServer/appServer/ServletMCPAssemblyAssistant.java";
const TARGET_HTML        = "/Users/rcyeager/appdev_root/apiant-website/ai-operability.html";

const USE_COLOR = process.stdout.isTTY;
const c = {
  green:  (s: string) => USE_COLOR ? `\x1b[32m${s}\x1b[0m` : s,
  yellow: (s: string) => USE_COLOR ? `\x1b[33m${s}\x1b[0m` : s,
  red:    (s: string) => USE_COLOR ? `\x1b[31m${s}\x1b[0m` : s,
  dim:    (s: string) => USE_COLOR ? `\x1b[2m${s}\x1b[0m` : s,
  cyan:   (s: string) => USE_COLOR ? `\x1b[36m${s}\x1b[0m` : s,
};

// ---------------------------------------------------------------------------
// Plugin + servlet loaders (same logic as apiantdocs/scripts/check-docs-sync.ts)
// ---------------------------------------------------------------------------

type PluginSkill = { command: string; description: string };

function readPluginSkills(): PluginSkill[]
{
  const out: PluginSkill[] = [];
  for (const entry of readdirSync(PLUGIN_SKILLS_DIR))
  {
    const path = join(PLUGIN_SKILLS_DIR, entry, "SKILL.md");
    if (!existsSync(path) || !statSync(path).isFile()) continue;
    const raw = readFileSync(path, "utf8");
    const { data } = matter(raw);
    // Em-dash strip: Fred's apiant.com CLAUDE.md forbids em-dashes anywhere on
    // the marketing site. Strip on the way in so every downstream write
    // (data-desc attr, <p class="desc"> text, NEEDS-MANUAL-PLACEMENT stubs)
    // is clean automatically.
    const rawDesc = typeof data.description === "string" ? data.description.trim() : "";
    const description = rawDesc.replace(/\s*—\s*/g, ", ");
    out.push({ command: `/${entry}`, description });
  }
  return out.sort((a, b) => a.command.localeCompare(b.command));
}

function readServletToolsets(): Record<string, number>
{
  const byToolset: Record<string, number> = {};
  for (const file of [AUTOMATION_SERVLET, ASSEMBLY_SERVLET])
  {
    const txt = readFileSync(file, "utf8");
    const nameRe = /objTool\.put\("name",\s*"([a-zA-Z0-9_]+)"\s*\)/g;
    const toolsetRe = /objTool\.put\("toolset",\s*"([a-zA-Z0-9_]+)"\s*\)/g;
    const names: Array<{ pos: number; name: string }> = [];
    const toolsets: Array<{ pos: number; toolset: string }> = [];
    let m: RegExpExecArray | null;
    while ((m = nameRe.exec(txt)) !== null) names.push({ pos: m.index, name: m[1] });
    while ((m = toolsetRe.exec(txt)) !== null) toolsets.push({ pos: m.index, toolset: m[1] });

    for (let i = 0; i < names.length; i++)
    {
      const cur = names[i];
      const next = names[i + 1]?.pos ?? txt.length;
      const prev = names[i - 1]?.pos ?? 0;
      const ts = toolsets.find(t => t.pos > cur.pos && t.pos < next)
              ?? toolsets.find(t => t.pos > prev && t.pos < cur.pos);
      const key = ts?.toolset ?? "(unknown)";
      byToolset[key] = (byToolset[key] ?? 0) + 1;
    }
  }
  return byToolset;
}

// ---------------------------------------------------------------------------
// HTML mutations
// ---------------------------------------------------------------------------

function escapeForDoubleQuotedAttr(s: string): string
{
  // data-desc can use either single or double quotes. We emit double-quote form,
  // so any " in the value must be replaced with its HTML entity. Single quotes
  // do not need escaping inside double-quoted attrs; newlines are rare.
  return s.replace(/"/g, "&quot;").replace(/\n/g, " ");
}

function escapeText(s: string): string
{
  // Text inside <p class="desc">...</p> — must escape HTML special chars.
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

/**
 * Rewrite `data-desc` attribute and inner `<p class="desc">...</p>` text of
 * every skill card whose `data-name` appears in the `descByCommand` map.
 * Reports cards touched. Does NOT create new cards here (new-skill appending
 * is handled separately).
 */
function rewriteSkillCardDescs(
  html: string,
  descByCommand: Map<string, string>,
): { html: string; touched: string[]; unknown: string[] }
{
  const touched: string[] = [];
  const unknown: string[] = [];

  // Card boundary: `<div class="card" ... data-kind="skill" data-name="..." ...>` ... `</div>`.
  // Skill names may be slash-prefixed (/build-automation) or slashless subskills
  // (assembly-trigger-new, pattern-chat-widget). Match both by requiring
  // data-kind="skill" explicitly, so this regex doesn't also hit tool cards.
  const cardRe = /<div class="card"[^>]*data-kind="skill"[^>]*data-name="([a-z0-9/\-_]+)"[^>]*>[\s\S]*?<p class="desc">[^<]*<\/p>\s*<\/div>/g;

  const newHtml = html.replace(cardRe, (block, name) =>
  {
    // Normalize: look up plugin desc with and without leading slash
    const lookups = [name, name.startsWith("/") ? name.slice(1) : `/${name}`];
    let desc: string | undefined;
    for (const key of lookups)
    {
      desc = descByCommand.get(key);
      if (desc) break;
    }
    if (!desc)
    {
      unknown.push(name);
      return block;
    }

    let updated = block;

    // 1. Rewrite data-desc — may be `data-desc="..."` OR `data-desc='...'`.
    const dataDescDouble = /data-desc="[^"]*"/;
    const dataDescSingle = /data-desc='[^']*'/;
    const newDataDesc = `data-desc="${escapeForDoubleQuotedAttr(desc)}"`;

    if (dataDescDouble.test(updated))
    {
      updated = updated.replace(dataDescDouble, newDataDesc);
    }
    else if (dataDescSingle.test(updated))
    {
      updated = updated.replace(dataDescSingle, newDataDesc);
    }

    // 2. Rewrite <p class="desc">...</p>
    updated = updated.replace(
      /<p class="desc">[^<]*<\/p>/,
      `<p class="desc">${escapeText(desc)}</p>`,
    );

    touched.push(name);
    return updated;
  });

  return { html: newHtml, touched, unknown };
}

/**
 * Rewrite the `<span class="cc-num">N</span>` inside each toolset `cat-count`
 * block so the per-toolset totals on the page match the servlet counts.
 *
 * Fred's markup:
 *   <div class="cat-count" data-cat-count="tools-toolsets" data-unit="toolset">
 *     <span class="cc-num">9</span> toolsets · 125 tools
 *   </div>
 *
 * We only touch the per-toolset inner cards — those are individual card blocks
 * with `data-category="tools"` and `data-name="<toolset_name>"`. The leading
 * "N tools." phrase in `<p class="desc">N tools. ...</p>` gets rewritten too.
 */
function rewriteToolsetCounts(
  html: string,
  countByToolset: Record<string, number>,
): { html: string; touched: string[] }
{
  const touched: string[] = [];

  // Match each toolset card inside inventory-tools: a card whose data-name
  // is one of the known toolset names and whose data-category="tools".
  const knownToolsets = Object.keys(countByToolset);

  for (const ts of knownToolsets)
  {
    const count = countByToolset[ts];
    // Match the full card for this toolset, including everything through the
    // visible `<p class="desc">...</p>` and its closing `</div>`. The lazy
    // `[\s\S]*?<\/div>` form would stop at the first `</div>` (the glyph's
    // close), missing the visible paragraph and the data-example text.
    const cardRe = new RegExp(
      `(<div class="card[^"]*"[^>]*data-name="${ts}"[^>]*>[\\s\\S]*?<p class="desc">[^<]*<\\/p>\\s*<\\/div>)`,
      "g",
    );
    let changed = false;
    const newHtml = html.replace(cardRe, (block) =>
    {
      let updated = block;

      // data-desc="N tools. ..." leading count
      updated = updated.replace(
        /data-desc="(\d+)\s+tools\./,
        (_full, _n) => `data-desc="${count} tools.`,
      );

      // Visible <p class="desc">N tools. ...</p>
      updated = updated.replace(
        /<p class="desc">(\d+)\s+tools\./,
        (_full, _n) => `<p class="desc">${count} tools.`,
      );

      // data-example "-> N tools: ..." inside the activate_toolset sample
      updated = updated.replace(
        /-&gt;\s+(\d+)\s+tools:/,
        (_full, _n) => `-&gt; ${count} tools:`,
      );

      if (updated !== block) changed = true;
      return updated;
    });

    if (changed) touched.push(ts);
    html = newHtml;
  }

  return { html, touched };
}

/**
 * Skills in the plugin but missing from the HTML get a stub card appended in a
 * NEEDS-MANUAL-PLACEMENT block before `</section>` of inventory-skills.
 *
 * TODO: auto-assign category (setup/build/edit/test/triggers/actions/etc.) and
 * pick a glyph. That requires heuristics that live in Fred's editorial pass, so
 * for now we emit stubs that say "NEEDS-MANUAL-PLACEMENT" and leave glyph blank.
 */
function appendMissingSkills(
  html: string,
  missing: PluginSkill[],
): { html: string; appendedCount: number }
{
  if (missing.length === 0) return { html, appendedCount: 0 };

  const marker = "<!-- NEEDS-MANUAL-PLACEMENT -->";
  const sectionCloseRe = /(<section class="s" id="inventory-skills"[\s\S]*?)(<\/section>)/;
  const match = sectionCloseRe.exec(html);
  if (!match) return { html, appendedCount: 0 };

  const stubs = missing.map((s) =>
    `<div class="card" data-category="unassigned" data-desc="${escapeForDoubleQuotedAttr(s.description)}" data-kind="skill" data-name="${s.command}" data-tags="unassigned" data-title="${s.command}" data-when="TODO">\n` +
    `<div class="glyph"></div>\n` +
    `<div class="name notranslate">${s.command}</div>\n` +
    `<div class="title">${s.command}</div>\n` +
    `<p class="desc">${escapeText(s.description)}</p>\n` +
    `</div>`,
  ).join("\n");

  const injection = `\n<!-- NEEDS-MANUAL-PLACEMENT -->\n` +
    `<div class="cat" data-cat-key="unassigned">\n` +
    `<div class="cat-ico"></div>\n` +
    `<div><div class="cat-title">Unassigned</div><div class="cat-desc">Plugin skills added since the last website sync. Move each into its real category manually.</div></div>\n` +
    `<div class="cat-count" data-cat-count="unassigned" data-unit="skill"><span class="cc-num">${missing.length}</span> skills</div>\n` +
    `</div>\n` +
    `<div class="grid" data-cat-key="unassigned">\n${stubs}\n</div>\n`;

  // Inject right before the closing `</section>` of inventory-skills. If the
  // NEEDS-MANUAL-PLACEMENT block already exists, we do NOT duplicate it; we
  // assume an editor is already working on it.
  if (html.slice(match.index, match.index + match[1].length).includes(marker))
  {
    return { html, appendedCount: 0 };
  }

  const newHtml = html.slice(0, match.index + match[1].length)
    + injection
    + html.slice(match.index + match[1].length);

  return { html: newHtml, appendedCount: missing.length };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main()
{
  const args = new Set(process.argv.slice(2));
  const write = args.has("--write");

  const plugin = readPluginSkills();
  const toolsetCounts = readServletToolsets();
  const html = readFileSync(TARGET_HTML, "utf8");

  const descByCommand = new Map(plugin.map((s) => [s.command, s.description]));

  // 1. Rewrite skill card descriptions
  const step1 = rewriteSkillCardDescs(html, descByCommand);

  // 2. Find which plugin skills the HTML is missing — look at skill cards only
  // (data-kind="skill"), and normalize slash-less names against the /foo form.
  const htmlSkillNames = new Set<string>();
  for (const m of html.matchAll(/<div class="card"[^>]*data-kind="skill"[^>]*data-name="([a-z0-9/\-_]+)"/g))
  {
    const raw = m[1];
    htmlSkillNames.add(raw.startsWith("/") ? raw : `/${raw}`);
  }
  const missing = plugin.filter((s) => !htmlSkillNames.has(s.command));

  const step2 = appendMissingSkills(step1.html, missing);

  // 3. Rewrite toolset count prefixes
  const step3 = rewriteToolsetCounts(step2.html, toolsetCounts);

  const newHtml = step3.html;
  const diffBytes = newHtml.length - html.length;

  // Report
  console.log(c.cyan(`Plugin skills:     ${plugin.length}`));
  console.log(c.cyan(`HTML cards found:  ${htmlSkillNames.size}`));
  console.log();
  console.log(c.green(`Skill cards with desc rewritten: ${step1.touched.length}`));
  if (step1.unknown.length > 0)
  {
    console.log(c.yellow(`Skill cards in HTML with no matching SKILL.md: ${step1.unknown.length}`));
    for (const n of step1.unknown) console.log(`  ${c.dim(n)}`);
  }
  console.log(c.green(`Missing skills appended as NEEDS-MANUAL-PLACEMENT: ${step2.appendedCount}`));
  console.log(c.green(`Toolset count blocks updated: ${step3.touched.length}`));
  if (step3.touched.length > 0)
  {
    for (const ts of step3.touched) console.log(`  ${c.dim(ts)}  -> ${toolsetCounts[ts]} tools`);
  }
  console.log();
  console.log(`Byte delta: ${diffBytes > 0 ? "+" : ""}${diffBytes}`);

  if (write)
  {
    if (newHtml === html)
    {
      console.log(c.green(`[OK] No changes to write.`));
      return;
    }
    writeFileSync(TARGET_HTML, newHtml);
    console.log(c.green(`[WROTE] ${TARGET_HTML}`));
  }
  else
  {
    console.log(c.yellow(`(dry run — pass --write to apply changes)`));
  }
}

main();
