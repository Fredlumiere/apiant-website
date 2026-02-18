# API App Landing Page Redesign Playbook

Use this prompt with an AI assistant to redesign any APIANT API App product page. It combines the content strategy and technical implementation patterns proven on the Mindbody+HubSpot page.

---

## How to Use

1. Copy the prompt below
2. Replace every `{{PLACEHOLDER}}` with your product-specific values
3. Provide the AI assistant with the HTML file to modify
4. Review the output

---

## Placeholder Reference

| Placeholder | Example (Mindbody+HubSpot) | Description |
|---|---|---|
| `{{SOURCE_APP}}` | Mindbody | The primary data source app |
| `{{DEST_APP}}` | HubSpot | The destination/marketing app |
| `{{PRODUCT_NAME}}` | CRMConnect | The API App product name |
| `{{INDUSTRY}}` | wellness | The target industry (wellness, healthcare, nonprofit) |
| `{{INDUSTRY_BUSINESS_TYPE}}` | fitness, wellness, and beauty businesses | Full descriptor for the industry |
| `{{USER_ROLE}}` | marketing team | Who benefits from the integration |
| `{{SOURCE_DATA_TYPES}}` | clients, sales, services, and memberships | Key data types from the source app |
| `{{PAIN_POINT_1_TITLE}}` | Hours of Manual Data Entry |  |
| `{{PAIN_POINT_1_DESC}}` | Staff waste time copying client info between Mindbody and HubSpot instead of serving clients and growing your business. |  |
| `{{PAIN_POINT_2_TITLE}}` | Missed Renewals & Lapsed Members |  |
| `{{PAIN_POINT_2_DESC}}` | Without automated alerts, memberships expire and sessions run low with no one noticing until the client has already left. |  |
| `{{PAIN_POINT_3_TITLE}}` | Generic Emails That Don't Convert |  |
| `{{PAIN_POINT_3_DESC}}` | Without real client activity data in HubSpot, every email is a mass blast — no personalization, no segmentation, no results. |  |
| `{{STEP_2_DESC}}` | Choose what to sync. CRMConnect handles the data logic, deduplication, and mapping. | What the Configure step does |
| `{{STEP_3_DESC}}` | Build HubSpot workflows on rich, real-time client data. Automate what matters. | What the Grow/Use step does |
| `{{FEATURES}}` | (see Features section below) | Product-specific feature showcase items |
| `{{FEATURE_CHECKLIST}}` | (see Checklist section below) | All features as a flat list |
| `{{COMPARISON_FEATURES}}` | (see Comparison section below) | Rows for the vs. table |
| `{{BASE_PRICE}}` | $169/mo | Starting price |
| `{{PARTNER_BADGE_1_SRC}}` | ../../images/Mindbody_Most_Valuable_Partner.avif | Partner badge image path |
| `{{PARTNER_BADGE_1_ALT}}` | Mindbody Most Valuable Partner | Partner badge alt text |
| `{{PARTNER_BADGE_2_SRC}}` | ../../images/HubSpot-platinum-partner-p-500.avif | Partner badge image path |
| `{{PARTNER_BADGE_2_ALT}}` | HubSpot Platinum Partner | Partner badge alt text |
| `{{CUSTOMER_LOGOS}}` | (keep existing logos from the page) | Customer logo markup |
| `{{ELFSIGHT_WIDGET_ID}}` | d8708bea-47ed-4880-849f-e9cb6f109855 | Elfsight Google Reviews widget ID |
| `{{FAQ_ITEMS}}` | (keep existing FAQ from the page) | Product-specific FAQ |
| `{{FINAL_CTA_SUBTITLE}}` | Join hundreds of wellness businesses already using CRMConnect. |  |

---

## The Prompt

