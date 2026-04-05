#!/usr/bin/env python3
import os

ADDITIONS = {
    "blog/ufw-nftables-backend-ubuntu/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Fix guide: <a href="/fix/nftables/ubuntu-22/">nftables setup on Ubuntu 22.04</a> &nbsp;·&nbsp; <a href="/fix/nftables/docker-conflict/">nftables Docker conflict</a></div>\n</footer>'
    ),
    "fix/ufw/docker-bypass/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Related: <a href="/fix/nftables/ubuntu-22/">nftables on Ubuntu 22.04</a> &nbsp;·&nbsp; <a href="/blog/ufw-nftables-backend-ubuntu/">UFW nftables backend explained</a></div>\n</footer>'
    ),
    "glossary/nftables/index.html": (
        "</footer>",
        '\n    <div style="max-width:760px;margin:0 auto;padding:0 2rem 1.5rem;font-size:0.82rem;color:var(--muted);">Setup guide: <a href="/fix/nftables/ubuntu-22/">nftables on Ubuntu 22.04</a> &nbsp;·&nbsp; <a href="/blog/ufw-nftables-backend-ubuntu/">UFW and nftables explained</a></div>\n</footer>'
    ),
}

count = 0
for filepath, (old, new) in ADDITIONS.items():
    if not os.path.exists(filepath):
        print(f"  SKIP {filepath} — not found")
        continue
    with open(filepath) as f:
        content = f.read()
    if "nftables/ubuntu-22" in content:
        print(f"  SKIP {filepath} — already has link")
        continue
    content = content.replace(old, new, 1)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"  OK   {filepath}")
    count += 1

print(f"\nDone. {count} pages updated.")
