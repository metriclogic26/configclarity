#!/usr/bin/env python3
import os

ADDITIONS = {
    "error/ufw-inactive-still-open/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/ufw/port-exposed-after-docker/">Port still exposed after Docker fix</a> &nbsp;·&nbsp; <a href="/fix/ufw/docker-bypass/">Docker UFW bypass fix</a></div>\n</footer>'
    ),
    "fix/nginx/ssl-redirect-missing/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/nginx/502-bad-gateway/">Nginx 502 Bad Gateway fix</a> &nbsp;·&nbsp; <a href="/fix/nginx/upstream-timeout/">Nginx 504 timeout fix</a></div>\n</footer>'
    ),
}

count = 0
for fp, (old, new) in ADDITIONS.items():
    if not os.path.exists(fp):
        print(f"  SKIP {fp} — not found")
        continue
    with open(fp) as f:
        content = f.read()
    if "port-exposed-after-docker" in content:
        print(f"  SKIP {fp} — already has link")
        continue
    if "ssl-redirect-missing" in content:
        print(f"  SKIP {fp} — already has link")
        continue
    content = content.replace(old, new, 1)
    with open(fp, "w") as f:
        f.write(content)
    print(f"  OK   {fp}")
    count += 1

print(f"\nDone. {count} pages updated.")
