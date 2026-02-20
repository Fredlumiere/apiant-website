# APIANT Website Graphics Brief

Comprehensive specification for all illustrations, diagrams, and visual assets needed across the APIANT marketing website. Organized by priority: Critical (visible placeholders on live pages), High (text-only audience/feature pages), Medium (nice-to-have enhancements).

**Date:** 2026-02-20
**Prepared for:** Recraft V3 API / DALL-E / Illustrator

---

## Brand Reference: Colors and Style

These values are extracted from `css/apiant.css` and page-level `<style>` blocks.

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-color` | `#0c0c0c` | Dark-mode page background |
| `--heading-color` | `#f7f8f8` | Heading text |
| `--paragraph-color` | `rgba(255,255,255,0.8)` | Body text |
| `--accent-color` (legacy) | `#f36725` | Orange accent (Webflow legacy, used sparingly) |
| Green primary | `#1ab759` | Primary CTA, badges, accents across all new pages |
| Green hover | `#159a4a` / `#15a34a` | Darker green for hover states |
| Green glow | `rgba(26,183,89,0.12)` | Background radial gradient glow |
| Card background | `rgba(255,255,255,0.03)` | Subtle translucent cards |
| Card border | `rgba(255,255,255,0.07)` to `rgba(255,255,255,0.08)` | Card stroke |
| Card border hover | `rgba(26,183,89,0.3)` | Green highlight on hover |
| Page bg (audience pages) | `#0f1419` | Slightly warmer dark for for-saas, for-si, for-enterprises |
| Muted text | `#94a3b8` | Secondary text on audience pages |
| Heading font | `DM Sans` | Primary heading typeface |
| Body font | `Inter` | Paragraph / UI typeface |

