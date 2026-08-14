# Forms, Analytics & Integrations

> Form submission flows, webhook endpoints, third-party scripts, and tracking setup.

## Table of Contents

1. [Forms Overview](#forms-overview)
2. [Contact/Demo Form ("Start Building")](#contactdemo-form)
3. [White Paper Download Form](#white-paper-download-form)
4. [Product Page Forms (Next-Steps)](#product-page-forms)
5. [Calendly Scheduling Embeds](#calendly-scheduling-embeds)
6. [reCAPTCHA](#recaptcha)
7. [Google Analytics](#google-analytics)
8. [Smartlook Session Recording](#smartlook-session-recording)
9. [HubSpot Tracking](#hubspot-tracking)
10. [APIANT Dynamic Script](#apiant-dynamic-script)
11. [External Scripts Summary](#external-scripts-summary)

---

## Forms Overview

The site has three types of forms, all submitted via jQuery AJAX to APIANT webhook endpoints:

| Form | ID | Webhook | Pages |
|------|-----|---------|-------|
| Contact/Demo | `start-building` | `e68fef48...30835da4...` | Most main pages |
| White Paper | `white-paper` | `a09f77e9...6bfabf28...` | Most main pages |
| Product-specific | Varies per product | Varies | Next-steps pages, product pages |

All forms use Webflow's form markup (`w-form` classes) with custom jQuery submit handlers that override the default Webflow form submission.

## Contact/Demo Form

**Form ID:** `start-building`
**Webhook:** `https://apiant.com/webhook/e68fef48cd714da480f372762771d8c6_30835da4cc274ef28b6034ae43a00b26`

### Qualification Popup Webhook Payload (current)

The "Talk to Us" popup posts its contact step to the webhook above via jQuery
AJAX (`$.ajax`, form-url-encoded). The handler lives in the inline popup script
on every popup page. Payload keys, ready for the sales@apiant.com automation to
map into HubSpot contact properties:

| Key | Example | Suggested HubSpot property |
|-----|---------|----------------------------|
| `WorkEmail` | `jane@acme.com` | `email` |
| `Mobile` | `+14155550123` (E.164) | `mobilephone` |
| `Company` | `Acme Inc` | `company` |
| `CompanyDomain` | `acme.com` | `website` |
| `CompanyType` | `saas` / `si` / `enterprise` | (custom) |
| `CompanyTypeLabel` | `SaaS Company` / `System Integrator` / `Enterprise` | (custom) |
| `IntegrationNeeds` | free text | note / custom |
| `PageTitle` | page `document.title` | lead source detail |

`CompanyType` / `CompanyTypeLabel` come from the first card the visitor picks
(SaaS / System Integrator / Enterprise). `Mobile` is captured with the
intl-tel-input country selector (flag + dial code) and normalized to E.164
(`+` country code + national digits). The same lead is also saved to Supabase
`submit-lead` for the WhatsApp handoff; that path does not include the phone.

> The table below documents the **legacy** pre-2026 contact form and no longer
> reflects the live popup.

### Fields

| Field | Element ID | Type | Required |
|-------|-----------|------|----------|
| Page Title | (automatic) | Hidden (from `document.title`) | Yes |
| First Name | `FirstName` | Text | Yes |
| Last Name | `LastName` | Text | Yes |
| Work Email | `WorkEmail` | Email | Yes |
| Mobile | `Mobile` | Tel | No |
| Company | `Company` | Text | Yes |
| Country | `country` | Select | Yes |
| Company Type | `company_type-1` | Select (saas/si/enterprise) | Yes |
| Integration Needs | `IntegrationNeeds` | Textarea | No |
| reCAPTCHA | (widget) | reCAPTCHA v2 | Yes |

### Company Type Descriptions

The Company Type dropdown dynamically shows a description below it:

| Value | Description |
|-------|-------------|
| `saas` | "You offer a software platform and need seamless, deeply embedded integrations..." |
| `si` | "You're an expert at crafting custom integrations for clients..." |
| `enterprise` | "You require secure, tailored integrations to streamline operations..." |

This is handled by inline JavaScript using `setupDropdown()` which binds to both the dropdown `change` event and optional button clicks (`select-saas`, `select-si`, `select-enterprise`).

### Form Title Customization

The form popup title changes based on which CTA button opened it:

| Button ID | Form Title |
|-----------|------------|
| `btn-apiapps` | "Start Building API Apps" |
| `btn-sales` | "Talk to Sales" |
| `btn-whitepaper` | "Download White Paper" |

### Submission Flow

```
User fills form + completes reCAPTCHA
         |
         v
jQuery submit handler fires
         |
         v
Checks grecaptcha.getResponse()
         |  (empty = alert + abort)
         v
$.ajax POST to APIANT webhook
         |
         v
On success: hide form, show success message
         |
         v
APIANT backend processes the lead
```

### Success/Error States

- **Success**: `$("#start-building").hide(); $("#start-building-form-success").show();`
- **Error**: Webflow's built-in `.w-form-fail` div shows "Oops! Something went wrong"
- **reCAPTCHA missing**: Browser alert "Please complete the reCAPTCHA before submitting."

## White Paper Download Form

**Form ID:** `white-paper`
**Webhook:** `https://apiant.com/webhook/a09f77e9c3464783852ca5c2a899ef1a_6bfabf2825da440585332741327d6f46`

Same fields as the contact form but with element IDs suffixed with `-2` (e.g., `FirstName-2`, `LastName-2`, `company_type-2`).

**Key difference:** The white paper form does NOT validate reCAPTCHA in its submit handler (reCAPTCHA widget is present but not checked programmatically).

### Submission Flow

```
User fills form
         |
         v
jQuery submit handler fires (no reCAPTCHA check)
         |
         v
$.ajax POST to APIANT webhook
         |
         v
On success: hide form, show success message
         |
         v
User receives white paper download
```

## Product Page Forms

Product pages (next-steps pages and some API App pages) have their own forms with product-specific webhooks:

| Page | Webhook |
|------|---------|
| `zoomconnect-nextsteps.html` | `a09f77e9...6bfabf28...` |
| Other next-steps pages | Similar pattern |

Product pages may also include Recurly billing integration and pricing sliders with their own JavaScript logic. **Do not modify pricing/billing JavaScript** without understanding the full flow.

## Calendly Scheduling Embeds

Scheduling URLs are **never hardcoded in page HTML**. In July 2026 the CRMConnect
discovery link was scraped from page source and used for repeated spam bookings
(the slug had already been rotated once, to `-apac2`, for the same reason).

How it works now:

1. Pages ship a placeholder instead of a `calendly-inline-widget` div:
   ```html
   <div class="calendly-lazy" data-calendly-event="crmconnect"
        data-calendly-params="hide_event_type_details=1&amp;hide_gdpr_banner=1&amp;a3=Mindbody and HubSpot"
        style="min-width:320px;height:100%;"></div>
   ```
2. `js/calendly-loader.js` (included before `</body>`) watches placeholders with
   an IntersectionObserver. When one becomes visible (demo popup opened, or
   scrolled into view), it fetches the base URL from the `get-calendly-url`
   Supabase edge function, appends `data-calendly-params`, and injects the
   Calendly widget via `Calendly.initInlineWidget`.
3. `get-calendly-url` requires a browser context (allowed Origin or Referer),
   rate-limits per IP (20/hour), and reads URLs from project secrets:

   | Event key | Secret |
   |-----------|--------|
   | `crmconnect` | `CALENDLY_URL_CRMCONNECT` |
   | `calendarconnect` | `CALENDLY_URL_CALENDARCONNECT` |
   | `zoomconnect-onboarding` | `CALENDLY_URL_ZOOMCONNECT_ONBOARDING` |
   | `shopconnect-onboarding` | `CALENDLY_URL_SHOPCONNECT_ONBOARDING` |

**Rotating a burned Calendly link** (after spam): edit the event type's URL slug
in Calendly, then update the secret; no site redeploy needed:

```bash
supabase secrets set CALENDLY_URL_CRMCONNECT='https://calendly.com/apiant_discovery/<new-slug>'
```

The `Talk to Us` popup's Calendly path is separate: it gets its URL from
`check-availability` (stored in the `admin_settings` table, editable in
`admin.html`).

**Blocked emails:** `submit-lead` silently drops submissions from addresses in
the `BLOCKED_EMAILS` secret (comma-separated, exact match after lowercasing).
The sender still sees a success response, like the honeypot path.

## reCAPTCHA

**Type:** Google reCAPTCHA v2 (checkbox)
**Site Key:** `6LdTIVkrAAAAAOYkqcvyOhFE7IfuXC-VAivaS6RY`

The reCAPTCHA script is loaded in the `<head>` of every page:
```html
<script src="https://www.google.com/recaptcha/api.js"></script>
```

The widget is rendered using Webflow's `w-form-formrecaptcha` class with the `data-sitekey` attribute:
```html
<div data-sitekey="6LdTIVkrAAAAAOYkqcvyOhFE7IfuXC-VAivaS6RY"
     class="w-form-formrecaptcha g-recaptcha"></div>
```

**Note:** Only the contact/demo form (`start-building`) programmatically validates the reCAPTCHA response. The white paper form relies on the widget being present but does not enforce it in JavaScript.

## Google Analytics

**Property ID:** `G-G902ZQ3PZZ`
**Type:** GA4 (Google Analytics 4)

Loaded on every page in the `<head>`:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G902ZQ3PZZ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-G902ZQ3PZZ');
</script>
```

No custom events are tracked beyond pageviews. Form submissions go to APIANT webhooks, not GA events.

## Smartlook Session Recording

**Project ID:** `61b74e67b734857ecfff330d0bf2543efa3e601e`

Loaded on most pages in the `<head>` after the page-specific `<style>` block:
```html
<script>
  window.smartlook||(function(d){
    var o=smartlook=function(){o.api.push(arguments)},h=d.getElementsByTagName('head')[0];
    var c=d.createElement('script');o.api=new Array();c.async=true;c.type='text/javascript';
    c.charset='utf-8';c.src='https://rec.smartlook.com/recorder.js';h.appendChild(c);
  })(document);
  smartlook('init', '61b74e67b734857ecfff330d0bf2543efa3e601e');
  smartlook('record', { forms: true, numbers: true, emails: true, ips: true });
</script>
```

**Recording settings:** Forms, numbers, emails, and IPs are all recorded (not masked). This is configured in the `smartlook('record', ...)` call.

## HubSpot Tracking

**Portal ID:** `5004658`

Loaded at the bottom of every page, just before the closing `</body>` tag:
```html
<script type="text/javascript" id="hs-script-loader" async defer
        src="https://js.hs-scripts.com/5004658.js"></script>
```

HubSpot tracks pageviews and identifies visitors. It does not handle form submissions (those go to APIANT webhooks).

**Chat widget disabled site-wide:** `js/cookie-consent.js` sets `window.hsConversationsSettings.loadImmediately = false` before injecting the HubSpot loader, so the conversations chat widget never appears on any page while pageview tracking and visitor identification keep working. To re-enable chat, remove that setting (and re-check the chatflow targeting in the HubSpot portal).

**Tracking coverage:** every page must include `/css/cookie-consent.css` in the head and `/js/cookie-consent.js` before `</body>`. Blog pages get both from `blog/_templates/_head.html` and `blog/_templates/_footer.html` (regenerated by `scripts/build_blog.py`). The `architecture-illustration*.html` files are headless HTML fragments, not pages, and carry no tracking.

## APIANT Dynamic Script

Loaded from the APIANT server at the bottom of every page:
```html
<script src="https://apiant.com/js/apiant_dynamic.js"></script>
```

This script manages the **Sign In / Dashboard** button state in the nav bar. It detects whether the visitor has an active APIANT session and toggles between:
- **"Sign In"** button (for unauthenticated visitors)
- **"Dashboard"** button (for authenticated users)

**Important:** As of Aug 2026 this file IS maintained in this repository (`js/apiant_dynamic.js`) and deployed by the website CI, overwriting the copy that previously lived only on the server. It used to force-load the HubSpot chat widget for signed-in APIANT users (identification token + `HubSpotConversations.widget.load()`); that block was removed when chat was retired. If a platform-side deploy ever ships its own copy of this file, it would silently reintroduce the chat for signed-in users, so the chat block should also be removed from wherever the platform sources it.

## External Scripts Summary

All external scripts loaded on the site, in order of loading:

| Script | Source | Purpose | Loaded In |
|--------|--------|---------|-----------|
| WebFont loader | Google | Font loading | `<head>` |
| reCAPTCHA | Google | Form spam protection | `<head>` |
| GA4 | Google | Analytics | `<head>` |
| Smartlook | Smartlook | Session recording | `<head>` |
| jQuery 3.5.1 | Cloudfront CDN | DOM manipulation, AJAX | Before `</body>` |
| `js/apiant.js` | Local | Webflow runtime | Before `</body>` |
| HubSpot | HubSpot | Visitor tracking | Before `</body>` |
| `apiant_dynamic.js` | apiant.com | Auth state for nav | Before `</body>` |
| Elfsight | Elfsight (on some pages) | Google Reviews widget | Inline |
| Termly | Termly (legal pages only) | Privacy/Cookie policy content | Inline |
