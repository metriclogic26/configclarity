#!/usr/bin/env python3
"""
Add content depth section to fix/nftables/ubuntu-22/index.html
Targets: "common nftables errors ubuntu 22.04"
Run from: ~/Projects/CronSight/
"""

NEW_SECTION = """
    <h2 style="font-size:1.1rem;font-weight:700;margin:2.5rem 0 0.75rem;color:var(--text);">Common nftables errors on Ubuntu 22.04</h2>

    <h3 style="font-size:0.95rem;font-weight:700;margin:1.5rem 0 0.5rem;color:var(--text);">Error: Could not process rule: No such file or directory</h3>
    <p style="font-size:0.875rem;color:var(--muted);margin-bottom:1rem;">This appears when nftables tries to load a ruleset that references a table or chain that doesn't exist yet. Usually caused by running <code style="background:#1e2130;padding:.1rem .4rem;border-radius:3px;font-size:.82rem;">nft -f /etc/nftables.conf</code> before the base tables are created.</p>
    <pre style="background:#0d0f1a;border:1px solid #2a2d3d;border-radius:8px;padding:1.25rem 1.5rem;font-size:0.78rem;overflow-x:auto;margin:1rem 0 1.5rem;line-height:1.7;color:var(--text);"># Fix: flush and reload from scratch
sudo nft flush ruleset
sudo systemctl restart nftables
sudo nft list ruleset</pre>

    <h3 style="font-size:0.95rem;font-weight:700;margin:1.5rem 0 0.5rem;color:var(--text);">Error: UFW rules not working after switching to nftables</h3>
    <p style="font-size:0.875rem;color:var(--muted);margin-bottom:1rem;">On Ubuntu 22.04, UFW uses nftables as its backend. If you previously had iptables rules, they won't carry over. Check which backend UFW is actually using:</p>
    <pre style="background:#0d0f1a;border:1px solid #2a2d3d;border-radius:8px;padding:1.25rem 1.5rem;font-size:0.78rem;overflow-x:auto;margin:1rem 0 1.5rem;line-height:1.7;color:var(--text);"># Check UFW backend:
sudo ufw status verbose
sudo nft list tables
# Look for: inet ufw6 — confirms UFW is using nftables

# If UFW rules are missing, reset and re-apply:
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable</pre>

    <h3 style="font-size:0.95rem;font-weight:700;margin:1.5rem 0 0.5rem;color:var(--text);">Error: Docker containers accessible despite UFW deny rules</h3>
    <p style="font-size:0.875rem;color:var(--muted);margin-bottom:1rem;">Docker uses iptables for container networking even on Ubuntu 22.04 where UFW uses nftables. The two systems don't interact — Docker's iptables rules bypass UFW's nftables rules entirely. This is not a UFW bug, it's an architectural conflict.</p>
    <pre style="background:#0d0f1a;border:1px solid #2a2d3d;border-radius:8px;padding:1.25rem 1.5rem;font-size:0.78rem;overflow-x:auto;margin:1rem 0 1.5rem;line-height:1.7;color:var(--text);"># Verify Docker is using iptables (even on nftables Ubuntu):
sudo iptables -L DOCKER --line-numbers

# The fix — bind container ports to localhost:
# In docker-compose.yml:
# ports:
#   - "127.0.0.1:8080:80"  # NOT "8080:80"</pre>

    <h3 style="font-size:0.95rem;font-weight:700;margin:1.5rem 0 0.5rem;color:var(--text);">Verify nftables is running correctly</h3>
    <pre style="background:#0d0f1a;border:1px solid #2a2d3d;border-radius:8px;padding:1.25rem 1.5rem;font-size:0.78rem;overflow-x:auto;margin:1rem 0 1.5rem;line-height:1.7;color:var(--text);"># Check service status:
sudo systemctl status nftables

# List all active rules:
sudo nft list ruleset

# Check UFW is using nftables backend:
sudo nft list tables | grep ufw

# Test a specific port is blocked:
sudo nft list ruleset | grep -A2 "drop|reject"</pre>

    <p style="font-size:0.875rem;color:var(--muted);margin-bottom:1rem;">Related: <a href="/fix/nftables/docker-conflict/" style="color:#6c63ff;">nftables and Docker conflict fix</a> &nbsp;·&nbsp; <a href="/blog/ufw-nftables-backend-ubuntu/" style="color:#6c63ff;">UFW nftables backend explained</a> &nbsp;·&nbsp; <a href="/fix/ufw/docker-bypass/" style="color:#6c63ff;">Docker UFW bypass fix</a></p>
"""

OLD = '    <div class="cta"><p>Use the Firewall Auditor to check your UFW/iptables rules on Ubuntu 22.</p><a href="/firewall/">Open Tool →</a></div>'
NEW = NEW_SECTION + '\n    <div class="cta"><p>Audit your UFW and nftables rules for Docker bypass risk and missing default-deny on Ubuntu 22.04.</p><a href="/firewall/">Open Firewall Auditor →</a></div>'

if __name__ == "__main__":
    with open("fix/nftables/ubuntu-22/index.html", "r") as f:
        content = f.read()

    if "Common nftables errors" in content:
        print("Already has content section — skipping")
    else:
        content = content.replace(OLD, NEW, 1)
        with open("fix/nftables/ubuntu-22/index.html", "w") as f:
            f.write(content)

        # Word count after
        import re
        text = re.sub(r'<[^>]+>', '', content)
        words = len(text.split())
        print(f"OK  fix/nftables/ubuntu-22/index.html ({words:,} words)")