```
You are a B2B SaaS marketing expert AND a front-end developer specializing in integration products for small businesses. I need you to redesign this API App landing page following a proven playbook. The product is APIANT's {{SOURCE_APP}} + {{DEST_APP}} integration (called "{{PRODUCT_NAME}}").

The pricing may feel steep to small business owners who don't yet understand the value. The strategy: show them an interactive demo first, let the value sink in, then reveal pricing. By the time they see the price, it should feel like a no-brainer.

Read the full HTML file first. Understand the existing structure, CTA buttons, pricing section, forms, and webhook logic before touching anything.

=== CONTENT STRATEGY ===

The page flow should be reordered to:
Hero → Trusted-By Logos → Benefits (reframed as problems) → How It Works → Features (visual showcase) → Reviews → Comparison Table → Demo → Pricing (hidden until demo scroll) → FAQ → Final CTA → More API Apps

1. HERO SECTION
- Rewrite headline to be problem-aware, not aspirational. Example pattern: "Stop Losing [noun] Between {{SOURCE_APP}} and {{DEST_APP}}"
- Subheadline should frame the demo-first strategy: "Before you see pricing, see exactly what you're getting — and why hundreds of {{INDUSTRY}} businesses already rely on it."
- Replace any hard-sell CTAs with a single curiosity-driven button: "See It In Action →" linking to #Demo
- Add risk-reversal microcopy below: "2-minute interactive demo · No signup required"
- If the page has partner badges (e.g., MVP Partner, Platinum Partner), relocate them into the hero section, absolutely positioned on the left side of the hero image

2. TRUSTED-BY LOGOS
- Fix any duplicate wording (e.g., "businesses businesses")
- Wrap the logo container in a scrolling marquee using CSS animation (see technical section)
- Keep existing customer logos

3. BENEFITS → REFRAME AS PROBLEMS
- Replace the existing benefits section with exactly 3 problem cards
- Title should agitate the core pain: "Your {{SOURCE_APP}} Data Is Locked Away"
- Subtitle: "You have thousands of [clients/patients/donors] in {{SOURCE_APP}}. But without the right integration, your {{USER_ROLE}} can't use that data where it matters."
- Problem cards: {{PAIN_POINT_1}}, {{PAIN_POINT_2}}, {{PAIN_POINT_3}}
- Use emoji icons: ⏱ ⚠ ✉ (or appropriate alternatives)

4. NEW "HOW IT WORKS" SECTION
- Heading: "Live in 3 Steps. No Coding Required."
- 3 numbered step cards:
  1. Connect — "Link your {{SOURCE_APP}} and {{DEST_APP}} accounts in minutes. No developers needed."
  2. Configure — "{{STEP_2_DESC}}"
  3. Grow — "{{STEP_3_DESC}}"
- Follow with a mid-section CTA: "See It In Action →"

5. FEATURES SECTION
- Replace the old feature cards with an alternating image+text showcase (image left/right alternating)
- Each feature gets: screenshot image + heading + 1-2 sentence description
- Feature images should be clickable and open in a lightbox
- Add an expand icon overlay (bottom-right of each image) to indicate clickability
- After the showcase, add a mid-section CTA with risk-reversal text
- Then add a "Every Feature at a Glance" checklist grid (2 columns, green checkmarks)
- Hide the old feature cards with display:none (don't delete them)

6. REVIEWS SECTION
- Move below Features (was above in Webflow default)
- Remove any placeholder/dummy testimonials (e.g., "Emily Chen / DevOps Specialist")
- Keep the Elfsight Google Reviews widget

7. NEW COMPARISON TABLE
- Heading: "Why {{PRODUCT_NAME}} vs. DIY Integration Tools?"
- Subtitle: "Integrations aren't side-projects — they're critical infrastructure. {{PRODUCT_NAME}} is a turnkey, professionally-engineered solution built by experts with deep domain knowledge in {{SOURCE_APP}} and {{DEST_APP}}."
- 4-column grid: Feature | {{PRODUCT_NAME}} | Make/Zapier | Custom Dev
- Include rows for: Setup time, key differentiating features, maintenance, support, starting cost
- Highlight the {{PRODUCT_NAME}} column with a green tint

8. DEMO SECTION (placeholder for DemoMaker.ai)
- Bold headline: "Watch how it works in 2 minutes"
- Subtitle: "Most customers understand the ROI before the demo is even over."
- Embed container: <div id="demomaker-embed" style="width:100%; min-height:500px; margin: 32px 0;"></div>
- Transition text below: "Seen enough? Here's what it costs." with anchor button to #Pricing
- This transition element gets class "demo-transition" — it triggers the pricing reveal

9. PRICING SECTION
- Hide with style="display:none;" on the section div
- Replace single CTA with dual buttons: "Start Free Trial" (primary) + "Schedule a Demo" (secondary)
- Add risk-reversal: "No credit card required · Cancel anytime"
- Add trust callout above pricing: "Most customers see ROI within their first 30 days. No long-term contract required."
- Do NOT touch the pricing JavaScript logic, slider, add-on checkboxes, Recurly URLs, or webhook logic

10. NAVIGATION
- Remove "Pricing" from the nav (since it's hidden until demo scroll)
- Keep: Benefits, Reviews, Features, FAQ

11. FINAL CTA BANNER
- Dark gradient background (navy/charcoal)
- Heading: "Ready to Connect {{SOURCE_APP}} and {{DEST_APP}}?"
- Subtitle: "{{FINAL_CTA_SUBTITLE}}"
- "See It In Action →" button linking to #Demo
- Place before the "More API Apps" section

12. TONE
- Write all copy as a trusted advisor, not a salesperson
- Confident, clear, low-pressure
- The demo earns the sale — the copy just gets them to watch it

=== TECHNICAL IMPLEMENTATION ===

All custom styles go in a single <style> block in the <head>, after the existing Webflow/API Apps styles. All custom JS goes at the bottom of <body>, after the existing scripts.

IMPORTANT: Do not touch any of the following:
- Form logic and webhook URLs
- reCAPTCHA setup
- HubSpot tracking script
- Smartlook tracking
- Google Analytics
- Recurly billing URLs and pricing JavaScript
- data.js globalOverrides script
- Existing Webflow CSS classes (use new classes for all new elements)
- The "More API Apps" section at the bottom
- The demo/contact form modal

=== CSS COMPONENTS TO ADD ===

Paste the full CSS block below into the <style> tag. These are the proven, responsive components:

/* ===== PAGE REDESIGN CSS ===== */

/* Hero partner badges */
.hero-badges {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  position: absolute;
  top: 50%;
  left: 48px;
  transform: translateY(-50%);
  z-index: 2;
}
.hero-badges img {
  width: 90px;
  height: auto;
}

/* Dual CTA buttons */
.dual-cta {
  display: flex;
  gap: 16px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.btn-primary {
  font-family: var(--_fonts-spaces---paragraph-font);
  color: #fff;
  text-align: center;
  background: #1ab759;
  border: 2px solid #1ab759;
  border-radius: 10px;
  padding: 12px 28px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: background .2s, border-color .2s;
  display: inline-block;
}
.btn-primary:hover {
  background: #15a04d;
  border-color: #15a04d;
}
.btn-secondary {
  font-family: var(--_fonts-spaces---paragraph-font);
  color: var(--_white-mode---heading-color);
  text-align: center;
  background: transparent;
  border: 2px solid var(--_white-mode---heading-color);
  border-radius: 10px;
  padding: 12px 28px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: background .2s;
  display: inline-block;
}
.btn-secondary:hover {
  background: rgba(0,0,0,0.05);
}
.risk-reversal {
  text-align: center;
  font-size: 14px;
  color: #666;
  margin-top: 12px;
}

/* Problem section */
.problem-grid {
  display: flex;
  gap: 30px;
  justify-content: center;
  margin-top: 40px;
}
.problem-card {
  flex: 1;
  max-width: 340px;
  text-align: center;
  padding: 32px 24px;
  border: 1px solid var(--_white-mode---element-stroke-color);
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 2px 12px rgba(31,64,105,0.06);
}
.problem-icon {
  font-size: 40px;
  margin-bottom: 16px;
  display: block;
}
.problem-card h3 {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 10px;
  color: var(--_white-mode---heading-color);
}
.problem-card p {
  font-size: 15px;
  color: var(--_white-mode---paragraph-color);
  margin: 0;
  line-height: 1.5;
}

/* How It Works */
.steps-grid {
  display: flex;
  gap: 40px;
  justify-content: center;
  margin-top: 40px;
}
.step-card {
  flex: 1;
  max-width: 320px;
  text-align: center;
}
.step-number {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1ab759, #14a04d);
  color: #fff;
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}
.step-card h3 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--_white-mode---heading-color);
}
.step-card p {
  font-size: 16px;
  color: var(--_white-mode---paragraph-color);
  margin: 0;
  line-height: 1.5;
}

/* Alternating feature showcase */
.feature-showcase {
  display: flex;
  flex-direction: column;
  gap: 60px;
  margin-top: 50px;
}
.feature-row {
  display: flex;
  gap: 50px;
  align-items: center;
  max-width: 1050px;
  margin: 0 auto;
}
.feature-row.reversed {
  flex-direction: row-reverse;
}
.feature-row-image {
  flex: 1;
  min-width: 0;
}
.feature-row-image-inner {
  position: relative;
  display: inline-block;
  max-width: 480px;
}
.feature-row-image-inner::after {
  content: '';
  position: absolute;
  bottom: 14px;
  right: 14px;
  width: 34px;
  height: 34px;
  background: rgba(255,255,255,0.93) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M15 3l-4.5 4.5M3 15l4.5-4.5M9 3h6v6M9 15H3V9'/%3E%3C/svg%3E") center/18px no-repeat;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  pointer-events: none;
  opacity: 0.8;
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.feature-row-image-inner:hover::after {
  opacity: 1;
  transform: scale(1.1);
}
.feature-row-image img {
  display: block;
  width: 100%;
  border-radius: 12px;
  border: 2px solid var(--_white-mode---accent-color);
  box-shadow: 0 4px 20px rgba(31,64,105,0.1);
  cursor: pointer;
  transition: box-shadow 0.2s ease;
}
.feature-row-image img:hover {
  box-shadow: 0 6px 28px rgba(31,64,105,0.2);
}

/* Lightbox */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0,0,0,0);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: zoom-out;
  pointer-events: none;
  transition: background 0.35s ease;
}
.lightbox-overlay.active {
  background: rgba(0,0,0,0.85);
  pointer-events: auto;
}
.lightbox-overlay img {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 8px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.4);
  transform: scale(0.4);
  opacity: 0;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.3s ease;
}
.lightbox-overlay.active img {
  transform: scale(1);
  opacity: 1;
}
.lightbox-close {
  position: absolute;
  top: 20px;
  right: 28px;
  font-size: 36px;
  color: #fff;
  cursor: pointer;
  line-height: 1;
  font-weight: 300;
  opacity: 0;
  transition: opacity 0.3s ease 0.15s;
}
.lightbox-overlay.active .lightbox-close {
  opacity: 1;
}
.feature-row-text {
  flex: 1;
  min-width: 0;
}
.feature-row-text h3 {
  font-size: 26px;
  font-weight: 700;
  margin: 0 0 12px;
  color: var(--_white-mode---heading-color);
  line-height: 1.3;
}
.feature-row-text p {
  font-size: 16px;
  color: var(--_white-mode---paragraph-color);
  margin: 0;
  line-height: 1.6;
}

/* Feature checklist grid */
.checklist-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px 40px;
  max-width: 800px;
  margin: 40px auto 0;
}
.checklist-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  color: var(--_white-mode---heading-color);
  font-weight: 500;
}
.checklist-item::before {
  content: '';
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  background: #1ab759;
  border-radius: 50%;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
  background-size: 14px;
  background-position: center;
  background-repeat: no-repeat;
}

/* Comparison grid */
.comparison-wrapper {
  margin: 40px auto 0;
  overflow-x: auto;
  text-align: center;
}
.cmp-grid {
  display: inline-grid;
  grid-template-columns: auto auto auto auto;
  text-align: left;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  font-size: 15px;
}
.cmp-grid > div {
  padding: 14px 24px;
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}
.cmp-head {
  font-weight: 700;
  text-align: center;
  background: #f9fafb;
  border-bottom: 2px solid #d1d5db;
  padding: 16px 24px;
  color: var(--_white-mode---heading-color);
}
.cmp-head:not(:first-child) {
  border-left: 1px solid #e5e7eb;
}
.cmp-head.cmp-crm {
  background: rgba(26, 183, 89, 0.10);
  color: #1ab759;
  font-size: 16px;
}
.cmp-feat {
  font-weight: 500;
  color: var(--_white-mode---heading-color);
}
.cmp-val {
  text-align: center;
  border-left: 1px solid #e5e7eb;
  color: var(--_white-mode---paragraph-color);
}
.cmp-val.cmp-crm {
  background: rgba(26, 183, 89, 0.06);
}
.cmp-good { color: #1ab759; font-weight: 700; }
.cmp-bad { color: #dc2626; }
.cmp-dim { color: #9ca3af; }
.cmp-grid > div:nth-last-child(-n+4) {
  border-bottom: none;
}

/* Demo section */
.demo-section {
  text-align: center;
  padding: 80px 0 60px;
}
.demo-section h2 {
  font-size: 36px;
  font-weight: 700;
  color: var(--_white-mode---heading-color);
  margin: 0 0 12px;
}
.demo-section .demo-subtitle {
  font-size: 17px;
  color: var(--_white-mode---paragraph-color);
  margin: 0 0 32px;
  line-height: 1.5;
}
.demo-transition {
  margin-top: 40px;
  font-size: 17px;
  color: var(--_white-mode---paragraph-color);
}
.demo-transition a {
  display: inline-block;
  margin-top: 12px;
}

/* Trust callout */
.trust-callout {
  text-align: center;
  background: rgba(26, 183, 89, 0.08);
  border: 1px solid rgba(26, 183, 89, 0.2);
  border-radius: 12px;
  padding: 20px 32px;
  max-width: 640px;
  margin: 0 auto 40px;
  font-size: 16px;
  font-weight: 500;
  color: var(--_white-mode---heading-color);
  line-height: 1.5;
}

/* Final CTA banner */
.final-cta-section {
  background: linear-gradient(135deg, #14191f, #1e2a3a);
  padding: 80px 0;
  text-align: center;
}
.final-cta-section h2 {
  color: #fff;
  margin-top: 0;
}
.final-cta-section p {
  color: rgba(255,255,255,0.7);
  font-size: 18px;
  margin: 10px 0 30px;
}
.final-cta-section .btn-secondary {
  color: #fff;
  border-color: rgba(255,255,255,0.4);
}
.final-cta-section .btn-secondary:hover {
  background: rgba(255,255,255,0.1);
}

/* Mid-section CTA */
.mid-section-cta {
  text-align: center;
  padding: 40px 0;
}

/* ===== Scrolling logo marquee ===== */
@keyframes scrollLogos {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.company-logo-holder.customer-logos-holder {
  opacity: 1;
}
.logo-scroll-track {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: max-content;
  animation: scrollLogos 35s linear infinite;
  will-change: transform;
}
.logo-scroll-track:hover {
  animation-play-state: paused;
}
.company-logo-holder.customer-logos-holder .company-logo-container {
  gap: 60px;
  padding-right: 60px;
  align-items: center;
}
.company-logo-holder.customer-logos-holder .company-logo.customer-logo {
  max-height: 50px;
  opacity: 0.55;
  filter: grayscale(100%);
  transition: opacity 0.3s, filter 0.3s;
}
.company-logo-holder.customer-logos-holder .company-logo.customer-logo:hover {
  opacity: 1;
  filter: grayscale(0%);
}
.parnter-fade-holder .parnter-fade {
  z-index: 2;
}

/* Responsive */
@media screen and (max-width: 991px) {
  .hero-badges img {
    width: 70px;
  }
  .problem-grid {
    flex-wrap: wrap;
  }
  .problem-card {
    min-width: 250px;
  }
  .steps-grid {
    flex-wrap: wrap;
  }
  .step-card {
    min-width: 250px;
  }
}
@media screen and (max-width: 767px) {
  .hero-badges {
    gap: 8px;
    top: 12px;
    left: 12px;
  }
  .hero-badges img {
    width: 55px;
  }
  .problem-grid {
    flex-direction: column;
    align-items: center;
  }
  .problem-card {
    max-width: 100%;
    width: 100%;
  }
  .steps-grid {
    flex-direction: column;
    align-items: center;
  }
  .step-card {
    max-width: 100%;
  }
  .feature-row,
  .feature-row.reversed {
    flex-direction: column;
    gap: 24px;
  }
  .feature-row-image img {
    max-width: 100%;
  }
  .checklist-grid {
    grid-template-columns: 1fr;
  }
  .cmp-grid {
    font-size: 13px;
    border-radius: 8px;
  }
  .cmp-grid > div {
    padding: 10px 12px;
  }
  .final-cta-section {
    padding: 50px 20px;
  }
}

=== JAVASCRIPT TO ADD (bottom of <body>) ===

Add these two scripts at the bottom of <body>, after all existing scripts:

1. LIGHTBOX (for feature screenshots):
<!-- Lightbox -->
<div class="lightbox-overlay" id="lightbox">
  <span class="lightbox-close">&times;</span>
  <img src="" alt="">
</div>
<script>
(function() {
  var overlay = document.getElementById('lightbox');
  var lbImg = overlay.querySelector('img');
  function openLightbox(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt;
    requestAnimationFrame(function() {
      overlay.classList.add('active');
    });
  }
  function closeLightbox() {
    overlay.classList.remove('active');
    setTimeout(function() { lbImg.src = ''; }, 400);
  }
  document.querySelectorAll('.feature-row-image img').forEach(function(img) {
    img.addEventListener('click', function() {
      openLightbox(this.src, this.alt);
    });
  });
  overlay.addEventListener('click', closeLightbox);
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeLightbox();
  });
})();
</script>

2. PRICING REVEAL (progressive disclosure):
<script>
/* Reveal pricing when demo transition comes into view */
(function() {
  var pricing = document.getElementById('Pricing');
  var trigger = document.querySelector('.demo-transition');
  if (!pricing || !trigger) return;
  var observer = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting) {
      pricing.style.display = '';
      observer.disconnect();
    }
  }, { threshold: 0.5 });
  observer.observe(trigger);
})();
</script>

=== HTML STRUCTURE PATTERNS ===

Use these exact HTML patterns within the existing Webflow section/container structure:

HERO CTA PATTERN:
<div class="dual-cta">
  <a href="#Demo" class="btn-primary">See It In Action &rarr;</a>
</div>
<div class="risk-reversal">2-minute interactive demo &middot; No signup required</div>

HERO BADGES (inside .icons-holder, before the main hero image):
<div class="hero-badges">
  <img src="{{PARTNER_BADGE_1_SRC}}" loading="lazy" alt="{{PARTNER_BADGE_1_ALT}}">
  <img src="{{PARTNER_BADGE_2_SRC}}" loading="lazy" alt="{{PARTNER_BADGE_2_ALT}}">
</div>

SCROLLING MARQUEE (wrap both .company-logo-container divs):
<div class="logo-scroll-track">
  <div class="company-logo-container"><!-- ...existing logos... --></div>
  <div class="company-logo-container"><!-- ...duplicate logos for seamless loop... --></div>
</div>

PROBLEM CARDS:
<div class="problem-grid">
  <div class="problem-card">
    <span class="problem-icon">&#9201;</span>
    <h3>{{PAIN_POINT_1_TITLE}}</h3>
    <p>{{PAIN_POINT_1_DESC}}</p>
  </div>
  <div class="problem-card">
    <span class="problem-icon">&#9888;</span>
    <h3>{{PAIN_POINT_2_TITLE}}</h3>
    <p>{{PAIN_POINT_2_DESC}}</p>
  </div>
  <div class="problem-card">
    <span class="problem-icon">&#9993;</span>
    <h3>{{PAIN_POINT_3_TITLE}}</h3>
    <p>{{PAIN_POINT_3_DESC}}</p>
  </div>
</div>

STEPS:
<div class="steps-grid">
  <div class="step-card">
    <div class="step-number">1</div>
    <h3>Connect</h3>
    <p>Link your {{SOURCE_APP}} and {{DEST_APP}} accounts in minutes. No developers needed.</p>
  </div>
  <div class="step-card">
    <div class="step-number">2</div>
    <h3>Configure</h3>
    <p>{{STEP_2_DESC}}</p>
  </div>
  <div class="step-card">
    <div class="step-number">3</div>
    <h3>Grow</h3>
    <p>{{STEP_3_DESC}}</p>
  </div>
</div>

FEATURE ROW (alternate .feature-row and .feature-row.reversed):
<div class="feature-row">  <!-- or class="feature-row reversed" -->
  <div class="feature-row-image">
    <span class="feature-row-image-inner"><img src="{{IMAGE_SRC}}" loading="lazy" alt="{{FEATURE_TITLE}}" sizes="(max-width: 800px) 100vw, 800px" srcset="{{IMAGE_SRC_500}} 500w, {{IMAGE_SRC}} 800w"></span>
  </div>
  <div class="feature-row-text">
    <h3>{{FEATURE_TITLE}}</h3>
    <p>{{FEATURE_DESC}}</p>
  </div>
</div>

CHECKLIST:
<div class="checklist-grid">
  <div class="checklist-item">Feature Name</div>
  <!-- repeat for each feature -->
</div>

COMPARISON TABLE:
<div class="comparison-wrapper">
  <div class="cmp-grid">
    <div class="cmp-head"></div>
    <div class="cmp-head cmp-crm">{{PRODUCT_NAME}}</div>
    <div class="cmp-head">Make / Zapier</div>
    <div class="cmp-head">Custom Dev</div>

    <div class="cmp-feat">Setup time</div>
    <div class="cmp-val cmp-crm cmp-good">&lt; 30 min</div>
    <div class="cmp-val cmp-dim">Weeks</div>
    <div class="cmp-val cmp-dim">Months</div>
    <!-- repeat rows -->
  </div>
</div>

DEMO SECTION:
<div id="Demo" class="section">
  <div class="container">
    <div class="demo-section">
      <h2>Watch how it works in 2 minutes</h2>
      <p class="demo-subtitle">Most customers understand the ROI before the demo is even over.</p>
      <div id="demomaker-embed" style="width:100%; min-height:500px; margin: 32px 0;"></div>
      <div class="demo-transition">
        Seen enough? Here's what it costs.
        <a href="#Pricing" class="btn-primary">View Pricing &darr;</a>
      </div>
    </div>
  </div>
</div>

TRUST CALLOUT (placed just before the Pricing section):
<div class="trust-callout">
  Most customers see ROI within their first 30 days. No long-term contract required.
</div>

FINAL CTA BANNER:
<div class="final-cta-section">
  <div class="container">
    <div class="fade-in-on-scroll">
      <h2>Ready to Connect {{SOURCE_APP}} and {{DEST_APP}}?</h2>
      <p>{{FINAL_CTA_SUBTITLE}}</p>
      <div class="dual-cta">
        <a href="#Demo" class="btn-primary">See It In Action &rarr;</a>
      </div>
    </div>
  </div>
</div>

PRICING DUAL CTA (replaces single button inside existing pricing section):
<div class="dual-cta" style="margin-bottom: 12px;">
  <a href="#" class="btn-primary">Start Free Trial</a>
  <a data-w-id="033a9fd7-457e-abff-e217-71d4c84b3b37" href="#" class="btn-secondary">Schedule a Demo</a>
</div>
<div class="risk-reversal">No credit card required &middot; Cancel anytime</div>

=== PRESERVE EVERYTHING ELSE ===

Do not touch any form logic, webhook URLs, reCAPTCHA setup, HubSpot tracking, Smartlook, Google Analytics, Recurly billing, data.js globalOverrides, or existing Webflow CSS classes. Only modify CTA copy, section ordering, button anchor targets, and inject the new sections. The page must still function exactly as before.

Output the fully updated HTML file when done.
```

---

## Reference: Mindbody+HubSpot Implementation

The first page built with this playbook is:
`apipartners/mindbody/mindbody-hubspot-integration-and-automation-apiant.html`

Refer to it as a working reference for how each component looks in context.
