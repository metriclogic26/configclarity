#!/usr/bin/env python3
import re

FIXES = [
    (
        "fix/nftables/ubuntu-22/index.html",
        "Fix: nftables Setup on Ubuntu 22.04 — ConfigClarity",
        "UFW nftables Backend on Ubuntu 22.04 — Fix and Configuration Guide",
        "Ubuntu 22.04 uses nftables as the default UFW backend. How to configure UFW with nftables, fix Docker conflicts, and verify your firewall rules are working correctly.",
    ),
    (
        "providers/vultr/ssh-hardening/index.html",
        "Vultr SSH Hardening Guide — ConfigClarity",
        "Vultr SSH Hardening: Disable Password Auth on Ubuntu 22.04",
        "Harden SSH on Vultr VPS — disable password authentication, disable root login, set up fail2ban, and verify your sshd_config. Ubuntu 22.04 step-by-step guide.",
    ),
]

for filepath, old_title, new_title, new_desc in FIXES:
    with open(filepath, "r") as f:
        content = f.read()

    content = content.replace(
        "<title>" + old_title + "</title>",
        "<title>" + new_title + "</title>"
    )
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="' + new_desc + '">',
        content, count=1
    )
    with open(filepath, "w") as f:
        f.write(content)

    # Verify
    with open(filepath) as f:
        check = f.read()
    ok = new_title in check and new_desc in check
    print(f"  {'OK' if ok else 'FAIL'}  {filepath}")
