#!/usr/bin/env python3
"""
Add internal links to pages with 0-1 internal links.
Run from: ~/Projects/CronSight/
"""
import os

ADDITIONS = {
    # docker/network-host — 0 links
    "fix/docker/hardcoded-secrets/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/docker/network-host/">Docker network_mode: host risks</a> &nbsp;·&nbsp; <a href="/fix/docker/userland-proxy/">Docker userland-proxy explained</a></div>\n</footer>'
    ),
    "fix/docker/ufw-bypass/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/docker/network-host/">Docker network_mode: host</a> &nbsp;·&nbsp; <a href="/fix/docker/userland-proxy/">Docker userland-proxy</a></div>\n</footer>'
    ),
    "blog/docker-compose-security-checklist/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/docker/network-host/">network_mode: host risks</a> &nbsp;·&nbsp; <a href="/fix/docker/nvidia-gpu/">NVIDIA GPU Docker config</a> &nbsp;·&nbsp; <a href="/fix/docker/userland-proxy/">Docker userland-proxy</a></div>\n</footer>'
    ),
    # ssl/cdn-domain — 1 link
    "fix/ssl/expiry-monitoring/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/ssl/cdn-domain/">SSL on CDN-fronted domains</a> &nbsp;·&nbsp; <a href="/fix/ssl/200-day-warning/">Why monitor SSL at 200 days</a></div>\n</footer>'
    ),
    # ssl/traefik-renewal — 1 link
    "fix/proxy/traefik-v2-to-v3/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/ssl/traefik-renewal/">Traefik SSL renewal fix</a> &nbsp;·&nbsp; <a href="/fix/proxy/traefik-gateway-timeout/">Traefik gateway timeout fix</a></div>\n</footer>'
    ),
    # proxy low-link pages
    "fix/proxy/dangling-routes/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/proxy/caddy-tls-handshake-failed/">Caddy TLS handshake fix</a> &nbsp;·&nbsp; <a href="/fix/proxy/nginx-413-request-too-large/">Nginx 413 request too large</a> &nbsp;·&nbsp; <a href="/fix/proxy/traefik-no-route-found/">Traefik no route found</a></div>\n</footer>'
    ),
    "fix/proxy/traefik-v2-to-v3/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/proxy/traefik-gateway-timeout/">Traefik gateway timeout</a> &nbsp;·&nbsp; <a href="/fix/proxy/traefik-no-route-found/">Traefik no route found</a></div>\n</footer>'
    ),
}

SKIP_IF_CONTAINS = {
    "fix/docker/hardcoded-secrets/index.html": "network-host",
    "fix/docker/ufw-bypass/index.html": "userland-proxy",
    "blog/docker-compose-security-checklist/index.html": "network-host",
    "fix/ssl/expiry-monitoring/index.html": "cdn-domain",
    "fix/proxy/traefik-v2-to-v3/index.html": "traefik-renewal",
    "fix/proxy/dangling-routes/index.html": "caddy-tls",
}

count = 0
for fp, (old, new) in ADDITIONS.items():
    if not os.path.exists(fp):
        print(f"  SKIP {fp} — not found")
        continue
    with open(fp) as f:
        content = f.read()
    skip_check = SKIP_IF_CONTAINS.get(fp, "XXXXXXXXXXX")
    if skip_check in content:
        print(f"  SKIP {fp} — already has link")
        continue
    content = content.replace(old, new, 1)
    with open(fp, "w") as f:
        f.write(content)
    print(f"  OK   {fp}")
    count += 1

print(f"\nDone. {count} pages updated.")
