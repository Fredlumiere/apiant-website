# APIANT Homepage Revision — Complete Copy for Webflow
## Every section, every headline, every CTA, every paragraph

**Prepared:** February 18, 2026
**For:** Webflow developer implementation
**Reference:** APIANT-Website-Revision-Plan-v2-FINAL.md (Part 3)
**Current page:** index.html

---

## Page Meta

| Field | Value |
|-------|-------|
| `<title>` | APIANT \| The Integration Platform Builders Own |
| `meta description` | APIANT gives SaaS companies and System Integrators a dedicated, white-label integration platform with AI co-pilots, embeddable UIs, and the deepest automation engine on the market. Trusted by 8,000+ companies. |
| `og:title` | APIANT \| The Integration Platform Builders Own |
| `og:description` | Own your integration infrastructure. APIANT is a dedicated, white-label integration platform with AI co-pilots, embeddable UIs, and the deepest automation engine on the market. |
| `twitter:title` | APIANT \| The Integration Platform Builders Own |
| `twitter:description` | (same as og:description) |

---

## Navigation (Revised)

**Structure:**
```
Logo | Platform ▾ | Solutions ▾ | Connectors | Resources ▾ | [Start Building] (CTA button)
```

**Platform dropdown:**
| Label | Link |
|-------|------|
| The APIANT Platform | /platform |
| Automation Editor | /platform/automation-editor |
| Assembly Editor + AI Co-Pilot | /platform/assembly-editor |
| Admin Console | /platform/admin-console |
| AI Agents | /ai/agents |
| AI Chatbot | /ai/chatbot |
| FormApps | /formapps |
| MCP Servers | /mcp-servers |

**Solutions dropdown:**
| Label | Link |
|-------|------|
| For SaaS Companies | /for-saas |
| For System Integrators | /for-si |
| For Enterprises | /for-enterprise |
| --- (divider) | --- |
| Mindbody Integrations | /apipartners/mindbody-turnkey-integration-solutions.html |
| Cliniko Integrations | /apipartners/cliniko-turnkey-integration-solutions.html |
| DonorPerfect Integrations | /apipartners/donorperfect-turnkey-integration-solutions.html |

**Resources dropdown:**
| Label | Link |
|-------|------|
| Documentation | https://info.apiant.com |
| Blog | https://blog.apiant.com |
| Community Forum | https://forum.apiant.com |
| White Paper: The Deep Integration Gap | (existing white paper link) |

**CTA button:** "Start Building" → https://apiant.com/editor

> **Dev note:** Replace the current nav (Logo | API Apps | Who is APIANT For? | Products ▾ | Sign In / Dashboard). Keep Sign In / Dashboard buttons in top-right, separate from the main nav links. The "Start Building" CTA should be styled as a primary green button in the nav bar.

---

## SECTION 1: Hero

> **Design note:** Keep the existing dark-mode background. Keep the platform animation video (the looping hero video is a strong asset). Increase contrast slightly and slow the video playback to ~0.8x for a more premium feel. Full-bleed, cinematic.

### Headline (rotating text animation — cycle through these three)

| Element | Type | Content |
|---------|------|---------|
| Headline 1 | `H1` (rotating) | Your iPaaS. Your Brand. Your Revenue. |
| Headline 2 | `H1` (rotating) | The Integration Platform Builders Own. |
| Headline 3 | `H1` (rotating) | Ship Deep Integrations. Not Shallow Connectors. |

> **Dev note:** Use the same Webflow text-rotation animation pattern currently on the page (the "Turnkey / Powerful / Intelligent / Scalable / Profitable" cycling). Swap the content.

### Sub-headline

| Element | Type | Content |
|---------|------|---------|
| Sub-headline | `<p>` body text, large (18-20px) | APIANT gives SaaS companies and System Integrators a dedicated, white-label integration platform — with AI co-pilots, embeddable UIs, and the deepest automation engine on the market. |

### CTAs

| Element | Type | Content | Link |
|---------|------|---------|------|
| Primary CTA | Button (green, primary) | See the Platform | /platform |
| Secondary CTA | Button (outline/ghost, white border) | Talk to Us | (contact form / modal trigger) |

