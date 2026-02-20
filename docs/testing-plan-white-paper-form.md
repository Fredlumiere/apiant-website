# White Paper Form Fix — User Testing Plan

**Date:** February 20, 2026
**Issue:** [GitHub #3](https://github.com/Fredlumiere/apiant-website/issues/3)
**Commit:** 8b91640
**Files changed:** 37

---

## What Was Fixed

| Bug | Before | After |
|-----|--------|-------|
| Email lost on submit | `name="Last-Name-4"` (duplicate of Last Name) | `name="Work-Email"` |
| Empty submissions allowed | No validation on any field | All 4 fields have `required` |
| Labels disconnected from inputs | `for="FirstName-3"` did not match `id="FirstName-2"` | `for="FirstName-2"` matches input |

---

## Test Script

Repeat the following 3 tests on each page listed below.

### Test 1: Required field validation

1. Open the White Paper popup (click the "Download White Paper" card in the footer)
2. Leave all fields empty
3. Click **DOWNLOAD**
4. **Expected:** Browser shows a validation error on the first empty field. Form does NOT submit.

### Test 2: Email value is captured correctly

1. Fill in all 4 fields with test data:
   - Name: `Test`
   - Last Name: `User`
   - Work Email: `test@example.com`
   - Mobile: `+1234567890`
2. Click **DOWNLOAD**
3. Check the webhook endpoint or backend to verify:
   - `Work-Email` field contains `test@example.com`
   - `Last-Name` field contains `User` (not overwritten by email)
4. **Expected:** All 4 values arrive correctly with no data loss.

### Test 3: Label-input association

1. Click the label text **"Name"** — cursor should jump into the Name input
2. Click the label text **"Last Name"** — cursor should jump into the Last Name input
3. Click the label text **"Work Email"** — cursor should jump into the Work Email input
4. Click the label text **"Mobile"** — cursor should jump into the Mobile input
5. **Expected:** Each label click focuses the correct input field.

---

## Pages to Test

### Priority 1 — High-traffic pages (run all 3 tests)

| # | Page | URL |
|---|------|-----|
| 1 | Homepage | `/index.html` |
| 2 | AI Capabilities | `/ai.html` |
| 3 | MCP Servers | `/mcp-servers.html` |
| 4 | FormApps | `/formapps.html` |
| 5 | Apps / Connectors | `/apps.html` |

### Priority 2 — Legal pages (run Test 1 + Test 2)

| # | Page | URL |
|---|------|-----|
| 6 | Privacy Policy | `/privacy.html` |
| 7 | Terms of Service | `/tos.html` |
| 8 | Cookie Policy | `/cookie-policy.html` |

### Priority 3 — API Partner hub pages (spot-check 1 per brand)

| # | Page | URL |
|---|------|-----|
| 9 | Mindbody Hub | `/apipartners/mindbody-turnkey-integration-solutions.html` |
| 10 | Cliniko Hub | `/apipartners/cliniko-turnkey-integration-solutions.html` |
| 11 | DonorPerfect Hub | `/apipartners/donorperfect-turnkey-integration-solutions.html` |

### Priority 4 — API Partner sub-pages (spot-check 1 per brand)

| # | Page | URL |
|---|------|-----|
| 12 | Mindbody + HubSpot | `/apipartners/mindbody/mindbody-hubspot-integration-and-automation-apiant.html` |
| 13 | Cliniko + Salesforce | `/apipartners/cliniko/cliniko-salesforce-integration-and-automation-apiant.html` |
| 14 | DonorPerfect + Mailchimp | `/apipartners/donorperfect/donorperfect-mailchimp-integration-and-automation-apiant.html` |

### Priority 5 — Next-steps and other pages (run Test 1 only)

| # | Page | URL |
|---|------|-----|
| 15 | AppConnect Next Steps | `/appconnect-next-steps.html` |
| 16 | ZoomConnect Next Steps | `/zoomconnect-nextsteps.html` |
| 17 | Connect | `/connect/connect.html` |
| 18 | Connections | `/connections/connections.html` |
| 19 | Backup / Pricing | `/backup/backup-with-extended-pricing.html` |

---

## Results Checklist

| Page                     | Required works | Email received | Labels click | Tester | Pass |
| ------------------------ | :------------: | :------------: | :----------: | ------ | :--: |
| index.html               |                |                |              |        |      |
| ai.html                  |                |                |              |        |      |
| mcp-servers.html         |                |                |              |        |      |
| formapps.html            |                |                |              |        |      |
| apps.html                |                |                |              |        |      |
| privacy.html             |                |                |              |        |      |
| tos.html                 |                |                |              |        |      |
| cookie-policy.html       |                |                |              |        |      |
| 1x Mindbody hub          |                |                |              |        |      |
| 1x Cliniko hub           |                |                |              |        |      |
| 1x DonorPerfect hub      |                |                |              |        |      |
| 1x Mindbody sub-page     |                |                |              |        |      |
| 1x Cliniko sub-page      |                |                |              |        |      |
| 1x DonorPerfect sub-page |                |                |              |        |      |
| 1x Next-steps page       |                |                |              |        |      |
| connect.html             |                |                |              |        |      |
| connections.html         |                |                |              |        |      |
| backup page              |                |                |              |        |      |

---

## Notes

- All 37 pages share the same White Paper form template. If Priority 1 pages all pass, the rest should be identical.
- The main contact form (Schedule a Demo popup on index.html, for-saas, for-si, for-enterprises) was NOT affected by this bug — it already had correct `name` attributes, `required` fields, and matching labels.
- The webhook endpoint receiving form data may need to be updated to expect `Work-Email` instead of `Last-Name-4` for the email field.
