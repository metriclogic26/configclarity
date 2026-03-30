#!/usr/bin/env python3
"""
Add internal links to high-impression low-click pages.
Run from: ~/Projects/CronSight/
"""
import os

ADDITIONS = {
    "providers/hetzner/docker-firewall/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Also see: <a href="/providers/hetzner/ssl-setup/">Hetzner SSL setup guide</a> &nbsp;·&nbsp; <a href="/fix/ssl/expiry-monitoring/">SSL expiry monitoring</a></div>\n</footer>'
    ),
    "providers/hetzner/ufw-docker/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Also see: <a href="/providers/hetzner/ssl-setup/">Hetzner SSL setup</a> &nbsp;·&nbsp; <a href="/fix/ufw/docker-bypass/">UFW Docker bypass fix</a></div>\n</footer>'
    ),
    "fix/nginx/upstream-timeout/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/nginx/502-bad-gateway/">Nginx 502 Bad Gateway fix</a> &nbsp;·&nbsp; <a href="/glossary/dangling-route/">Dangling route</a></div>\n</footer>'
    ),
    "fix/proxy/dangling-routes/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/nginx/502-bad-gateway/">Nginx 502 Bad Gateway fix</a> &nbsp;·&nbsp; <a href="/fix/nginx/upstream-timeout/">Nginx upstream timeout fix</a></div>\n</footer>'
    ),
    "error/nginx-502-bad-gateway/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Fix guide: <a href="/fix/nginx/502-bad-gateway/">Nginx 502 Bad Gateway — exact fix</a></div>\n</footer>'
    ),
    "fix/ufw/docker-bypass/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/error/ufw-inactive-still-open/">UFW inactive but ports still open</a> &nbsp;·&nbsp; <a href="/fix/ufw/default-deny-missing/">Default deny missing fix</a></div>\n</footer>'
    ),
    "fix/ufw/port-exposed-after-docker/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/error/ufw-inactive-still-open/">UFW inactive but ports still open</a> &nbsp;·&nbsp; <a href="/glossary/docker-ufw-bypass/">Docker UFW bypass explained</a></div>\n</footer>'
    ),
}

count = 0
for filepath, (old, new) in ADDITIONS.items():
    if not os.path.exists(filepath):
        print(f"  SKIP {filepath} — not found")
        continue
    with open(filepath) as f:
        content = f.read()
    check = 'ufw-inactive-still-open' if 'ufw-inactive' in new else \
            'hetzner/ssl-setup' if 'hetzner/ssl-setup' in new else \
            '502-bad-gateway' if '502-bad-gateway' in new else \
            'ufw/docker-bypass' if 'ufw/docker-bypass' in new else ''
    if check and f'Also see' in content or (check and check in content and 'Related:' in content):
        print(f"  SKIP {filepath} — already has link")
        continue
    content = content.replace(old, new, 1)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"  OK   {filepath}")
    count += 1

print(f"\nDone. {count} pages updated.")