> **Dev note:** Use a dual-button layout, centered. Primary button is solid green (#1ab759). Secondary is transparent with white border.

### Trust Bar

| Element | Type | Content |
|---------|------|---------|
| Trust text | `<h4>` or small heading | Trusted by 8,000+ companies worldwide |

### Logo Marquee

> **Dev note:** Keep the existing partner/customer logo strip (Cliniko, Mindbody, DonorPerfect, Shopify, Calendly, Salesforce, Mailchimp, HubSpot, Klaviyo, Keap, Zoho CRM, ActiveCampaign). Use a CSS scrolling marquee animation (infinite horizontal scroll, pause on hover). This already exists on the page — keep the implementation.

### Background

| Element | Type | Content |
|---------|------|---------|
| Background video | `<video>` autoplay loop muted | Keep existing `videos/1-transcode.mp4` — the platform animation. Increase contrast. Slow to 0.8x playback speed. |

---

## SECTION 2: The Pain We Solve

> **Design note:** Dark section with high-contrast white text. This section should feel like a moment of truth — sharp, direct, no fluff. Consider a subtle dark gradient background (slightly different shade than the hero) to visually separate it.

### Headline

| Element | Type | Content |
|---------|------|---------|
| Section heading | `H2` | Integration is always the first thing to cut. |

### Body Copy (3 paragraphs)

| Element | Type | Content |
|---------|------|---------|
| Paragraph 1 | `<p>` body text | Every SaaS company and SI hits the same wall. Integration surfaces as a priority when there's a deal on the line — and it's the first thing deprioritized when AI features, core product work, or new revenue initiatives need your developers. |
| Paragraph 2 | `<p>` body text | You're left with two bad options: build shallow connectors that disappoint customers, or divert your best engineers from your product to build integrations that still won't be deep enough. And there's a real difference — a shallow integration syncs a contact; a deep one knows when your customer's client last visited, when they're coming next, that they canceled Tuesday's class so next visit is now Thursday, and that their 10-pack has one session remaining. |
| Paragraph 3 | `<p>` body text | APIANT is the third option. A dedicated integration platform — managed, scalable, AI-assisted — that makes integration the easiest part of your conversation. Assign a workflow architect, not a developer. Go deep, not wide. And never cut integration from your roadmap again. |

### CTA

| Element | Type | Content | Link |
|---------|------|---------|------|
| Section CTA | Text link with arrow (or small button) | See how it works → | /platform |

---

## SECTION 3: Three Value Pillars

> **Design note:** Three cards, side by side, equal width. Each card has a subtle hover animation (icon pulse, slight card lift, or border glow). Dark card backgrounds with accent borders or subtle gradient overlays. Cards should feel like doorways — each leads to a deep-dive page.

### Cards

**Card 1: Own Your Platform**

| Element | Type | Content |
|---------|------|---------|
| Icon | Subtle icon (e.g., shield/lock or server icon) | (icon — no text) |
| Card heading | `H3` | Own Your Platform |
| Card body | `<p>` body text | Get a dedicated APIANT server — white-labeled, fully managed, entirely yours. For SaaS companies adding deep, native integrations to their product without diverting developers. |
| Card CTA | Text link with arrow | For SaaS Companies → |
| Card CTA link | | /for-saas |

**Card 2: Build & Monetize**

| Element | Type | Content |
|---------|------|---------|
| Icon | Subtle icon (e.g., chart-up or money/growth icon) | (icon — no text) |
| Card heading | `H3` | Build & Monetize |
| Card body | `<p>` body text | Turn your integration expertise into a scalable, recurring revenue stream. For SIs and consultants ready to productize what they already know how to solve. |
| Card CTA | Text link with arrow | For System Integrators → |
| Card CTA link | | /for-si |

**Card 3: Go Deep, Not Wide**

| Element | Type | Content |
|---------|------|---------|
| Icon | Subtle icon (e.g., layers or depth icon) | (icon — no text) |
| Card heading | `H3` | Go Deep, Not Wide |
| Card body | `<p>` body text | Ship integrations with real logic, real error handling, real business value. The platform behind 17 turnkey products serving thousands of businesses — and counting. |
| Card CTA | Text link with arrow | See the Platform → |
| Card CTA link | | /platform |

---

## SECTION 4: Platform Glimpse

> **Design note:** This is a cinematic, scroll-triggered section. Left/right split layout. Left side: animated screen recording or mockup of the Assembly Editor AI Co-Pilot building an Asana "Delete Task" action. Right side: copy. Below the split, a horizontal scrolling strip of capability badges. This section should feel like a product reveal moment.

### Left Side (Visual)

| Element | Type | Content |
|---------|------|---------|
| Visual | Screen recording / animated mockup | The AI Co-Pilot in the Assembly Editor, building an Asana "Delete Task" action autonomously — finding API docs, understanding auth, generating code, testing, confirming success. |

> **Dev note:** This will need a video asset or animated sequence produced separately. Placeholder: use a static screenshot of the Assembly Editor with a "play" overlay until the video is ready. Recommended: real screen recording of the demo, sped up 2-3x, with captions at key moments.

### Right Side (Copy)

| Element | Type | Content |
|---------|------|---------|
| Section heading | `H2` | The AI That Reads API Docs So You Don't Have To |
| Body text | `<p>` body text | Type the name of any app. The AI Co-Pilot finds the API documentation, figures out authentication, builds the connector, tests it, and confirms it works. No developer needed. No API documentation to read. We believe we're the first integration platform in the world to do this. |
| CTA | Button or text link | Explore the Platform → |
| CTA link | | /platform |

### Capability Badges Strip (below the split)

> **Design note:** Horizontal row of pill-shaped badges, scrolling or static. Dark backgrounds with subtle borders. Each badge is a platform capability.

| Element | Type | Content |
|---------|------|---------|
| Badge 1 | Pill/tag | Data Engine |
| Badge 2 | Pill/tag | Assembly Editor + AI Co-Pilot |
| Badge 3 | Pill/tag | Automation Editor |
| Badge 4 | Pill/tag | FormApps |
| Badge 5 | Pill/tag | AI Agents |
| Badge 6 | Pill/tag | Chatbot |
| Badge 7 | Pill/tag | Admin Console |
| Badge 8 | Pill/tag | MCP Servers |
| Badge 9 | Pill/tag | 500+ Connectors |

> **Dev note:** Each badge can optionally link to its respective page (/platform, /formapps, /ai, etc.). On hover, subtle glow or highlight.

---

## SECTION 5: Real-World Proof — The Exercise Coach

> **Design note:** This is the visual anchor of the homepage. It should feel substantial — a full-width section with real screenshots, real numbers. Dark background with high contrast. The stats strip should be prominent. Screenshots should be high-quality, real product captures (Splunk dashboard, account network, HubSpot custom objects). No stock photography. No mockups.

### Headline

| Element | Type | Content |
|---------|------|---------|
| Section heading | `H2` | 228 Locations. One Platform. Zero Errors. |

### Body Copy (3 paragraphs)

| Element | Type | Content |
|---------|------|---------|
| Paragraph 1 | `<p>` body text | Exercise Coach runs 228 MindBody locations syncing to a single HubSpot instance through APIANT. Five custom object types — class bookings, appointments, memberships, client services, and contracts — with bi-directional sync, 120+ fields per contact, rate limiting, and real-time monitoring. |
| Paragraph 2 | `<p>` body text | Every location runs the same core logic but consumes the integration differently — different time zones, different configurations, different feature toggles. APIANT separates settings from logic, so one codebase serves all 228 locations. When we upgrade, we select the entire codebase group and deploy to everyone simultaneously. |
| Paragraph 3 | `<p>` body text | The architecture: a master account routes all CRM data to the correct MindBody site out of 228. All locations share a single CRM connection with rate limiting configured at 185 API calls per 10 seconds — a threshold calibrated to never exceed the CRM's limits even when every location renews memberships on Monday morning on January 1st. The Splunk dashboard proves it: zero errors, zero rate limit violations. |

### Visual Proof Elements

> **Dev note:** These need real screenshots. Produce these as separate assets.

| Element | Type | Content |
|---------|------|---------|
| Screenshot 1 | Image (with caption) | Splunk dashboard showing API calls per 10 seconds, never exceeding the 185/10s threshold |
| Screenshot 2 | Image (with caption) | Account network view showing 228 linked MindBody sites |
| Screenshot 3 | Image (with caption) | HubSpot custom objects (class bookings, appointments, memberships) |

### Stats Strip

> **Design note:** Horizontal row of 5 large stats. Big numbers with small labels underneath. Consider a subtle count-up animation on scroll-into-view.

| Stat number | Label below | Element type |
|-------------|-------------|--------------|
| 228 | Connected locations | `Stat` (large number + small label) |
| 5 | Custom object types | `Stat` |
| 120+ | Fields synced per contact | `Stat` |
| 185/10s | API calls managed per 10 seconds | `Stat` |
| 0 | Rate limit violations in production | `Stat` |

> **Dev note for stat labels (expanded, for tooltip or small text):**
> - "5" = class bookings, appointments, memberships, client services, contracts
> - "185/10s" = API calls managed per 10 seconds, shared across all 228 locations

### CTA

| Element | Type | Content | Link |
|---------|------|---------|------|
| Section CTA | Button or styled text link | This is what deep integration looks like. See how the platform works → | /platform |

---

## SECTION 6: Proof — Turnkey API Apps

> **Design note:** Keep the existing three-product-card layout (Mindbody, Cliniko, DonorPerfect) but tighten the design. Add a small "Built with APIANT" badge on each card (top-right corner or below the logo). Keep links to the existing hub pages.

### Headline

| Element | Type | Content |
|---------|------|---------|
| Section heading | `H2` | 17 Turnkey Products. Built on APIANT. Shipped to Thousands. |
| Section sub-heading | `<p>` body text (subtitle) | We don't just sell the platform. We build on it — every day. These products are our proof. |

### Product Cards

**Card 1: Mindbody Integrations**

| Element | Type | Content |
|---------|------|---------|
| Logo | Image | Mindbody logo |
| Badge | Small tag/pill (top-right) | Built with APIANT |
| Card heading | `H3` or card title | Mindbody Integrations |
| Card body | `<p>` | 10 turnkey products connecting Mindbody to HubSpot, ActiveCampaign, Keap, Klaviyo, Shopify, Zoho CRM, Calendly, HighLevel, Zapier, and Zoom. |
| Card CTA | Link | Explore Mindbody Solutions → |
| Card CTA link | | /apipartners/mindbody-turnkey-integration-solutions.html |

**Card 2: Cliniko Integrations**

| Element | Type | Content |
|---------|------|---------|
| Logo | Image | Cliniko logo |
| Badge | Small tag/pill (top-right) | Built with APIANT |
| Card heading | `H3` or card title | Cliniko Integrations |
| Card body | `<p>` | 3 turnkey products connecting Cliniko to HubSpot, ActiveCampaign, and Salesforce for healthcare and allied health practices. |
| Card CTA | Link | Explore Cliniko Solutions → |
| Card CTA link | | /apipartners/cliniko-turnkey-integration-solutions.html |

**Card 3: DonorPerfect Integrations**

| Element | Type | Content |
|---------|------|---------|
| Logo | Image | DonorPerfect logo |
| Badge | Small tag/pill (top-right) | Built with APIANT |
| Card heading | `H3` or card title | DonorPerfect Integrations |
| Card body | `<p>` | 4 turnkey products connecting DonorPerfect to HubSpot, ActiveCampaign, Keap, and Mailchimp for nonprofits and fundraising organizations. |
| Card CTA | Link | Explore DonorPerfect Solutions → |
| Card CTA link | | /apipartners/donorperfect-turnkey-integration-solutions.html |

---

## SECTION 7: Testimonials

> **Design note:** Keep the existing 13 testimonials. Reformat as a cleaner carousel/slider with larger quote text, prominent name/role/company attribution. Add filtering tags ("SaaS" | "SI" | "Enterprise") so visitors can see testimonials relevant to them. Remove any placeholder/dummy testimonials (e.g., "Emily Chen / DevOps Specialist" if it still exists in the code).

### Section Heading

| Element | Type | Content |
|---------|------|---------|
| Section heading | `H2` | What Builders Say |

### Filter Tags

| Tag | Label |
|-----|-------|
| Tag 1 | All |
| Tag 2 | SaaS |
| Tag 3 | SI |
| Tag 4 | Enterprise |

> **Dev note:** Keep existing testimonial content. Just restyle the container and add the filtering mechanism. Each testimonial card should have a data attribute for category.

---

## SECTION 8: AI Capabilities

> **Design note:** Remove "Coming Soon" framing entirely. Present AI as real and shipping. Three mini-cards in a row, each with an icon and brief description. Darker section background to feel modern/technical.

### Headline

| Element | Type | Content |
|---------|------|---------|
| Section heading | `H2` | AI That Doesn't Just Chat. AI That Acts. |

### Mini-Cards

**Card 1: AI Agents**

| Element | Type | Content |
|---------|------|---------|
| Icon | Subtle icon (robot/agent) | (icon) |
| Card heading | `H3` | AI Agents |
| Card body | `<p>` | Agents with goals, tools, and the whole platform behind them. While others bolt AI onto standalone chatbots, APIANT agents operate inside the full integration platform — with access to 500+ connectors, your automations, and your business logic. |
| Card CTA | Text link | Learn more → |
| Card CTA link | | /ai/agents |

**Card 2: AI Chatbot**

| Element | Type | Content |
|---------|------|---------|
| Icon | Subtle icon (chat bubble) | (icon) |
| Card heading | `H3` | AI Chatbot |
| Card body | `<p>` | A chat is one trigger and one action. Everything between is up to your imagination. One user message can trigger complex automations — data lookups, conditional branching, API calls, notifications — all invisible to the user. |
| Card CTA | Text link | Learn more → |
| Card CTA link | | /ai/chatbot |

**Card 3: Assembly Editor AI Co-Pilot**

| Element | Type | Content |
|---------|------|---------|
| Icon | Subtle icon (sparkle/wand) | (icon) |
| Card heading | `H3` | AI Co-Pilot |
| Card body | `<p>` | The first AI in integration that builds connectors autonomously. Type an app name. The Co-Pilot researches API docs, determines authentication, generates code, tests against live APIs, and self-corrects. By morning, you have production-ready building blocks. |
| Card CTA | Text link | Learn more → |
| Card CTA link | | /platform/assembly-editor |

---

## SECTION 9: White Paper CTA

> **Design note:** Keep this section as-is. It's a strong lead-gen asset. Just ensure it uses the updated design language (tighter typography, consistent spacing). Dark gradient background.

### Content

| Element | Type | Content |
|---------|------|---------|
| Section heading | `H2` | "The Deep Integration Gap" |
| Body text | `<p>` | (Keep existing white paper description copy) |
| CTA | Button (primary green) | Download the White Paper |
| CTA link | | (existing white paper download link) |

> **Dev note:** This section already exists on the current homepage. Keep the existing content and download mechanism. Only update styling to match the new design system.

---

## SECTION 10: Footer

> **Design note:** Keep the existing footer structure. Add new links for the platform pages and audience pages.

### Footer Link Columns

**Column 1: Platform**

| Label | Link |
|-------|------|
| The APIANT Platform | /platform |
| Automation Editor | /platform/automation-editor |
| Assembly Editor + AI Co-Pilot | /platform/assembly-editor |
| Admin Console | /platform/admin-console |
| AI Agents | /ai/agents |
| AI Chatbot | /ai/chatbot |
| FormApps | /formapps |
| MCP Servers | /mcp-servers |

**Column 2: Solutions**

| Label | Link |
|-------|------|
| For SaaS Companies | /for-saas |
| For System Integrators | /for-si |
| For Enterprises | /for-enterprise |
| Mindbody Integrations | /apipartners/mindbody-turnkey-integration-solutions.html |
| Cliniko Integrations | /apipartners/cliniko-turnkey-integration-solutions.html |
| DonorPerfect Integrations | /apipartners/donorperfect-turnkey-integration-solutions.html |

**Column 3: Resources**

| Label | Link |
|-------|------|
| Documentation | https://info.apiant.com |
| Blog | https://blog.apiant.com |
| Community Forum | https://forum.apiant.com |
| White Paper | (existing link) |
| Connectors | apps.html |

**Column 4: Company**

| Label | Link |
|-------|------|
| Sign In | https://apiant.com/editor?view=login |
| Dashboard | https://apiant.com/editor |
| Privacy Policy | (existing) |
| Terms of Service | (existing) |

---

## Sections to REMOVE from Current Homepage

These existing sections should be removed (or relocated to other pages):

| Current Section | Action | Reason |
|----------------|--------|--------|
| "What's an API App?" (scroll-reveal text animation + Start Building / Explore API Apps cards) | Remove from homepage. Content moves to /platform or /solutions. | Homepage visitors who are builders don't need this primer — it slows them down. |
| "Who is APIANT For?" (sticky scroll section with SI / SaaS / Enterprise / API Apps Users) | Replace with Section 3 (Three Value Pillars) above. | The new audience-specific pages (/for-saas, /for-si) do this job much better. |
| "APIANT Marketplace" (Coming Soon section) | Remove entirely. | Teasing vaporware weakens credibility. Re-add when launched. |
| "Turnkey AI Agents" (Coming Soon framing) | Replace with Section 8 (AI Capabilities) above. | Present AI as real and shipping, not "coming soon." |
| "Built by Builders, For Builders" (current section) | Remove or fold key messaging into Section 2 (The Pain We Solve). | Redundant with the new pain/value structure. |

---

## Copy Style Guide (for Webflow developer reference)

### Voice
- **Direct.** No corporate fluff. Say what the thing does.
- **Technical but not jargon-dense.** Builders respect precision.
- **Confident without arrogance.** "We believe we're the first integration platform to do this" — confident, qualified, honest.
- **Builder-to-builder.** Write like an engineer explaining to another engineer over coffee.

### Key Phrases to Preserve Across the Site
These are from real sales conversations and land with buyers:

- "Make integration the easiest part of your conversation."
- "Assign a workflow architect, not a developer."
- "Your secret weapon for integrations."
- "Go deep, not wide."
- "We don't just sell the platform. We build on it. Every day."
- "We eat our own cooking."
- "Ingredients and recipes."
- "Settings vs. logic — that's the difference between custom work and a product."
- "The builders who master it become unstoppable."

### Typography Hierarchy

| Level | Usage | Suggested Size (desktop) |
|-------|-------|-------------------------|
| H1 | Hero headline only (one per page) | 56-72px |
| H2 | Section headings | 36-42px |
| H3 | Card headings, sub-section headings | 24-28px |
| H4 | Minor headings, trust bar text | 18-20px |
| Body | Paragraphs, descriptions | 16-18px |
| Small | Captions, risk-reversal text, stat labels | 14px |

### Colors

| Use | Value | Notes |
|-----|-------|-------|
| Primary green (CTAs) | #1ab759 | Hover: #15a04d |
| Dark background | Deep navy/charcoal (existing) | Not pure black |
| Heading text (dark sections) | #ffffff | |
| Body text (dark sections) | rgba(255,255,255,0.7) | |
| Heading text (light sections) | var(--_white-mode---heading-color) | Existing Webflow variable |
| Body text (light sections) | var(--_white-mode---paragraph-color) | Existing Webflow variable |

---

## Section Flow Summary (top to bottom)

| # | Section | Type | Background |
|---|---------|------|------------|
| 1 | Hero | Full-bleed with video bg | Dark (existing) |
| 2 | The Pain We Solve | Text-heavy, emotional | Dark (slightly different shade) |
| 3 | Three Value Pillars | 3-card grid | Dark |
| 4 | Platform Glimpse | Left/right split + badge strip | Dark |
| 5 | Exercise Coach Proof | Screenshots + stats | Dark with subtle gradient |
| 6 | Turnkey API Apps | 3 product cards | Dark |
| 7 | Testimonials | Carousel/slider with filters | Dark |
| 8 | AI Capabilities | 3 mini-cards | Dark |
| 9 | White Paper CTA | Banner | Dark gradient |
| 10 | Footer | Links | Dark |

> **Overall design note:** The entire page is dark mode. Maintain the existing dark-mode foundation (deep navy/charcoal). No light-mode sections. No stock photography anywhere. Real screenshots, real product recordings, custom illustrations or diagrams only.

---

## Content Assets Required Before Build

| Asset | Type | Status | Notes |
|-------|------|--------|-------|
| AI Co-Pilot screen recording (Asana demo) | Video | Needs production | Real demo, sped up 2-3x, captions at key moments |
| Splunk dashboard screenshot | Image | Needs capture | API calls/10s graph, zero violations visible |
| Account network screenshot (228 sites) | Image | Needs capture | Shows the master + child account structure |
| HubSpot custom objects screenshot | Image | Needs capture | Class bookings, appointments, memberships visible |
| Platform architecture diagram | Animated SVG or motion graphic | Needs design | For capability badge strip and/or Platform Glimpse |
| Card icons (3 value pillars + 3 AI cards) | SVG icons | Needs design | Subtle, line-style icons matching dark theme |

---

*This document contains every word of copy needed for the revised homepage. The Webflow developer can build directly from this — all headings, body text, CTAs, links, stats, and developer notes are specified. For the broader site revision plan (other new pages, detailed blueprints), refer to APIANT-Website-Revision-Plan-v2-FINAL.md.*
