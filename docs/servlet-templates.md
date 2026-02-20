# Servlet Templates & SEO Pages

> How the APIANT backend generates dynamic SEO pages using `{TEMPLATE_*}` placeholders.

## Table of Contents

1. [Overview](#overview)
2. [Template Files](#template-files)
3. [Connect Template (Two-App)](#connect-template)
4. [Connections Template (Single-App)](#connections-template)
5. [Placeholder Reference](#placeholder-reference)
6. [How It Works](#how-it-works)
7. [Static Examples](#static-examples)
8. [Important Rules](#important-rules)

---

## Overview

The APIANT backend dynamically generates SEO landing pages for every app combination it supports. Instead of maintaining hundreds of static HTML files, two template files contain `{TEMPLATE_*}` placeholders that the backend replaces at serve time. This generates unique pages like:

- `apiant.com/connect/hubspot/salesforce` (two-app connect page)
- `apiant.com/connections/cliniko` (single-app connections page)

These URLs are served by the APIANT Java backend (servlet), not by the static file server.

## Template Files

| File | Purpose | URL Pattern |
|------|---------|-------------|
| `connect/servlettemplateconnect.html` | Two-app integration page | `/connect/{app1}/{app2}` |
| `connections/servlettemplateconnections.html` | Single-app integrations page | `/connections/{app}` |

Both files share the same head boilerplate, nav bar, and footer as regular pages.

## Connect Template

**File:** `connect/servlettemplateconnect.html`

Shows a page for connecting two specific apps, with triggers and actions for both.

### Page Structure

1. **Hero**: Logos of both apps with "Build API Apps with {FROM_APP} and {TO_APP}"
2. **Description section**: Brief overview of the integration
3. **Triggers and Actions grid**: Four sections showing available API endpoints
   - App 1 Triggers (with count)
   - App 1 Actions (with count)
   - App 2 Triggers (with count)
   - App 2 Actions (with count)
4. **CTA section**: "Start Building" button
5. **Standard footer**

### Placeholders Used

| Placeholder | Content |
|-------------|---------|
| `{TEMPLATE_FROM_APP}` | First app name (e.g., "HubSpot") |
| `{TEMPLATE_TO_APP}` | Second app name (e.g., "Salesforce") |
| `{TEMPLATE_FROM_ICON}` | First app icon URL |
| `{TEMPLATE_TO_ICON}` | Second app icon URL |
| `{TEMPLATE_APP_ICON}` | Used in a secondary context |
| `{TEMPLATE_APP1_TRIGGERS}` | HTML list of App 1 triggers |
| `{TEMPLATE_APP1_TRIGGERS_COUNT}` | Number of App 1 triggers |
| `{TEMPLATE_APP1_ACTIONS}` | HTML list of App 1 actions |
| `{TEMPLATE_APP1_ACTIONS_COUNT}` | Number of App 1 actions |
| `{TEMPLATE_APP2_TRIGGERS}` | HTML list of App 2 triggers |
| `{TEMPLATE_APP2_TRIGGERS_COUNT}` | Number of App 2 triggers |
| `{TEMPLATE_APP2_ACTIONS}` | HTML list of App 2 actions |
| `{TEMPLATE_APP2_ACTIONS_COUNT}` | Number of App 2 actions |

## Connections Template

**File:** `connections/servlettemplateconnections.html`

Shows a page for a single app's available integrations.

### Page Structure

1. **Hero**: App logo with "{APP_NAME}" heading
2. **Triggers and Actions**: Two sections showing available API endpoints
   - App Triggers (with count)
   - App Actions (with count)
3. **CTA section**
4. **Standard footer**

### Placeholders Used

| Placeholder | Content |
|-------------|---------|
| `{TEMPLATE_APP_NAME}` | App name (e.g., "Cliniko") |
| `{TEMPLATE_APP_ICON}` | App icon URL |
| `{TEMPLATE_APP_TRIGGERS}` | HTML list of triggers |
| `{TEMPLATE_APP_TRIGGERS_COUNT}` | Number of triggers |
| `{TEMPLATE_APP_ACTIONS}` | HTML list of actions |
| `{TEMPLATE_APP_ACTIONS_COUNT}` | Number of actions |

## Placeholder Reference

Complete list of all `{TEMPLATE_*}` placeholders used across both templates:

| Placeholder | Used In | Type |
|-------------|---------|------|
| `{TEMPLATE_FROM_APP}` | Connect | Text (app name) |
| `{TEMPLATE_TO_APP}` | Connect | Text (app name) |
| `{TEMPLATE_FROM_ICON}` | Connect | URL (icon image) |
| `{TEMPLATE_TO_ICON}` | Connect | URL (icon image) |
| `{TEMPLATE_APP_NAME}` | Connections | Text (app name) |
| `{TEMPLATE_APP_ICON}` | Both | URL (icon image) |
| `{TEMPLATE_APP1_TRIGGERS}` | Connect | HTML (list items) |
| `{TEMPLATE_APP1_TRIGGERS_COUNT}` | Connect | Number |
| `{TEMPLATE_APP1_ACTIONS}` | Connect | HTML (list items) |
| `{TEMPLATE_APP1_ACTIONS_COUNT}` | Connect | Number |
| `{TEMPLATE_APP2_TRIGGERS}` | Connect | HTML (list items) |
| `{TEMPLATE_APP2_TRIGGERS_COUNT}` | Connect | Number |
| `{TEMPLATE_APP2_ACTIONS}` | Connect | HTML (list items) |
| `{TEMPLATE_APP2_ACTIONS_COUNT}` | Connect | Number |
| `{TEMPLATE_APP_TRIGGERS}` | Connections | HTML (list items) |
| `{TEMPLATE_APP_TRIGGERS_COUNT}` | Connections | Number |
| `{TEMPLATE_APP_ACTIONS}` | Connections | HTML (list items) |
| `{TEMPLATE_APP_ACTIONS_COUNT}` | Connections | Number |

## How It Works

```
Browser requests: apiant.com/connect/hubspot/salesforce
                         |
                         v
APIANT Java servlet receives the request
                         |
                         v
Reads connect/servlettemplateconnect.html
                         |
                         v
Looks up "hubspot" and "salesforce" in its app database
                         |
                         v
Replaces all {TEMPLATE_*} placeholders with real data:
  - App names, icon URLs
  - HTML lists of triggers and actions
  - Counts
                         |
                         v
Returns the fully rendered HTML page
```

The backend has access to a database of all supported apps, their icons, and their available API triggers/actions. The template is filled at request time, so new apps are automatically supported without creating new HTML files.

## Static Examples

For development and testing, static versions of these pages exist:

| Static File | Template It Mirrors |
|-------------|-------------------|
| `connect/connect.html` | `servlettemplateconnect.html` (Cliniko + Stripe example) |
| `connections/connections.html` | `servlettemplateconnections.html` (Cliniko example) |

These static files have hardcoded content instead of `{TEMPLATE_*}` placeholders and can be opened directly in a browser.

## Important Rules

1. **Never change `{TEMPLATE_*}` placeholder syntax.** The APIANT backend does exact string replacement. Changing `{TEMPLATE_FROM_APP}` to `{{TEMPLATE_FROM_APP}}` or `{template_from_app}` will break all generated pages.

2. **Placeholder names are case-sensitive.** `{TEMPLATE_FROM_APP}` is not the same as `{template_from_app}`.

3. **Placeholders appear in multiple contexts.** The same placeholder appears in `<title>`, meta tags, heading text, alt attributes, and image src attributes. All occurrences must remain intact.

4. **HTML-type placeholders** (like `{TEMPLATE_APP1_TRIGGERS}`) inject raw HTML. The backend generates the HTML list markup. Do not wrap these in additional HTML tags that would break the generated structure.

5. **Test changes against both static examples.** After modifying a template, open the corresponding static example (`connect.html` or `connections.html`) to verify the layout still works with real content.

6. **Nav and footer must stay synchronized** with the rest of the site, just like any other page. See the [Site Maintenance Guide](./site-maintenance-guide.md).