**Global style direction:** Dark background, clean/minimal tech aesthetic, thin lines, subtle gradients, green (#1ab759) as the sole accent color. No orange in new graphics. Consistent with SaaS B2B enterprise visual language. No emojis. No clip art. All graphics should feel premium and technical.

---

## CRITICAL PRIORITY: Visible Placeholders on Live Pages

These are dashed-border placeholder boxes with descriptive labels that visitors can see right now on `platform/index.html`. Each one uses the `.screenshot-placeholder` class: a dashed border box (`1px dashed rgba(255,255,255,0.12)`), rounded corners (`12px`), 80px vertical padding, centered label text. The container is `.platform-container` at `max-width: 1100px`.

---

### Graphic 1: Unified Data Engine Diagram

- **Page:** `platform/index.html`
- **Section:** Section 2, "Built Different at the Core" (below the body text, above the proof-grid cards)
- **Placeholder label:** "Diagram: Multiple API formats (JSON, XML, CSV, SOAP) flowing into the unified APIANT Engine"
- **Type:** Technical diagram / flow illustration
- **Format:** SVG preferred, PNG acceptable
- **Dimensions:** 1052px wide (1100px container minus 48px padding), ~300px tall (the placeholder has 80px top/bottom padding)
- **Description:** Show four labeled input streams on the left (JSON, XML, CSV, SOAP), each represented as a distinct data format icon or labeled node. All four converge via flow lines into a central processing block labeled "APIANT Unified Engine" (or just the APIANT logo mark with a green glow). On the right side, a single clean output stream exits, representing normalized data. The visual should convey the concept of "many formats in, one consistent model out." The central engine should feel like the core, perhaps a hexagonal or circular shape with green accent.
- **Prompt suggestion:** "Technical diagram on a dark background (#0c0c0c). Four data format nodes on the left labeled JSON, XML, CSV, and SOAP, connected by thin glowing green (#1ab759) flow lines converging into a central hexagonal processing engine labeled 'Unified Engine' with a subtle green glow. A single output stream exits to the right. Clean, minimal B2B SaaS style. Thin lines, no gradients on nodes, dark card-style backgrounds on each node. No text besides labels. 1052x300px."
- **Style notes:** Dark background (#0c0c0c). Green (#1ab759) for flow lines and engine accent. Node backgrounds should use rgba(255,255,255,0.03) with rgba(255,255,255,0.07) borders. White text labels. No decorative elements.
- **Priority:** Critical

---

### Graphic 2: AI Co-Pilot Building a Connector

- **Page:** `platform/index.html`
- **Section:** Section 3, "The AI That Reads API Docs So You Don't Have To" (right column of the feature-row)
- **Placeholder label:** "Screenshot: AI Co-Pilot building an Asana connector in real time"
- **Type:** Screenshot mockup / UI illustration
- **Format:** PNG (screenshot-style renders better as PNG)
- **Dimensions:** ~526px wide (half of 1100px container minus 48px gap), aspect ratio approximately 4:3, so ~395px tall
- **Description:** A stylized mockup of the Assembly Editor interface. Show a dark-themed code/visual editor panel with an AI chat sidebar. The AI should be mid-conversation, with messages like "Reading Asana API documentation..." and "Building GET /tasks endpoint..." with green checkmarks next to completed steps. The main panel should show a partially built connector with labeled fields (endpoint URL, authentication method, response mapping). This should feel like a real product UI, not a diagram.
- **Prompt suggestion:** "Dark-themed software UI mockup of an AI-powered assembly editor. Left panel shows a chat interface with an AI assistant, messages reading 'Analyzing Asana API docs...' and 'Building GET /tasks endpoint' with green checkmarks. Right panel shows a visual connector builder with fields for endpoint URL, authentication, and response mapping. Dark background (#0c0c0c), green accent (#1ab759) on active elements, clean sans-serif typography (Inter font style). Rounded corners, subtle borders. Professional SaaS product screenshot aesthetic."
- **Style notes:** Dark UI matching site palette. Green (#1ab759) for checkmarks, progress indicators, active states. Card-style panels with rgba(255,255,255,0.03) backgrounds. No real product data that could be misleading.
- **Priority:** Critical

---

### Graphic 3: Multi-Step Automation with Conditional Branching

- **Page:** `platform/index.html`
- **Section:** Section 4, "Visual. Powerful. Production-Grade." (right column of the reverse feature-row, appears on left visually due to RTL)
- **Placeholder label:** "Screenshot: Multi-step automation with conditional branching"
- **Type:** Screenshot mockup / UI illustration
- **Format:** PNG
- **Dimensions:** ~526px wide x ~395px tall (same as Graphic 2, opposite side of a feature-row)
- **Description:** A stylized mockup of the Automation Editor. Show a visual flow/pipeline with connected steps: a trigger node ("New Class Booking"), followed by a conditional branch ("Custom Objects Enabled?"), with two paths (Yes/No) leading to different processing steps. Include error handling nodes and a final "Update CRM" step. The flow should move top-to-bottom or left-to-right. Each node should be a rounded rectangle with a type label and step name.
- **Prompt suggestion:** "Dark-themed visual automation editor UI mockup. A workflow pipeline flows left-to-right with connected nodes. Trigger node labeled 'New Class Booking' (green border), followed by a diamond conditional node 'Custom Objects?', branching into two paths: 'Yes' path with 'Create Custom Object' step, 'No' path with 'Update Contact' step, both converging to a final 'Sync to CRM' node. Connection lines are thin green (#1ab759). Nodes have dark backgrounds with subtle borders. An error handler node is connected below. Professional automation builder aesthetic on #0c0c0c background."
- **Style notes:** Node backgrounds rgba(255,255,255,0.04), green border on trigger/active nodes, white text labels, thin connection lines in green. Diamond shape for conditional branch.
- **Priority:** Critical

---

### Graphic 4: One Codebase, Multiple Deployments

- **Page:** `platform/index.html`
- **Section:** Section 5, "Build Once. Deploy to Hundreds." (below the callout block)
- **Placeholder label:** "Diagram: One codebase branching into multiple deployment configurations"
- **Type:** Architectural diagram
- **Format:** SVG preferred, PNG acceptable
- **Dimensions:** 1052px wide x ~300px tall (full-width within the container, same as Graphic 1)
- **Description:** A single source block on the left labeled "Master Codebase" (containing logic icons: conditional branch, loop, API call). From this block, multiple branching lines fan out to 4-6 smaller blocks on the right, each labeled as a different deployment: "Location A (EST, Custom Objects ON)", "Location B (PST, Custom Objects OFF)", "Location C (CST, Premium Tier)", etc. Each deployment block should have a small settings/gear icon to represent per-deployment configuration. A small "Deploy All" button indicator near the source block reinforces the one-click upgrade concept.
- **Prompt suggestion:** "Technical architecture diagram on dark background (#0c0c0c). A large rounded rectangle on the left labeled 'Master Codebase' with internal icons representing automation logic. Five thin green (#1ab759) branching lines fan out to the right, each connecting to a smaller card labeled as different deployment configurations: 'Location A - EST, Custom Objects ON', 'Location B - PST, Basic Tier', 'Location C - CST, Premium', etc. Each deployment card has a small gear icon. A green 'Deploy to All' button near the master block. Clean B2B SaaS diagramming style."
- **Style notes:** Same visual language as Graphic 1. Master block slightly larger and more prominent with green glow. Deployment blocks smaller, uniform styling.
- **Priority:** Critical

---

### Graphic 5: Data Search / Support Monitoring

- **Page:** `platform/index.html`
- **Section:** Section 6, "When Location 150 Says Something's Wrong" (right column of feature-row)
- **Placeholder label:** "Screenshot: Data search results showing a client ID's full journey through the automation"
- **Type:** Screenshot mockup / UI illustration
- **Format:** PNG
- **Dimensions:** ~526px wide x ~395px tall
- **Description:** A dark-themed search/monitoring UI. At the top, a search bar with a client ID or email entered. Below, a timeline or log view showing the data's journey: step 1 "Webhook Received" (timestamp), step 2 "Contact Matched" (with ID), step 3 "Membership Updated" (fields changed), step 4 "CRM Synced" (API response 200). Each step should have a green status dot and expandable detail. The overall feel should be "instant visibility into any piece of data."
- **Prompt suggestion:** "Dark-themed monitoring dashboard UI mockup. Search bar at top with 'client-12847' entered. Below, a vertical timeline showing data flow steps: 'Webhook Received 14:32:05' with green dot, 'Contact Matched: John D.' with green dot, 'Membership Status Updated' with green dot, 'HubSpot API: 200 OK' with green dot. Each step has an expandable arrow for details. Right sidebar shows summary: 'Total steps: 4, Duration: 1.2s, Errors: 0'. Dark background (#0c0c0c), green (#1ab759) status indicators, clean monospace timestamps."
- **Style notes:** Monitoring/observability aesthetic. Green success indicators. Monospace font for timestamps and IDs. White text on dark cards.
- **Priority:** Critical

---

### Graphic 6: FormApp Embedded in a SaaS Product

- **Page:** `platform/index.html`
- **Section:** Section 7, "Build Any UI. Embed It Anywhere." (right column of reverse feature-row)
- **Placeholder label:** "Mockup: A FormApp embedded inside a SaaS product's settings panel"
- **Type:** UI mockup (nested interface)
- **Format:** PNG
- **Dimensions:** ~526px wide x ~395px tall
- **Description:** A browser window frame showing a generic SaaS product (with a blurred/generic sidebar nav on the left). Inside the main content area, an embedded FormApp panel is visible, styled with a clean settings interface: toggles for "Sync Appointments" (on), "Custom Object Bookings" (on), "Two-way Contact Sync" (off), a dropdown for "Default Time Zone," and a "Save Settings" button. The FormApp should look native to the host product, not like a separate tool. A subtle "Powered by [hidden]" or no branding at all to reinforce the white-label concept.
- **Prompt suggestion:** "UI mockup of a SaaS product settings page with an embedded integration configuration panel. Browser window frame shows a generic SaaS app with a sidebar navigation (blurred/generic). The main content area contains an embedded FormApp with toggles: 'Sync Appointments' (green, ON), 'Custom Object Bookings' (green, ON), 'Two-way Contact Sync' (gray, OFF). A 'Default Time Zone' dropdown set to 'Eastern'. A green 'Save Settings' button at the bottom. The embedded panel looks native to the host app. Clean, professional UI. Dark theme optional (the host SaaS could be light-themed to show contrast)."
- **Style notes:** The FormApp itself should use green (#1ab759) for active toggles. The host SaaS product can use a neutral light or dark theme. The key message is "it looks native, not bolted on."
- **Priority:** Critical

---

### Graphic 7: AI Agent Orchestrating a Workflow

- **Page:** `platform/index.html`
- **Section:** Section 8, "Agents with Goals, Tools, and the Whole Platform Behind Them" (right column)
- **Placeholder label:** "Screenshot: AI Agent orchestrating a multi-step workflow"
- **Type:** Diagram / UI illustration
- **Format:** PNG
- **Dimensions:** ~526px wide x ~395px tall
- **Description:** An AI agent represented as a central brain/node with goal-oriented connections radiating outward. The agent has a "Goal: Resolve billing discrepancy" label. Connected to it are tool nodes: "Query Salesforce," "Check HubSpot timeline," "Pull invoice from QuickBooks," "Send Slack notification." Lines from the agent to each tool show data flow. A status panel shows the agent's reasoning steps. The composition should convey "autonomous agent with access to real tools, not just a chatbot."
- **Prompt suggestion:** "Technical diagram of an AI agent system on dark background (#0c0c0c). Central circular node labeled 'AI Agent' with a brain/neural icon and green (#1ab759) glow. A goal label reads 'Resolve billing discrepancy'. Four tool nodes orbit around it: 'Query Salesforce' (CRM icon), 'Check HubSpot' (timeline icon), 'Pull Invoice' (document icon), 'Send Slack Alert' (message icon). Green connection lines show data flow direction with arrows. A small reasoning panel in the corner shows numbered steps. Clean B2B tech illustration style."
- **Style notes:** Central agent should feel intelligent and autonomous. Tool nodes should look like platform capabilities, not external services. Green connections reinforce the platform theme.
- **Priority:** Critical

---

### Graphic 8: AI Chatbot Triggering Automation

- **Page:** `platform/index.html`
- **Section:** Section 9, "A Chat. One Trigger. One Action." (right column of reverse feature-row)
- **Placeholder label:** "Screenshot: Chat interaction triggering automation behind the scenes"
- **Type:** Split illustration (chat UI + automation flow)
- **Format:** PNG
- **Dimensions:** ~526px wide x ~395px tall
- **Description:** Left side shows a chat interface with a user message ("What's the membership status for client 12847?") and a bot response with structured data (name, status, next visit, sessions remaining). Right side (or below, connected by a subtle arrow) shows the behind-the-scenes automation: the chatbot trigger fires, queries Mindbody API, transforms data, and returns the formatted response. The two halves should be visually connected to show the chat is backed by real automation, not a canned response.
- **Prompt suggestion:** "Split-view illustration on dark background (#0c0c0c). Left: chat interface mockup with user message 'What is the membership status for client 12847?' and bot response showing a formatted card with 'Name: Sarah M. | Status: Active | Next Visit: Thursday 2pm | Sessions: 3 remaining'. Right: a simplified automation flow showing 'Chat Trigger > Query API > Transform Data > Return Response' with green connection lines. A subtle connecting element bridges the chat and the automation. Clean, dark UI aesthetic with green (#1ab759) accents."
- **Style notes:** The chat UI should feel modern (rounded bubbles, dark theme). The automation flow should be simplified (not full editor, just conceptual). Green accents throughout.
- **Priority:** Critical

---

### Graphic 9: MCP Protocol Diagram

- **Page:** `platform/index.html`
- **Section:** Section 10, "Protocol-Level AI Connectivity" (right column)
- **Placeholder label:** "Diagram: AI models connecting to APIANT via MCP protocol"
- **Type:** Technical protocol diagram
- **Format:** SVG preferred, PNG acceptable
- **Dimensions:** ~526px wide x ~395px tall
- **Description:** On the left, show 3-4 AI model icons/blocks labeled "Claude," "GPT," "Custom LLM." In the center, a vertical bar or gateway labeled "MCP Protocol" acts as the standardized interface. On the right, the APIANT platform block with sub-labels: "500+ Connectors," "Automations," "Business Logic." Flow arrows go bidirectionally through the MCP layer. The key message: MCP is a standardized protocol layer, not a custom integration per AI model.
- **Prompt suggestion:** "Technical protocol diagram on dark background (#0c0c0c). Left side: three AI model blocks labeled 'Claude', 'GPT-4', 'Custom LLM' with subtle AI brain icons. Center: a vertical green (#1ab759) bar labeled 'MCP Protocol' acting as a gateway. Right side: APIANT platform block containing '500+ Connectors', 'Automations', 'Business Logic'. Bidirectional arrows flow through the MCP layer. Clean, minimal, standardized interface feel. Thin lines, dark node backgrounds, green accent for the protocol layer."
- **Style notes:** MCP layer should be the visual focal point with strong green presence. AI models on the left, APIANT on the right. Symmetrical, clean layout.
- **Priority:** Critical

---

### Graphic 10: Admin Console with Account Network

- **Page:** `platform/index.html`
- **Section:** Section 11, "Your Control Center" (right column of reverse feature-row)
- **Placeholder label:** "Screenshot: Admin Console showing account network with linked accounts and shared connections"
- **Type:** Screenshot mockup / UI illustration
- **Format:** PNG
- **Dimensions:** ~526px wide x ~395px tall
- **Description:** A dark-themed admin dashboard. Left sidebar with navigation items: "Accounts," "Connections," "Rate Limits," "Monitoring." Main area shows an account network view: a master account at the top with branching lines to child accounts below (Location 1, Location 2, Location 3, etc. up to "...228 total"). A panel on the right shows details for a selected account: connection status, feature toggles enabled, last sync time. A rate limit meter shows "185/10s - 62% utilized." The overall feel is "complete control over a large deployment."
- **Prompt suggestion:** "Dark-themed admin console UI mockup. Left sidebar navigation: Accounts, Connections, Rate Limits, Monitoring. Main area shows a tree view of accounts: 'Master Account' at top, branching to 'Location 1', 'Location 2', 'Location 3', and a '...225 more' indicator. Right detail panel shows 'Location 1' details: Status Active (green dot), Connections: HubSpot, Mindbody, Last Sync: 2 min ago. A horizontal rate limit bar shows '185/10s - 62% utilized' in green (#1ab759). Dark background (#0c0c0c), clean dashboard aesthetic."
- **Style notes:** Admin/dashboard UI. Green for healthy states, muted text for labels. Tree/hierarchy visual for account network.
- **Priority:** Critical

---

## CRITICAL PRIORITY: Homepage Placeholder

### Graphic 11: AI Co-Pilot Demo Video Placeholder

- **Page:** `index.html`
- **Section:** Section 4, "The AI That Reads API Docs So You Don't Have To" (left column of the platform-grid, 16:10 aspect ratio container)
- **Placeholder label:** "AI Co-Pilot Demo Video" (with a play button SVG icon)
- **Type:** Video thumbnail / cover image
- **Format:** PNG (will eventually be replaced by actual video)
- **Dimensions:** Container has `aspect-ratio: 16/10`, within a `1fr` column of a 2-column grid inside a `1200px` container with `60px` gap, so approximately 570px wide x 356px tall
- **Description:** A compelling video thumbnail/cover image showing the AI Co-Pilot in action. Should show a stylized view of the Assembly Editor with the AI building a connector, similar to Graphic 2 but composed as a thumbnail with a translucent play button overlay. The image should make visitors want to click play.
- **Prompt suggestion:** "Video thumbnail for an AI Co-Pilot demo. Dark-themed Assembly Editor UI showing an AI assistant building API connectors. A chat panel shows 'Building Asana connector...' with progress indicators. The main panel shows partially built API operations. A large translucent circular play button overlays the center. Subtle green (#1ab759) glow emanates from the AI chat area. Cinematic, professional SaaS product screenshot feel. Dark background, 570x356px, 16:10 aspect ratio."
- **Style notes:** Should feel cinematic and inviting. The play button overlay should be semi-transparent white with green accent. This image needs to be especially polished as it is on the homepage.
- **Priority:** Critical

---

## CRITICAL PRIORITY: FormApps Demo Placeholder

### Graphic 12: FormApps Interactive Demo Placeholder

- **Page:** `formapps.html`
- **Section:** Section 7, "Demo & Interactive Example" (`.fa-demo-block` with dashed border)
- **Placeholder label:** "Interactive Demo Coming Soon - A live, embedded FormApp example will be available here"
- **Type:** Screenshot mockup / placeholder illustration
- **Format:** PNG
- **Dimensions:** Full container width (1200px minus 80px padding = 1120px), with 80px vertical padding. Approximately 1120px wide x 400px tall
- **Description:** A preview/teaser of what the FormApp demo will look like. Show a realistic FormApp interface: an integration setup wizard with step indicators (Step 1: Connect, Step 2: Configure, Step 3: Activate). The current step shows a "Connect to HubSpot" OAuth flow with a green "Authorize" button and field mapping controls below. The FormApp should look embedded within a subtle browser frame to convey the "embeddable" nature.
- **Prompt suggestion:** "FormApp UI mockup showing an integration setup wizard. Step indicator at top: 'Connect' (active, green), 'Configure' (upcoming), 'Activate' (upcoming). Main area shows 'Connect to HubSpot' with an OAuth authorization button in green (#1ab759) and a preview of field mapping below: 'First Name > firstname', 'Email > email', 'Membership Type > custom_membership'. Clean, modern form UI on dark background (#0c0c0c). Embedded within a subtle browser frame. Professional SaaS configuration panel aesthetic. 1120x400px."
- **Style notes:** Should demonstrate the FormApp concept visually. Green (#1ab759) for active/primary elements. The wizard step pattern is key to convey the guided setup experience.
- **Priority:** Critical

---

## HIGH PRIORITY: Audience Page Hero Graphics

These pages are entirely text-based with no visual content beyond SVG icons and inline HTML. Adding a hero or section graphic to each would significantly improve engagement and visual credibility.

---

### Graphic 13: For SaaS Companies - Hero Illustration

- **Page:** `for-saas.html`
- **Section:** Hero section (centered, max-width 900px, padding-top 170px)
- **Type:** Conceptual illustration
- **Format:** SVG preferred, PNG acceptable
- **Dimensions:** 900px wide x 400px tall (to sit below hero text, above the divider)
- **Description:** An illustration of a SaaS product with integration capabilities embedded natively. Show a simplified SaaS application interface (dashboard-style) with an integration panel expanding from the sidebar. Inside the panel, multiple app logos connect via green lines to the SaaS core. The concept: "your product, with deep integrations baked in." Optionally show the "white-label" concept by having the APIANT layer invisible/ghosted behind the scenes.
- **Prompt suggestion:** "Conceptual illustration of a SaaS product with embedded integrations. A modern dashboard interface (dark theme) with a sidebar showing an 'Integrations' section expanded. Inside, multiple app connection cards (CRM, ERP, Scheduling icons) are connected via green (#1ab759) flow lines to the core product. Behind the interface, a subtle ghosted layer labeled 'APIANT Platform' shows the invisible infrastructure. Clean, minimal B2B SaaS illustration on dark background (#0f1419). Professional, not cartoonish."
- **Style notes:** Background should match `#0f1419` (the for-saas page bg). Green accent #1ab759. The illustration should reinforce "own your platform, white-label, invisible infrastructure."
- **Priority:** High

---

### Graphic 14: For SaaS Companies - How It Works Diagram

- **Page:** `for-saas.html`
- **Section:** Section 3, "How It Works" (4-step grid: `.fs-steps` with 4 columns)
- **Type:** Process flow diagram
- **Format:** SVG preferred
- **Dimensions:** 1120px wide (1200px container minus 80px padding) x 200px tall (to sit above or alongside the step cards)
- **Description:** A horizontal 4-step pipeline: "Assign a Workflow Architect" > "AI Co-Pilot Builds Connectors" > "Configure per Customer" > "Embed & Go Live". Each step connected by arrows. This reinforces the simplicity of the process visually.
- **Prompt suggestion:** "Horizontal 4-step pipeline diagram on dark background (#0f1419). Step 1: person icon, 'Assign Architect'. Step 2: AI brain icon with green glow, 'AI Builds Connectors'. Step 3: settings/gear icon, 'Configure per Customer'. Step 4: rocket/launch icon, 'Embed & Go Live'. Steps connected by green (#1ab759) arrows. Each step is a rounded card with an icon and label. Clean, minimal SaaS process flow."
- **Style notes:** Match the for-saas page styling. Green accents, dark background (#0f1419), card-style step boxes.
- **Priority:** High

---

### Graphic 15: For System Integrators - Flywheel Illustration

- **Page:** `for-si.html`
- **Section:** Section 3, "How SIs Build with APIANT - The Flywheel" (8-step grid: `.fs-flywheel`)
- **Type:** Circular flywheel diagram
- **Format:** SVG preferred
- **Dimensions:** 600px x 600px (centered, to replace or supplement the 8-step grid)
- **Description:** A circular flywheel showing the 8 steps in a continuous loop: Identify > Build > Separate > Package > Distribute > Support > Grow > Expand, with arrows connecting each step in a clockwise circle. The center should have "Recurring Revenue" as the core engine. The circular motion conveys the self-reinforcing nature of the business model.
- **Prompt suggestion:** "Circular flywheel diagram on dark background (#0f1419). Eight segments arranged clockwise: 'Identify', 'Build', 'Separate', 'Package', 'Distribute', 'Support', 'Grow', 'Expand'. Curved green (#1ab759) arrows connect each segment. Center of the wheel reads 'Recurring Revenue' with a subtle green glow. Each segment has a small icon and label. Professional B2B strategy diagram aesthetic. 600x600px."
- **Style notes:** Green (#1ab759) arrows and center accent. Segment backgrounds can use varying subtle transparencies. The flywheel should feel dynamic and self-reinforcing.
- **Priority:** High

---

### Graphic 16: For System Integrators - Revenue Growth Chart

- **Page:** `for-si.html`
- **Section:** Section 7, "The Revenue Math Is Simple" (`.fs-revenue-grid`)
- **Type:** Data visualization / chart illustration
- **Format:** SVG preferred, PNG acceptable
- **Dimensions:** 1120px wide x 300px tall
- **Description:** A simple ascending bar or area chart showing revenue growth as customer count increases. X-axis: customer count milestones (50, 100, 250, 500). Y-axis: annual recurring revenue ($59K, $118K, $297K, $594K). The bars/area should be green-filled. A subtitle line: "One product at $99/mo." The visual should make the revenue opportunity feel tangible and achievable.
- **Prompt suggestion:** "Ascending bar chart on dark background (#0f1419). Four green (#1ab759) bars growing from left to right. X-axis labels: '50 customers', '100 customers', '250 customers', '500 customers'. Y-axis labels show revenue: '$59K/yr', '$118K/yr', '$297K/yr', '$594K/yr'. A small label at the bottom: 'One product at $99/mo'. Clean, minimal data visualization. No grid lines, subtle axis labels in muted gray (#94a3b8)."
- **Style notes:** Green bars/gradient. Simple, readable. Not overly decorated. Should feel like a realistic revenue projection, not marketing hype.
- **Priority:** High

---

### Graphic 17: For Enterprises - Deep Integration Gap Diagram

- **Page:** `for-enterprises.html`
- **Section:** Section 2, "The Deep Integration Gap" (above the pain-point cards)
- **Type:** Conceptual comparison diagram
- **Format:** SVG preferred, PNG acceptable
- **Dimensions:** 1120px wide x 350px tall
- **Description:** A side-by-side comparison showing "Shallow Integration" vs "Deep Integration." Left side: a simplified sync showing one arrow between two apps with a single field label ("Contact Name"). Right side: a rich, multi-layered connection with multiple data flows (class bookings, appointments, memberships, client services, contracts), conditional logic nodes, error handling, and rate limiting indicators. The left should look incomplete and fragile; the right should look robust and comprehensive.
- **Prompt suggestion:** "Side-by-side comparison diagram on dark background (#0f1419). Left half labeled 'Shallow Integration' shows a single thin gray line between two app icons with one field synced. It looks sparse and fragile. Right half labeled 'Deep Integration' shows multiple green (#1ab759) data streams between two apps, with intermediate nodes for 'Logic', 'Error Handling', 'Rate Limiting', and labels for 5 data types: bookings, appointments, memberships, services, contracts. The right side looks robust and comprehensive. Clean B2B technical illustration."
- **Style notes:** Gray/muted tones for the "shallow" side. Green/vibrant for the "deep" side. The contrast should be immediately obvious.
- **Priority:** High

---

### Graphic 18: For Enterprises - Platform Architecture Overview

- **Page:** `for-enterprises.html`
- **Section:** Section 3, "One Platform. Every Department." (above the 4-step process grid)
- **Type:** Architecture diagram
- **Format:** SVG preferred
- **Dimensions:** 1120px wide x 400px tall
- **Description:** An enterprise architecture view showing the APIANT dedicated server at the center, with department connections radiating outward: Marketing (CRM), Operations (ERP), HR (HRIS), Finance (Billing), Sales (Pipeline). Each department connects through the central platform. An IT Admin overlay/shield icon shows governance and control. The concept: one platform serving every department with full IT visibility.
- **Prompt suggestion:** "Enterprise architecture diagram on dark background (#0f1419). Central block: 'APIANT Dedicated Server' with green (#1ab759) border and subtle glow. Five department nodes radiate outward: 'Marketing - CRM' (top-left), 'Operations - ERP' (top-right), 'HR - HRIS' (bottom-left), 'Finance - Billing' (bottom-right), 'Sales - Pipeline' (bottom-center). Green connection lines from each to center. An IT governance shield icon overlays the center block. Clean enterprise architecture diagram style."
- **Style notes:** Enterprise/corporate feel but still matching the dark APIANT aesthetic. Green connections, shield/governance iconography.
- **Priority:** High

---

## HIGH PRIORITY: Feature Page Visual Enhancements

These pages currently use only CSS-rendered visuals (boxes, SVG icons, styled divs) but no actual illustrations or screenshots.

---

### Graphic 19: AI Capabilities - Co-Pilot Visual

- **Page:** `ai.html`
- **Section:** Section 2, "Assembly Editor AI Co-Pilot" (the `.ai-copilot-visual` box, right column of the copilot card)
- **Current state:** A CSS-styled box with an SVG icon, text description, and bullet points. Min-height 280px.
- **Type:** Illustration / product screenshot mockup
- **Format:** PNG
- **Dimensions:** ~526px wide x 280px tall minimum (within the copilot card grid, `grid-template-columns: 1fr 1fr`)
- **Description:** Replace the CSS placeholder with a proper illustration of the AI Co-Pilot in action. Show a terminal-style or chat-style interface with the AI processing steps: "1. Reading API docs... done", "2. Building GET /contacts... done", "3. Testing against live API... done", "4. Self-correcting auth method... done." Green checkmarks on each step. A progress bar at the bottom showing "12 of 15 endpoints built." This should feel more real than the current icon + bullet points.
- **Prompt suggestion:** "AI Co-Pilot interface mockup on dark background. Terminal/chat style panel showing sequential processing steps with green (#1ab759) checkmarks: 'Reading API docs... done', 'Building GET /contacts... done', 'Testing live API... done', 'Self-correcting auth... done'. A progress bar at the bottom reads '12 of 15 endpoints built' with green fill. Dark card background rgba(0,0,0,0.3) with rounded corners (16px). Clean, technical, professional."
- **Style notes:** Matches the existing `.ai-copilot-visual` styling: bg rgba(0,0,0,0.3), border rgba(255,255,255,0.08), border-radius 16px.
- **Priority:** High

---

### Graphic 20: AI Capabilities - Agent Architecture Visual

- **Page:** `ai.html`
- **Section:** Section 3, "AI Agents That Operate Inside the Full Platform" (above or alongside the 3-card grid)
- **Type:** Architecture diagram
- **Format:** SVG preferred
- **Dimensions:** 1120px wide x 300px tall (full width above the card grid)
- **Description:** Show the agent architecture: an AI Agent in the center with two layers of access. Inner ring: Goals and reasoning engine. Outer ring: Tools (500+ connectors, automations, business logic, data queries). Arrows show the agent receiving a goal, reasoning about which tools to use, executing through the platform, and returning results. This conveys "agents with full platform access, not isolated chatbots."
- **Prompt suggestion:** "AI agent architecture diagram on dark background (#0c0c0c). Central circle: 'AI Agent' with a brain icon. Inner ring labeled 'Goals + Reasoning'. Outer ring divided into segments: '500+ Connectors', 'Automations', 'Business Logic', 'Data Queries'. Arrows show the flow: Goal In > Reasoning > Tool Selection > Execution > Results Out. Green (#1ab759) accent on the agent and connection arrows. Professional technical architecture style."
- **Style notes:** Concentric ring layout or hub-and-spoke. Green accent for the agent core. Muted tones for tools. Clean arrows.
- **Priority:** High

---

### Graphic 21: MCP Servers - Protocol Architecture

- **Page:** `mcp-servers.html`
- **Section:** Section 2, "What Are MCP Servers?" (below the text description, within `.mcp-container`, max-width 1200px)
- **Type:** Protocol architecture diagram
- **Format:** SVG preferred
- **Dimensions:** 1120px wide x 350px tall
- **Description:** A three-layer architecture showing AI Applications at the top, the MCP Protocol layer in the middle, and the APIANT Platform at the bottom. Top layer shows multiple AI app icons (chatbot, agent, LLM app). The middle MCP layer is a standardized bus/bar with "discover tools," "understand capabilities," "execute operations" labels. Bottom layer shows the APIANT platform with connectors, automations, and data. The MCP layer is the star of the diagram, representing the standardization concept.
- **Prompt suggestion:** "Three-layer protocol architecture diagram on dark background (#0f1419). Top layer: 3-4 AI application nodes (chatbot icon, agent icon, LLM icon). Middle layer: a horizontal green (#1ab759) bar labeled 'MCP Protocol' with sub-labels 'Discover Tools', 'Understand Capabilities', 'Execute Operations'. Bottom layer: APIANT platform block with internal elements '500+ Connectors', 'Automations', 'Business Logic'. Bidirectional arrows between each layer. The MCP layer is visually prominent. Clean technical architecture diagram."
- **Style notes:** MCP layer should be the visual anchor with strong green presence. Top and bottom layers in more muted tones. Professional protocol diagram aesthetic.
- **Priority:** High

---

### Graphic 22: FormApps - Settings-to-UI Pipeline Visual

- **Page:** `formapps.html`
- **Section:** Section 5, "The Settings-to-UI Pipeline" (supplement the existing CSS-rendered 3-step pipeline)
- **Type:** Conceptual illustration
- **Format:** PNG
- **Dimensions:** 1120px wide x 300px tall
- **Description:** A more visual representation of the settings-to-UI pipeline than the current CSS boxes. Show three connected panels: (1) Automation Editor with settings controls (checkboxes, dropdowns), (2) FormApp Builder with the same controls being arranged in a drag-and-drop interface, (3) End User view showing the finished, branded configuration panel. Arrows flow left to right. The key insight: the same settings that control automation logic are the ones users interact with.
- **Prompt suggestion:** "Three-panel pipeline illustration on dark background (#0c0c0c). Panel 1 'Automation Editor': shows settings controls (checkboxes, dropdowns) being defined. Panel 2 'FormApp Builder': the same controls are visible in a drag-and-drop canvas with branding options. Panel 3 'Your Product': the end user sees a clean, branded settings panel. Green (#1ab759) arrows connect the panels left-to-right. Each panel is a rounded card with subtle border. The same checkbox/toggle appears in all three panels to show continuity. Clean B2B SaaS illustration."
- **Style notes:** The visual continuity of the same settings flowing through all three stages is the core concept. Green accents for active elements, arrows connecting stages.
- **Priority:** High

---

## MEDIUM PRIORITY: Nice-to-Have Enhancements

These would improve pages that are already functional but would benefit from additional visual polish.

---

### Graphic 23: Homepage - Three Pillars Card Icons

- **Page:** `index.html`
- **Section:** Section 3, "Three Value Pillars" (three card grid: "Own Your Platform," "Build & Monetize," "Go Deep, Not Wide")
- **Current state:** Each card has an inline SVG icon (shield, trending-up arrow, server stack) at 24x24 within a 48x48 green-tinted container
- **Type:** Custom icon set
- **Format:** SVG
- **Dimensions:** 48px x 48px each (3 icons total)
- **Description:** Replace the generic SVG stroke icons with more distinctive, custom-designed icons that better represent each pillar: (1) "Own Your Platform" - a dedicated server with a padlock/shield, (2) "Build & Monetize" - building blocks stacking with a currency/recurring symbol, (3) "Go Deep, Not Wide" - depth layers (like a stack of transparent planes going deep, not spreading wide).
- **Prompt suggestion:** "Set of three 48x48 SVG icons on transparent background. Icon 1: dedicated server with shield overlay, representing platform ownership. Icon 2: stacking building blocks with a recurring revenue symbol, representing monetization. Icon 3: layered depth visualization (stacked transparent planes going downward), representing deep integration. All icons use green (#1ab759) line art, 2px stroke weight, rounded line caps. Clean, minimal, consistent style."
- **Style notes:** Consistent stroke weight and style across all three. Green (#1ab759) only. Transparent backgrounds (these sit on green-tinted containers).
- **Priority:** Medium

---

### Graphic 24: Homepage - Exercise Coach Case Study Visual

- **Page:** `index.html`
- **Section:** Section 5, "228 Locations. One Platform. Zero Errors." (stats section)
- **Type:** Infographic / data visualization
- **Format:** SVG preferred, PNG acceptable
- **Dimensions:** 1140px wide x 200px tall (to sit above or below the stats strip)
- **Description:** A simplified map or network diagram showing the Exercise Coach architecture: a master account hub in the center connected to 228 location nodes arranged in a radial pattern, all feeding into a single HubSpot endpoint on the right. Rate limiting indicator shows "185/10s" with a green healthy status. This makes the impressive scale visually tangible.
- **Prompt suggestion:** "Network diagram infographic on dark background (#0c0c0c). A central hub labeled 'Master Account' with green (#1ab759) glow. Approximately 20-30 small dots arranged in a radial pattern representing 228 locations (with '228' label). All dots connect to the hub. The hub connects via a thick green line to a 'HubSpot' endpoint on the right. A rate limit meter shows '185/10s' with green fill. Clean, minimal data visualization. Not a geographic map, but a network topology view."
- **Style notes:** The scale (228 dots) should be visually impressive without being cluttered. Use varying dot sizes or opacity to suggest scale. Green accent throughout.
- **Priority:** Medium

---

### Graphic 25: For SaaS - Comparison Table Header Visual

- **Page:** `for-saas.html`
- **Section:** Section 5, comparison table area (the page has a comparison table in `.fs-compare-table`)
- **Type:** Icon set for table headers
- **Format:** SVG
- **Dimensions:** 32px x 32px each (4 icons: APIANT, iPaaS, Zapier/Make, Build In-House)
- **Description:** Small distinctive icons for each column header of the comparison table: (1) APIANT - the green engine/platform icon, (2) iPaaS competitors - a generic cloud/platform icon in gray, (3) DIY tools - a simple zap/lightning bolt in gray, (4) Build in-house - a wrench/code icon in gray. APIANT icon should be green; competitors should be neutral gray.
- **Prompt suggestion:** "Four 32x32 SVG icons. Icon 1: APIANT platform icon in green (#1ab759), representing a dedicated integration engine. Icon 2: generic cloud platform icon in gray (#94a3b8), representing iPaaS competitors. Icon 3: lightning bolt icon in gray (#94a3b8), representing DIY automation tools. Icon 4: wrench/code icon in gray (#94a3b8), representing in-house build. Consistent style, 2px stroke, rounded caps."
- **Style notes:** Only APIANT icon gets the green treatment. Others are deliberately muted to show APIANT as the preferred choice.
- **Priority:** Medium

---

### Graphic 26: For Enterprises - Shadow IT Diagram

- **Page:** `for-enterprises.html`
- **Section:** Section 2, alongside the "Shadow IT Integration Debt" pain card
- **Type:** Conceptual illustration
- **Format:** SVG preferred
- **Dimensions:** 1120px wide x 250px tall (or card-sized at ~350px x 200px)
- **Description:** A "before and after" mini-diagram. Left ("Before APIANT"): scattered, disconnected integration lines between apps with red X marks showing errors, no central visibility, and a worried IT admin icon. Right ("After APIANT"): all connections route through a central APIANT hub with green checkmarks, monitoring dashboard visible, and a confident IT admin icon. Quick visual that conveys the governance story.
- **Prompt suggestion:** "Before/after comparison illustration on dark background (#0f1419). Left 'Before': five app icons connected by tangled gray dashed lines with red X marks at failure points. A small IT admin icon looks overwhelmed. Label: 'Shadow IT chaos'. Right 'After': same five app icons connected through a central green (#1ab759) hub (APIANT), clean straight lines, green checkmarks on each connection. A monitoring panel is visible. IT admin icon looks confident. Label: 'Centralized governance'. Clean B2B illustration style."
- **Style notes:** Red/warning on the "before" side, green/healthy on the "after" side. The contrast tells the governance story at a glance.
- **Priority:** Medium

---

### Graphic 27: AI Capabilities - Chatbot Flow Enhancement

- **Page:** `ai.html`
- **Section:** Section 4, "AI Chatbot" (currently has a CSS-rendered 5-column flow: `.ai-chatbot-flow`)
- **Current state:** Five CSS boxes with arrows: "User asks" > arrow > "Automation engine processes" > arrow > "Response returned"
- **Type:** Enhanced flow illustration
- **Format:** SVG or PNG
- **Dimensions:** 1120px wide x 250px tall
- **Description:** An enhanced version of the existing CSS flow that adds visual richness. Replace the plain boxes with illustrated panels: a chat bubble for the user input, a brain/gears icon for the automation processing (with sub-steps like "interpret intent," "query APIs," "transform data"), and a formatted response card for the output. The flow should feel dynamic and intelligent, not static.
- **Prompt suggestion:** "Horizontal chatbot flow diagram on dark background (#0c0c0c). Left: a chat bubble with 'What are my upcoming appointments?' Right-arrow to center: a processing engine block with three internal steps 'Interpret Intent', 'Query Mindbody API', 'Format Response' stacked vertically. Right-arrow to end: a formatted response card showing a clean list of appointments. Connection arrows in green (#1ab759). Each stage has a subtle icon. Clean, professional, SaaS illustration style."
- **Style notes:** Three distinct visual treatments for input (chat), processing (engine), output (formatted card). Green connections.
- **Priority:** Medium

---

### Graphic 28: FormApps - Use Case Icons

- **Page:** `formapps.html`
- **Section:** Section 4, "What Can You Build with FormApps?" (5 use case cards in `.fa-usecases-grid`)
- **Current state:** Each card has a 48x48 green-background icon container with generic SVG stroke icons
- **Type:** Custom icon set
- **Format:** SVG
- **Dimensions:** 48px x 48px each (5 icons)
- **Description:** Custom icons for each FormApp use case: (1) Integration Configuration Panels - a settings/slider panel icon, (2) CX Apps in Partner Platforms - an embedded/nested app icon, (3) AI-Powered Intake Forms - a form with sparkle/AI indicator, (4) Self-Service Portals - a user with toggle controls, (5) Internal Tools - a dashboard/wrench combination.
- **Prompt suggestion:** "Five 48x48 SVG icons for FormApp use cases. All use green (#1ab759) line art on transparent background, 2px stroke. Icon 1: settings panel with slider controls. Icon 2: nested app/window-in-window icon. Icon 3: form document with AI sparkle symbol. Icon 4: user silhouette with toggle switches. Icon 5: dashboard with wrench overlay. Consistent style, rounded line caps, minimal detail."
- **Style notes:** Consistent with existing icon style on the page. Green (#1ab759) stroke. These sit inside 48x48 containers with `rgba(26,183,89,0.12)` backgrounds.
- **Priority:** Medium

---

### Graphic 29: MCP Servers - AI Stack Relationship Diagram

- **Page:** `mcp-servers.html`
- **Section:** Section 4, "Part of the APIANT AI Stack" (currently has text + link buttons to other AI pages)
- **Type:** Stack/layer diagram
- **Format:** SVG preferred
- **Dimensions:** 1120px wide x 250px tall
- **Description:** A horizontal stack showing how MCP Servers fit into the broader APIANT AI ecosystem. Four connected blocks: "AI Co-Pilot (Creation Layer)" > "AI Agents (Execution Layer)" > "AI Chatbot (Interaction Layer)" > "MCP Servers (Protocol Layer)." The MCP Servers block should be highlighted as the current page's focus. Arrows show how they interconnect. The platform foundation sits beneath all four.
- **Prompt suggestion:** "Horizontal AI stack diagram on dark background (#0f1419). Four connected blocks in a row: 'AI Co-Pilot - Creation Layer', 'AI Agents - Execution Layer', 'AI Chatbot - Interaction Layer', 'MCP Servers - Protocol Layer' (highlighted with green #1ab759 border). A platform foundation bar runs beneath all four: 'APIANT Integration Platform'. Bidirectional arrows between adjacent blocks. MCP Servers block has green glow to indicate current page focus. Clean technical architecture diagram."
- **Style notes:** MCP block visually prominent (green border/glow). Other blocks in muted styling. Foundation bar anchors the whole stack.
- **Priority:** Medium

---

## Summary: Graphics by Priority

### Critical (12 graphics) - Visible placeholders visitors can see now
| # | Page | Description | Container Size |
|---|------|-------------|----------------|
| 1 | platform/index.html | Unified Data Engine diagram | 1052x300 |
| 2 | platform/index.html | AI Co-Pilot screenshot mockup | 526x395 |
| 3 | platform/index.html | Automation Editor screenshot mockup | 526x395 |
| 4 | platform/index.html | One codebase, multiple deployments diagram | 1052x300 |
| 5 | platform/index.html | Data search/monitoring screenshot mockup | 526x395 |
| 6 | platform/index.html | FormApp embedded in SaaS product mockup | 526x395 |
| 7 | platform/index.html | AI Agent orchestrating workflow | 526x395 |
| 8 | platform/index.html | AI Chatbot triggering automation | 526x395 |
| 9 | platform/index.html | MCP protocol diagram | 526x395 |
| 10 | platform/index.html | Admin Console screenshot mockup | 526x395 |
| 11 | index.html | AI Co-Pilot demo video thumbnail | 570x356 |
| 12 | formapps.html | FormApps interactive demo placeholder | 1120x400 |

### High (10 graphics) - Text-only pages needing visual enhancement
| # | Page | Description | Container Size |
|---|------|-------------|----------------|
| 13 | for-saas.html | Hero illustration | 900x400 |
| 14 | for-saas.html | How It Works process diagram | 1120x200 |
| 15 | for-si.html | Flywheel diagram | 600x600 |
| 16 | for-si.html | Revenue growth chart | 1120x300 |
| 17 | for-enterprises.html | Deep Integration Gap comparison | 1120x350 |
| 18 | for-enterprises.html | Platform architecture overview | 1120x400 |
| 19 | ai.html | Co-Pilot visual (replace CSS placeholder) | 526x280 |
| 20 | ai.html | Agent architecture visual | 1120x300 |
| 21 | mcp-servers.html | Protocol architecture diagram | 1120x350 |
| 22 | formapps.html | Settings-to-UI pipeline visual | 1120x300 |

### Medium (7 graphics) - Nice-to-have enhancements
| # | Page | Description | Size |
|---|------|-------------|------|
| 23 | index.html | Three Pillars card icons (3 icons) | 48x48 each |
| 24 | index.html | Exercise Coach network diagram | 1140x200 |
| 25 | for-saas.html | Comparison table header icons (4 icons) | 32x32 each |
| 26 | for-enterprises.html | Shadow IT before/after diagram | 1120x250 |
| 27 | ai.html | Chatbot flow enhancement | 1120x250 |
| 28 | formapps.html | Use case icons (5 icons) | 48x48 each |
| 29 | mcp-servers.html | AI Stack relationship diagram | 1120x250 |

---

## File Naming Convention

All generated graphics should be placed in `/images/` and follow this naming pattern:

```
platform-data-engine-diagram.svg        (or .png)
platform-ai-copilot-mockup.png
platform-automation-editor-mockup.png
platform-deploy-diagram.svg
platform-monitoring-mockup.png
platform-formapp-embed-mockup.png
platform-ai-agent-diagram.png
platform-chatbot-flow-mockup.png
platform-mcp-protocol-diagram.svg
platform-admin-console-mockup.png
homepage-copilot-video-thumb.png
formapps-demo-preview.png
for-saas-hero-illustration.svg
for-saas-how-it-works.svg
for-si-flywheel.svg
for-si-revenue-chart.svg
for-enterprises-integration-gap.svg
for-enterprises-architecture.svg
ai-copilot-visual.png
ai-agent-architecture.svg
mcp-protocol-architecture.svg
formapps-pipeline-visual.png
homepage-pillar-icon-own.svg
homepage-pillar-icon-monetize.svg
homepage-pillar-icon-deep.svg
homepage-case-study-network.svg
for-saas-table-icon-apiant.svg
for-saas-table-icon-ipaas.svg
for-saas-table-icon-diy.svg
for-saas-table-icon-inhouse.svg
for-enterprises-shadow-it.svg
ai-chatbot-flow-enhanced.svg
formapps-usecase-icon-config.svg
formapps-usecase-icon-cx.svg
formapps-usecase-icon-ai-form.svg
formapps-usecase-icon-portal.svg
formapps-usecase-icon-tools.svg
mcp-ai-stack.svg
```

---

## Implementation Notes

1. **SVG vs PNG decision:** Use SVG for diagrams, flow charts, icons, and anything that should scale cleanly. Use PNG for UI mockups and screenshot-style illustrations where photorealistic detail matters.

2. **Retina/HiDPI:** For PNG graphics, generate at 2x the listed dimensions for retina displays. A 526x395 graphic should be rendered at 1052x790 and displayed at the smaller size via CSS.

3. **Dark background handling:** Most graphics can omit the background entirely (transparent) and rely on the page's dark background. For PNGs where a specific background matters, use the appropriate page background color listed in each spec.

4. **Replacing placeholders in HTML:** For the 10 platform/index.html placeholders, replace the `.screenshot-placeholder` div with an `<img>` tag using the same rounded corners (`border-radius: 12px`). For the homepage video placeholder, replace the entire `<div style="background: rgba(255,255,255,0.03); ..."` container.

5. **Accessibility:** All `<img>` tags must include descriptive `alt` text matching or paraphrasing the placeholder label text. Add `loading="lazy"` to all graphics below the fold.
