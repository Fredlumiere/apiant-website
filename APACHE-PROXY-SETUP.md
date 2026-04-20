# Apache Reverse Proxy Setup: apiant.com -> Vercel

## What This Does

Routes 37 marketing pages from `apiant.com` to the new site hosted on `apiant-website.vercel.app`, using Apache as a transparent reverse proxy. Users always see `apiant.com` in the browser.

**What changes:** Homepage, audience pages, feature pages, platform pages, API partner pages, legal pages, pricing, and static assets (CSS/JS/images/videos/fonts).

**What does NOT change:** Everything else. The `/editor`, `/admin-console`, `/oauth`, `/api`, `/servlet`, `/jsp*`, `/dashboard`, `/login`, `/register`, servlet template pages, and any path not explicitly listed in the config remain on the origin server, completely untouched. This is a strict whitelist, not a catch-all.

## Files

- `apache-vercel-proxy.conf`: The Apache config to include in the VirtualHost.

## Prerequisites

- Apache 2.4+
- Modules: `mod_proxy`, `mod_proxy_http`, `mod_headers`, `mod_ssl`
- SSH access to the apiant.com server

## Implementation Steps

### 1. Enable Apache modules

```bash
# Debian/Ubuntu
sudo a2enmod proxy proxy_http headers ssl
sudo systemctl restart apache2

# RHEL/CentOS/Amazon Linux
# Verify these are uncommented in /etc/httpd/conf.modules.d/:
#   LoadModule proxy_module modules/mod_proxy.so
#   LoadModule proxy_http_module modules/mod_proxy_http.so
#   LoadModule headers_module modules/mod_headers.so
#   LoadModule ssl_module modules/mod_ssl.so
```

### 2. Upload the config file

```bash
# Copy to Apache config directory
sudo cp apache-vercel-proxy.conf /etc/apache2/conf-available/   # Debian/Ubuntu
# or
sudo cp apache-vercel-proxy.conf /etc/httpd/conf.d/             # RHEL/CentOS
```

### 3. Include in VirtualHost

Open the apiant.com VirtualHost config and add ONE line inside the `<VirtualHost>` block:

```apache
<VirtualHost *:443>
    ServerName apiant.com

    # ... existing config stays as-is ...

    Include /etc/apache2/conf-available/apache-vercel-proxy.conf

    # ... rest of existing config ...
</VirtualHost>
```

### 4. Test config syntax

```bash
sudo apachectl configtest
# Must show "Syntax OK" before proceeding
```

### 5. Reload Apache

```bash
sudo systemctl reload apache2    # Debian/Ubuntu
sudo systemctl reload httpd      # RHEL/CentOS
```

Use `reload` (not `restart`) to avoid dropping active connections.

### 6. Verify

```bash
# Proxied page (should return 200 with Vercel content)
curl -I https://apiant.com/pricing.html

# Non-proxied path (should still hit origin, unaffected)
curl -I https://apiant.com/editor
```

## Rollback

Remove or comment out the `Include` line from the VirtualHost, then reload:

```bash
sudo systemctl reload apache2
```

Instant revert. No DNS or OAuth impact.

## Homepage Root Path

If `apiant.com/` (without `index.html`) should also serve the Vercel homepage, add this inside the VirtualHost BEFORE the Include line:

```apache
RewriteEngine On
RewriteRule ^/?$ /index.html [PT]
```

Only add this if the origin server doesn't already have its own handler for `/`.

## Notes

- DNS is not changed. The domain stays pointed at the current server.
- OAuth redirect URIs remain valid since the domain is unchanged.
- The Vercel backend URL is defined once at the top of the config file (`VERCEL_BACKEND`). If the Vercel deployment URL changes, update it there.
- HTML pages are served with `no-cache` headers so updates on Vercel are reflected immediately.
- Static assets are cached for 24 hours.
