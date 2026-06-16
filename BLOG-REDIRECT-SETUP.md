# Retiring the old HubSpot blog (blog.apiant.com -> apiant.com/blog)

Permanently 301-redirects the legacy HubSpot blog to the new blog, preserving
slugs so each old post lands on its exact new URL and keeps its SEO equity.

**Important:** committing `blog-redirect.conf` to the repo does NOT activate
the redirect. The file must be installed on the Apache host and the domain
must be moved off HubSpot. The steps below require SSH access to the
apiant.com server (`52.37.38.181`) and Route 53 access.

## Current state

- `blog.apiant.com` is a Route 53 `CNAME` -> `5004658.group8.sites.hubspot.net` (HubSpot CMS).
- `apiant.com` is AWS Apache at `52.37.38.181` (also reverse-proxies marketing pages; see `APACHE-PROXY-SETUP.md`).
- New blog content parity is complete (all 14 old posts live at `apiant.com/blog/...`, videos carried over).

## What the redirect does (`blog-redirect.conf`)

| Old URL | New URL |
|---|---|
| `blog.apiant.com/en/<slug>` | `https://apiant.com/blog/posts/<slug>/` |
| `blog.apiant.com/en/tag\|author\|page/*` | `https://apiant.com/blog/` |
| anything else (incl. `/`, draft UUID URLs) | `https://apiant.com/blog/` |

## Steps

1. **Issue a TLS cert for blog.apiant.com.** Zero-downtime via DNS challenge:
   ```
   sudo certbot certonly --dns-route53 -d blog.apiant.com
   ```
   (or, with a brief gap, repoint DNS first then `sudo certbot --apache -d blog.apiant.com`)

2. **Install the vhost** on `52.37.38.181`:
   ```
   sudo cp blog-redirect.conf /etc/httpd/conf.d/      # RHEL/Amazon Linux
   # or /etc/apache2/conf-available/ + a2enconf on Debian/Ubuntu
   sudo apachectl configtest && sudo systemctl reload httpd
   ```

3. **Repoint DNS in Route 53:** change the `blog.apiant.com` record from the
   HubSpot CNAME to this server, an `A` record to `52.37.38.181`
   (or `CNAME` -> `apiant.com`).

4. **Verify:**
   ```
   curl -sI https://blog.apiant.com/en/copy-paste-multiple-actions-between-automations-apiant
   # expect: HTTP/1.1 301 ... Location: https://apiant.com/blog/posts/copy-paste-multiple-actions-between-automations-apiant/
   curl -sI https://blog.apiant.com/en/tag/hubspot   # -> 301 to https://apiant.com/blog/
   ```

5. **Disconnect the domain in HubSpot** (Settings -> Domains & URLs) and cancel
   the CMS subscription once redirects are confirmed live.

## Pre-flight check

Confirm ports 80/443 on the Apache host accept `blog.apiant.com` (security
groups / firewall) before cutover, otherwise certbot's challenge and the
redirect will fail.

## Alternative (no DNS work, keeps HubSpot)

Import `docs/seo/blog-redirects.csv` into HubSpot (Settings -> Content -> URL
Redirects) and add flexible catch-alls for `/en/tag/*`, `/en/author/*`,
`/en/page/*`, and `blog.apiant.com/*` -> `https://apiant.com/blog/`. Same-day
SEO fix, but the redirects stay on HubSpot and must be redone server-side at
cutover.
