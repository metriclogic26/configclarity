#!/usr/bin/env python3
"""
Fix titles and descriptions on high-impression low-CTR pages.
Run from: ~/Projects/CronSight/
"""
import re

FIXES = {
    "providers/contabo/firewall-setup/index.html": {
        "old_title": "Contabo Firewall Setup Guide — ConfigClarity",
        "new_title": "Contabo UFW Firewall Setup: Docker + IPv6 — ConfigClarity",
        "new_desc": "UFW setup on Contabo VPS: default-deny rules, Docker UFW bypass fix, and IPv6 protection. Copy-paste commands for Ubuntu 22.04.",
    },
    "providers/vultr/firewall-setup/index.html": {
        "old_title": "Vultr Firewall Setup Guide — ConfigClarity",
        "new_title": "Vultr UFW Firewall Setup: Docker + IPv6 — ConfigClarity",
        "new_desc": "UFW setup on Vultr: default-deny rules, Docker UFW bypass fix, and IPv6 protection. Copy-paste commands for Ubuntu 22.04.",
    },
    "fix/nginx/502-bad-gateway/index.html": {
        "old_title": "Fix: Nginx 502 Bad Gateway Error — ConfigClarity",
        "new_title": "Nginx 502 Bad Gateway: Exact Fix for Docker Upstreams — ConfigClarity",
        "new_desc": "Nginx 502 Bad Gateway fix — diagnose stopped containers, wrong upstream ports, and crashed services. Exact copy-paste Nginx config fix.",
    },
    "fix/nginx/upstream-timeout/index.html": {
        "old_title": "Fix: Nginx Upstream Timeout (504 Gateway Timeout) — ConfigClarity",
        "new_title": "Nginx 504 Timeout: Increase proxy_read_timeout — ConfigClarity",
        "new_desc": "Fix Nginx 504 Gateway Timeout by increasing proxy_read_timeout and proxy_connect_timeout. Exact location block config for slow upstreams.",
    },
}

if __name__ == "__main__":
    count = 0
    for filepath, fix in FIXES.items():
        with open(filepath, "r") as f:
            content = f.read()

        # Fix title
        content = content.replace(
            f'<title>{fix["old_title"]}</title>',
            f'<title>{fix["new_title"]}</title>'
        )

        # Fix description
        content = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{fix["new_desc"]}">',
            content,
            count=1
        )

        with open(filepath, "w") as f:
            f.write(content)

        # Verify
        with open(filepath) as f:
            check = f.read()
        title_ok = fix["new_title"] in check
        desc_ok = fix["new_desc"] in check
        print(f"  {'OK' if title_ok and desc_ok else 'FAIL'}  {filepath} title:{title_ok} desc:{desc_ok}")
        count += 1

    print(f"\nDone. {count} pages updated.")
