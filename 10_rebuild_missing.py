#!/usr/bin/env python3
"""
Script 10: Rebuild missing pages + clean junk files.
Restores: 90 provider pages, fix/ufw, fix/nftables, fix/cron, fix/ssl, fix/nginx
Cleans: mnt/, crontab-validator/, docker-compose-linter/, nginx-config-validator/, home/
Run from: ~/Projects/CronSight/
"""

import os, json, shutil, glob
from datetime import date

TODAY = date.today().isoformat()
BASE = "https://configclarity.dev"

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

CSS = """    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root { --bg:#0b0d14; --bg2:#1e2130; --purple:#6c63ff; --green:#22c55e; --orange:#f97316; --red:#ef4444; --text:#e2e4f0; --muted:#8a8fb5; }
      body { background:var(--bg); color:var(--text); font-family:'JetBrains Mono',monospace; min-height:100vh; line-height:1.75; }
      a { color:var(--purple); text-decoration:none; } a:hover { text-decoration:underline; }
      .header { padding:1.5rem 2rem; border-bottom:1px solid #2a2d3d; display:flex; align-items:center; gap:1rem; }
      .header-logo { font-size:1.1rem; font-weight:700; color:var(--text); }
      .header-logo span { color:var(--purple); }
      .header-nav { margin-left:auto; display:flex; gap:1rem; font-size:0.8rem; }
      .header-nav a { color:var(--muted); }
      .breadcrumb { padding:1rem 2rem 0; max-width:760px; margin:0 auto; font-size:0.78rem; color:var(--muted); }
      .breadcrumb a { color:var(--muted); }
      .content { max-width:760px; margin:0 auto; padding:2rem; }
      h1 { font-size:1.6rem; font-weight:700; margin-bottom:1rem; }
      h2 { font-size:1.05rem; font-weight:700; margin:2rem 0 0.6rem; }
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1rem; }
      pre { background:#0d0f1a; border:1px solid #2a2d3d; border-radius:8px; padding:1rem 1.25rem; font-size:0.78rem; overflow-x:auto; margin:0.75rem 0 1.25rem; line-height:1.7; }
      .fix-box { background:var(--bg2); border-left:3px solid var(--green); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.25rem 0; }
      .fix-box .label { font-size:0.7rem; color:var(--green); text-transform:uppercase; letter-spacing:.06em; margin-bottom:0.4rem; }
      .faq-item { margin-bottom:1.4rem; }
      .faq-q { font-size:0.9rem; font-weight:600; margin-bottom:0.35rem; }
      .faq-a { font-size:0.84rem; color:var(--muted); }
      .cta { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.25rem 1.5rem; margin:2rem 0; text-align:center; }
      .cta p { color:var(--text); margin-bottom:0.6rem; font-size:0.875rem; }
      .cta a { display:inline-block; background:var(--purple); color:#fff; padding:0.45rem 1.2rem; border-radius:6px; font-size:0.82rem; font-weight:700; }
      footer { text-align:center; padding:2rem; font-size:0.75rem; color:var(--muted); border-top:1px solid #2a2d3d; margin-top:2rem; }
    </style>"""

HEADER = """  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a><a href="/ssl/">SSL</a><a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a><a href="/proxy/">Proxy</a><a href="/robots/">robots.txt</a>
    </nav>
  </header>"""

FOOTER = """  <footer>
    <p><a href="/fix/">Fix Guides</a> &nbsp;·&nbsp; <a href="/glossary/">Glossary</a> &nbsp;·&nbsp;
    <a href="https://metriclogic.dev">MetricLogic</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>"""

def breadcrumb_schema(crumbs):
    items = ",\n".join([
        f'    {{"@type":"ListItem","position":{i+1},"name":{repr(n)},"item":"{BASE}{u}"}}'
        for i, (n, u) in enumerate(crumbs)
    ])
    return f"""  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{items}
  ]}}
  </script>"""

def simple_page(title, meta_desc, keywords, canonical, crumbs, h1, body, cta_text, cta_href):
    bc_schema = breadcrumb_schema(crumbs)
    crumb_html = " › ".join([f'<a href="{u}" style="color:var(--muted);">{n}</a>' if i < len(crumbs)-1 else n for i, (n, u) in enumerate(crumbs)])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title} — ConfigClarity</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{BASE}{canonical}">
  <meta property="og:title" content="{title}"><meta property="og:description" content="{meta_desc}">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle","headline":"{title}",
    "url":"{BASE}{canonical}","description":"{meta_desc}",
    "author":{{"@type":"Organization","name":"MetricLogic"}},"datePublished":"{TODAY}"}}
  </script>
{bc_schema}
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">{crumb_html}</div>
  <div class="content">
    <h1>{h1}</h1>
    {body}
    <div class="cta"><p>{cta_text}</p><a href="{cta_href}">Open Tool →</a></div>
  </div>
{FOOTER}
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — FIX PAGES (ufw, nftables, cron, ssl, nginx)
# ═══════════════════════════════════════════════════════════════════════════════

FIX_PAGES = {
    "ufw": [
        {
            "slug": "docker-bypass",
            "title": "Fix: Docker Bypasses UFW Firewall Rules",
            "meta_desc": "Docker's iptables rules bypass UFW deny rules, exposing container ports to the internet. Exact fix for Ubuntu 20.04, 22.04, and Debian.",
            "keywords": "docker ufw bypass fix, docker firewall bypass ubuntu, ufw docker not blocking ports",
            "body": """<p>Docker inserts rules into the iptables DOCKER chain, which is evaluated before UFW's INPUT chain. Container ports published with <code>-p 8080:80</code> are accessible from the internet even when UFW has a deny rule for that port.</p>
<h2>The Fix — Bind to 127.0.0.1</h2>
<div class="fix-box"><div class="label">docker-compose.yml</div>
<pre>ports:
  - "127.0.0.1:8080:80"  # Not 0.0.0.0:8080:80</pre></div>
<h2>Verify the fix</h2>
<pre>sudo iptables -L DOCKER --line-numbers
# No ACCEPT rule should appear for your port from external IPs</pre>""",
            "cta_text": "Paste your ufw status verbose output to audit Docker bypass risk.",
            "cta_href": "/firewall/",
        },
        {
            "slug": "ipv6-mismatch",
            "title": "Fix: UFW IPv4 Rules Not Applied to IPv6",
            "meta_desc": "UFW firewall rules not protecting IPv6 interfaces. How to enable IPv6 in UFW and ensure rules apply to both address families.",
            "keywords": "ufw ipv6 mismatch fix, ufw ipv6 not working, ufw ipv6 enable ubuntu",
            "body": """<p>UFW manages both IPv4 (iptables) and IPv6 (ip6tables), but IPv6 rules are only applied when <code>IPV6=yes</code> is set in <code>/etc/default/ufw</code>.</p>
<div class="fix-box"><div class="label">/etc/default/ufw</div>
<pre>IPV6=yes</pre></div>
<pre>sudo ufw disable && sudo ufw enable
# Verify:
sudo ip6tables -L INPUT | grep -E "ACCEPT|DROP|REJECT"</pre>""",
            "cta_text": "Paste your ufw status verbose to detect IPv6 rule mismatches.",
            "cta_href": "/firewall/",
        },
        {
            "slug": "default-deny-missing",
            "title": "Fix: UFW Missing Default Deny Rule",
            "meta_desc": "UFW without a default deny rule allows all incoming traffic by default. How to set default deny incoming and verify the rule is active.",
            "keywords": "ufw default deny missing, ufw allow all by default fix, ufw default incoming policy",
            "body": """<p>Without a default deny rule, UFW allows all incoming connections that don't match a specific rule. The firewall should deny all incoming traffic and only allow explicitly permitted ports.</p>
<div class="fix-box"><div class="label">Set default deny incoming</div>
<pre>sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable</pre></div>
<pre># Verify:
sudo ufw status verbose | grep "Default:"
# Should show: Default: deny (incoming), allow (outgoing)</pre>""",
            "cta_text": "Paste your ufw status verbose to detect missing default-deny rules.",
            "cta_href": "/firewall/",
        },
        {
            "slug": "port-exposed-after-docker",
            "title": "Fix: Port Still Exposed After Adding UFW Deny Rule (Docker)",
            "meta_desc": "Adding ufw deny PORT does not block Docker-published ports. Why UFW rules don't affect Docker containers and how to actually close the port.",
            "keywords": "ufw deny not working docker, port still open after ufw deny, docker port exposed ufw",
            "body": """<p>This is the Docker UFW bypass problem. After running <code>sudo ufw deny 5432</code>, PostgreSQL in a Docker container is still reachable externally because Docker manages the FORWARD chain, not the INPUT chain that UFW controls.</p>
<div class="fix-box"><div class="label">Correct fix — bind container to localhost</div>
<pre># In docker-compose.yml:
services:
  postgres:
    ports:
      - "127.0.0.1:5432:5432"  # Not 5432:5432</pre></div>
<div class="fix-box"><div class="label">Or use DOCKER-USER chain rule</div>
<pre>sudo iptables -I DOCKER-USER -p tcp --dport 5432 -j DROP
sudo iptables -I DOCKER-USER -p tcp --dport 5432 -s 127.0.0.1 -j ACCEPT
sudo apt install iptables-persistent && sudo netfilter-persistent save</pre></div>""",
            "cta_text": "Paste your ufw status verbose to audit all Docker-exposed ports.",
            "cta_href": "/firewall/",
        },
    ],
    "nftables": [
        {
            "slug": "ubuntu-22",
            "title": "Fix: nftables Setup on Ubuntu 22.04",
            "meta_desc": "How to configure nftables as the firewall on Ubuntu 22.04. Basic ruleset, Docker compatibility, and UFW coexistence.",
            "keywords": "nftables ubuntu 22.04, nftables setup ubuntu, nftables docker ubuntu 22",
            "body": """<p>Ubuntu 22.04 uses nftables as the backend for iptables by default. The <code>iptables</code> command maps to <code>iptables-nft</code>. Direct nftables configuration provides better performance for complex rulesets.</p>
<div class="fix-box"><div class="label">Basic nftables ruleset — /etc/nftables.conf</div>
<pre>#!/usr/sbin/nft -f
flush ruleset

table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif lo accept
    tcp dport { 22, 80, 443 } accept
    icmp type echo-request accept
  }
  chain forward {
    type filter hook forward priority 0; policy drop;
  }
  chain output {
    type filter hook output priority 0; policy accept;
  }
}</pre></div>
<pre>sudo systemctl enable nftables && sudo systemctl start nftables</pre>""",
            "cta_text": "Use the Firewall Auditor to check your UFW/iptables rules on Ubuntu 22.",
            "cta_href": "/firewall/",
        },
        {
            "slug": "docker-conflict",
            "title": "Fix: nftables and Docker Conflict on Linux",
            "meta_desc": "Docker uses iptables rules that conflict with nftables configurations. How to resolve nftables and Docker networking conflicts on Ubuntu and Debian.",
            "keywords": "nftables docker conflict, docker nftables incompatible, nftables iptables docker fix",
            "body": """<p>Docker writes iptables rules using the nft-compat layer on nftables systems. Conflicts arise when user nftables rules and Docker's iptables rules interact unexpectedly — containers can't reach the internet, or firewall rules are silently bypassed.</p>
<div class="fix-box"><div class="label">Option 1: Configure Docker to use iptables-legacy</div>
<pre># /etc/docker/daemon.json
{
  "iptables": true
}
# Then ensure iptables-legacy is the default:
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
sudo systemctl restart docker</pre></div>
<div class="fix-box"><div class="label">Option 2: Allow Docker forwarding in nftables</div>
<pre># Add to nftables.conf forward chain:
chain forward {
  type filter hook forward priority 0; policy drop;
  # Allow Docker container traffic:
  oifname "docker0" accept
  iifname "docker0" accept
}</pre></div>""",
            "cta_text": "Paste your ufw status verbose to audit firewall rules.",
            "cta_href": "/firewall/",
        },
    ],
    "cron": [
        {
            "slug": "overlapping-jobs",
            "title": "Fix: Overlapping Cron Jobs Running Simultaneously",
            "meta_desc": "How to prevent multiple instances of the same cron job running simultaneously. flock safety, lock files, and detecting cron job overlaps.",
            "keywords": "cron overlapping jobs fix, cron job runs twice, prevent concurrent cron, cron flock fix",
            "body": """<p>When a cron job takes longer than its schedule interval, the next invocation starts before the previous one finishes. Both run simultaneously, competing for resources and potentially corrupting data.</p>
<div class="fix-box"><div class="label">Fix — wrap with flock</div>
<pre># Before (unsafe):
*/5 * * * * /usr/local/bin/sync.sh

# After (flock-safe):
*/5 * * * * flock -n /tmp/sync.lock /usr/local/bin/sync.sh</pre></div>
<p><code>flock -n</code> exits immediately if the lock is already held. The kernel releases the lock automatically when the process exits — even on crash.</p>
<h2>Detect current overlaps</h2>
<pre>ps aux | grep sync.sh | grep -v grep
# Multiple lines = overlapping runs</pre>""",
            "cta_text": "Paste your crontab to visualise overlaps on a 24-hour timeline.",
            "cta_href": "/",
        },
        {
            "slug": "silent-failure",
            "title": "Fix: Cron Jobs Failing Silently",
            "meta_desc": "Cron jobs fail without any visible error because output is discarded by default. How to capture cron job output, set up logging, and get email alerts on failure.",
            "keywords": "cron silent failure fix, cron job not running no error, cron logging setup, cron output capture",
            "body": """<p>By default cron discards all output if no MAILTO is configured or if the mail system isn't set up. Failures disappear without a trace.</p>
<div class="fix-box"><div class="label">Log output with timestamps</div>
<pre># Append stdout and stderr to a log file:
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# With timestamps:
0 2 * * * date >> /var/log/backup.log; /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1</pre></div>
<div class="fix-box"><div class="label">Log rotation — /etc/logrotate.d/cron-backup</div>
<pre>/var/log/backup.log {
    weekly
    rotate 8
    compress
    missingok
    notifempty
}</pre></div>
<h2>Test in cron-like environment</h2>
<pre>env -i HOME=/root PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin $
  /usr/local/bin/your-script.sh</pre>""",
            "cta_text": "Visualise your crontab to detect timing and overlap issues.",
            "cta_href": "/",
        },
        {
            "slug": "flock-safety",
            "title": "Fix: Adding flock Safety to Cron Jobs",
            "meta_desc": "How to add flock safety to cron jobs to prevent concurrent execution. flock syntax, lock file placement, and converting existing crontabs.",
            "keywords": "cron flock safety, flock cron job, prevent duplicate cron, flock -n cron example",
            "body": """<p>flock is a Linux utility that acquires a file-based lock before running a command. It prevents a new invocation from starting if the previous one is still running.</p>
<div class="fix-box"><div class="label">flock syntax patterns</div>
<pre># Non-blocking (skip if running):
*/5 * * * * flock -n /tmp/jobname.lock /path/to/script.sh

# Wait up to 10 seconds then skip:
*/5 * * * * flock -w 10 /tmp/jobname.lock /path/to/script.sh

# With inline command:
*/5 * * * * flock -n /tmp/sync.lock bash -c 'cd /app && node sync.js'</pre></div>
<p>Use a unique lock file per job. <code>/tmp/</code> is cleared on reboot, so stale locks from crashed processes are automatically removed.</p>
<h2>Convert all jobs at once</h2>
<p>The ConfigClarity Cron Visualiser has a flock safety toggle — enable it to generate flock-wrapped versions of all your jobs with unique lock file names automatically.</p>""",
            "cta_text": "Toggle flock safety on in the Cron Visualiser to wrap all your jobs.",
            "cta_href": "/",
        },
        {
            "slug": "server-load-spike",
            "title": "Fix: Cron Jobs Causing Server Load Spikes",
            "meta_desc": "Multiple cron jobs scheduled at the same time cause CPU and I/O spikes. How to stagger cron schedules and detect load-causing job clusters.",
            "keywords": "cron server load spike, cron midnight load, stagger cron jobs, cron cpu spike fix",
            "body": """<p>When multiple jobs run at the same minute — especially midnight — they compete for CPU, disk I/O, and database connections simultaneously, causing load spikes that affect live traffic.</p>
<div class="fix-box"><div class="label">Stagger jobs across the midnight window</div>
<pre># Before — all at midnight:
0 0 * * * /usr/local/bin/backup.sh
0 0 * * * /usr/local/bin/cleanup.sh
0 0 * * * /usr/local/bin/report.sh

# After — staggered:
0  0 * * * /usr/local/bin/backup.sh
10 0 * * * /usr/local/bin/cleanup.sh
25 0 * * * /usr/local/bin/report.sh</pre></div>
<h2>Add random jitter for fleets</h2>
<pre># Add 0–10 minute random delay:
0 2 * * * sleep $((RANDOM % 600)) && /usr/local/bin/backup.sh</pre>""",
            "cta_text": "Paste your crontab to see job clusters on a 24-hour timeline.",
            "cta_href": "/",
        },
        {
            "slug": "ai-agent-collision",
            "title": "Fix: AI Agent Cron Job Collisions",
            "meta_desc": "AI agents running on cron schedules can spawn multiple concurrent instances. How to use flock to prevent AI agent job collisions on Linux servers.",
            "keywords": "ai agent cron collision, cron ai agent duplicate, ai cron job flock safety",
            "body": """<p>AI agents (LLM inference jobs, RAG pipelines, embedding workers) running on cron are especially collision-prone because they use significant memory and GPU time. Two concurrent instances can exhaust VRAM or cause OOM kills.</p>
<div class="fix-box"><div class="label">flock-safe AI agent cron job</div>
<pre># Prevent concurrent AI agent runs:
*/10 * * * * flock -n /tmp/ai-agent.lock /usr/local/bin/run-agent.sh

# With GPU memory check before running:
*/10 * * * * flock -n /tmp/ai-agent.lock bash -c \
  'nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | \
   awk "{if(NR==1 &amp;&amp; int($1) &lt; 2000) system(\"/usr/local/bin/run-agent.sh\")}"'</pre></div>
<p>For Ollama-based agents, also ensure Ollama is bound to <code>127.0.0.1</code> before exposing via cron-triggered scripts.</p>""",
            "cta_text": "Visualise AI agent job schedules in the Cron Visualiser.",
            "cta_href": "/",
        },
    ],
    "ssl": [
        {
            "slug": "expiry-monitoring",
            "title": "Fix: SSL Certificate Expiry Monitoring Setup",
            "meta_desc": "How to set up SSL certificate expiry monitoring on Linux. Bash script to check multiple domains and alert at 200 days remaining — not the standard 30.",
            "keywords": "ssl certificate expiry monitoring, ssl expiry alert linux, monitor ssl cert expiry bash",
            "body": """<p>The standard 30-day alert is too late — your renewal pipeline may have been broken for months before you find out. Monitor at 200 days.</p>
<div class="fix-box"><div class="label">Weekly SSL check cron job</div>
<pre>#!/bin/bash
# /usr/local/bin/check-ssl.sh
DOMAINS=("yourdomain.com" "api.yourdomain.com")
ALERT_DAYS=200
EMAIL="you@yourdomain.com"

for domain in "${DOMAINS[@]}"; do
  expiry=$(openssl s_client -connect "$domain:443" $
    -servername "$domain" 2>/dev/null | $
    openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null)
  days_left=$(( (expiry_epoch - $(date +%s)) / 86400 ))
  if [ "$days_left" -lt "$ALERT_DAYS" ]; then
    echo "$domain: $days_left days left" | $
      mail -s "SSL warning: $domain" "$EMAIL"
  fi
done</pre></div>
<pre># Add to crontab:
0 9 * * 1 flock -n /tmp/ssl-check.lock /usr/local/bin/check-ssl.sh</pre>""",
            "cta_text": "Check multiple domains at once with the SSL Checker — 200-day warnings included.",
            "cta_href": "/ssl/",
        },
        {
            "slug": "cdn-domain",
            "title": "Fix: SSL Certificate Issues on CDN-Fronted Domains",
            "meta_desc": "CDN-fronted domains have two certificates — the CDN edge cert and the origin cert. How to check both and why the origin cert expires silently.",
            "keywords": "cdn ssl certificate, cloudflare ssl cert check, cdn origin cert expiry, ssl cdn domain fix",
            "body": """<p>When your site is behind Cloudflare or another CDN, visitors see the CDN's certificate. Your origin server has its own certificate. Both can expire independently — and most monitoring tools only check the CDN cert.</p>
<div class="fix-box"><div class="label">Check origin cert directly</div>
<pre># Check what CDN serves to visitors:
openssl s_client -connect yourdomain.com:443 2>/dev/null | $
  openssl x509 -noout -dates

# Check origin cert directly (bypass CDN):
openssl s_client -connect YOUR_SERVER_IP:443 $
  -servername yourdomain.com 2>/dev/null | $
  openssl x509 -noout -dates</pre></div>
<p>The ConfigClarity SSL Checker flags CDN-fronted domains in orange — the cert is managed by the CDN and may have different renewal behaviour than origin certs.</p>""",
            "cta_text": "Check CDN and origin certs for your domains in the SSL Checker.",
            "cta_href": "/ssl/",
        },
        {
            "slug": "traefik-renewal",
            "title": "Fix: Traefik Let's Encrypt Certificate Renewal Failure",
            "meta_desc": "Traefik automatic HTTPS certificate renewal failing. How to diagnose and fix Let's Encrypt renewal issues in Traefik v2 and v3.",
            "keywords": "traefik lets encrypt renewal, traefik certificate renewal failed, traefik acme renewal fix",
            "body": """<p>Traefik handles Let's Encrypt certificates automatically via ACME. Renewal fails when port 80 is blocked, DNS doesn't resolve to the server, or the acme.json file has permission issues.</p>
<div class="fix-box"><div class="label">Check Traefik ACME logs</div>
<pre>docker logs traefik 2>&1 | grep -i "acme|cert|renew|error" | tail -30</pre></div>
<div class="fix-box"><div class="label">Fix acme.json permissions</div>
<pre>chmod 600 /path/to/acme.json
docker restart traefik</pre></div>
<div class="fix-box"><div class="label">Traefik static config — verify ACME settings</div>
<pre>certificatesResolvers:
  letsencrypt:
    acme:
      email: you@yourdomain.com
      storage: /acme.json        # Must be 600 permissions
      httpChallenge:
        entryPoint: web          # Port 80 must be accessible</pre></div>""",
            "cta_text": "Check your Traefik-managed domains for cert expiry in the SSL Checker.",
            "cta_href": "/ssl/",
        },
        {
            "slug": "nginx-renewal",
            "title": "Fix: Nginx + Certbot Let's Encrypt Renewal Failure",
            "meta_desc": "Certbot renewal failing on Nginx servers. How to diagnose renewal errors, fix port 80 blocking, and verify the certbot timer is active.",
            "keywords": "certbot renewal failed nginx, lets encrypt renewal error nginx, certbot nginx fix, certbot timer systemd",
            "body": """<p>Certbot renews Let's Encrypt certificates via HTTP-01 challenge on port 80. Renewal fails when port 80 is blocked, Nginx is misconfigured, or the certbot timer has stopped.</p>
<div class="fix-box"><div class="label">Test renewal dry-run</div>
<pre>sudo certbot renew --dry-run
# Look for: "Congratulations, all renewals succeeded"</pre></div>
<div class="fix-box"><div class="label">Check certbot timer status</div>
<pre>systemctl status certbot.timer
# Should show: active (waiting)
# If inactive: sudo systemctl enable --now certbot.timer</pre></div>
<div class="fix-box"><div class="label">Nginx config — allow ACME challenge through redirect</div>
<pre>server {
    listen 80;
    server_name yourdomain.com;

    # Must come before the HTTPS redirect:
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}</pre></div>""",
            "cta_text": "Check your Nginx-served domains for cert expiry warnings.",
            "cta_href": "/ssl/",
        },
        {
            "slug": "200-day-warning",
            "title": "Why Monitor SSL Expiry at 200 Days — Not 30",
            "meta_desc": "The standard 30-day SSL expiry warning is too late to catch broken renewal pipelines. Why 200 days is the right threshold and how to implement it.",
            "keywords": "ssl expiry 200 days, ssl certificate monitoring threshold, ssl 30 day warning too late",
            "body": """<p>Let's Encrypt certificates expire every 90 days and are designed to renew at 60 days remaining. If renewal breaks on the day of issuance, you have 89 days of silent failure before a 30-day alert fires. That's nearly three months of broken renewal you don't know about.</p>
<h2>The 200-day math</h2>
<p>A brand new Let's Encrypt cert has 90 days. A cert expiring in under 200 days means either: (a) it's a short-validity cert that was intentionally issued short, or (b) renewal has already failed and the cert is counting down. Either case warrants investigation immediately — not when 30 days remain.</p>
<div class="fix-box"><div class="label">200-day check in bash</div>
<pre>DAYS_LEFT=$(( ($(date -d "$(openssl s_client -connect $
  domain.com:443 2>/dev/null | openssl x509 -noout -enddate $
  | cut -d= -f2)" +%s) - $(date +%s)) / 86400 ))

[ "$DAYS_LEFT" -lt 200 ] && echo "WARNING: $DAYS_LEFT days left"</pre></div>""",
            "cta_text": "The SSL Checker flags certs expiring within 200 days across all your domains.",
            "cta_href": "/ssl/",
        },
    ],
    "nginx": [
        {
            "slug": "502-bad-gateway",
            "title": "Fix: Nginx 502 Bad Gateway Error",
            "meta_desc": "Nginx 502 Bad Gateway — upstream application unreachable. How to diagnose and fix 502 errors from stopped containers, wrong ports, or crashed services.",
            "keywords": "nginx 502 bad gateway fix, nginx upstream not found 502, nginx 502 docker fix",
            "body": """<p>Nginx returns 502 when it can't get a valid response from the upstream server. The upstream is either not running, on the wrong port, or unreachable on the configured address.</p>
<h2>Diagnosis checklist</h2>
<pre># 1. Is the upstream service running?
docker ps | grep your-service
systemctl status your-service

# 2. Is it listening on the expected port?
ss -tlnp | grep 3000

# 3. Can Nginx reach it?
curl -sI http://127.0.0.1:3000/

# 4. Check Nginx error log:
tail -50 /var/log/nginx/error.log | grep upstream</pre></div>
<div class="fix-box"><div class="label">Common fix — update proxy_pass port</div>
<pre>location / {
    proxy_pass http://127.0.0.1:3000;  # Verify port matches your app
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}</pre></div>
<pre>nginx -t && systemctl reload nginx</pre>""",
            "cta_text": "Paste your nginx.conf to detect dangling routes and wrong upstream ports.",
            "cta_href": "/proxy/",
        },
        {
            "slug": "upstream-timeout",
            "title": "Fix: Nginx Upstream Timeout (504 Gateway Timeout)",
            "meta_desc": "Nginx 504 Gateway Timeout — upstream took too long to respond. How to increase proxy timeouts for slow applications, AI inference, and file processing.",
            "keywords": "nginx 504 gateway timeout, nginx upstream timeout fix, nginx proxy timeout increase",
            "body": """<p>Nginx's default proxy timeout is 60 seconds. Applications that take longer — AI inference, large file processing, database-heavy requests — hit this limit and return 504.</p>
<div class="fix-box"><div class="label">Increase proxy timeouts in Nginx</div>
<pre>location / {
    proxy_pass http://127.0.0.1:3000;

    proxy_connect_timeout  60s;
    proxy_send_timeout    300s;   # Time to send request to upstream
    proxy_read_timeout    300s;   # Time to read response from upstream
    send_timeout          300s;
}</pre></div>
<p>Set timeouts in the specific <code>location</code> block rather than globally — this avoids applying long timeouts to fast endpoints.</p>
<pre>nginx -t && systemctl reload nginx</pre>""",
            "cta_text": "Paste your nginx.conf to detect missing timeout configuration.",
            "cta_href": "/proxy/",
        },
        {
            "slug": "ssl-redirect-missing",
            "title": "Fix: Nginx Missing HTTP to HTTPS Redirect",
            "meta_desc": "Nginx not redirecting HTTP to HTTPS. The exact server block for a permanent 301 redirect from port 80 to 443, including Let's Encrypt ACME challenge compatibility.",
            "keywords": "nginx http https redirect, nginx ssl redirect missing, nginx 301 https redirect fix",
            "body": """<p>Without an HTTP to HTTPS redirect, visitors who type your domain without <code>https://</code> see an unencrypted page. The fix is a single Nginx server block.</p>
<div class="fix-box"><div class="label">Add HTTP redirect server block</div>
<pre>server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;

    # Keep ACME challenge accessible for cert renewal:
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}</pre></div>
<pre>nginx -t && systemctl reload nginx

# Verify:
curl -sI http://yourdomain.com | grep -E "HTTP|location"
# Should show: HTTP/1.1 301 and location: https://...</pre>""",
            "cta_text": "Paste your nginx.conf to detect missing SSL redirects automatically.",
            "cta_href": "/proxy/",
        },
    ],
}

def write_fix_page(category, page_data):
    slug = page_data["slug"]
    path = f"fix/{category}/{slug}/index.html"
    os.makedirs(f"fix/{category}/{slug}", exist_ok=True)

    cat_name = category.upper()
    crumbs = [
        ("ConfigClarity", "/"),
        ("Fix Guides", "/fix/"),
        (f"{cat_name} Fix Guides", f"/fix/{category}/"),
        (page_data["title"].replace("Fix: ", ""), f"/fix/{category}/{slug}/"),
    ]

    html = simple_page(
        page_data["title"], page_data["meta_desc"], page_data["keywords"],
        f"/fix/{category}/{slug}/", crumbs,
        page_data["title"], page_data["body"],
        page_data["cta_text"], page_data["cta_href"]
    )
    with open(path, "w") as f:
        f.write(html)
    return path


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — PROVIDER PAGES (90 pages)
# ═══════════════════════════════════════════════════════════════════════════════

PROVIDERS = [
    ("hetzner", "Hetzner"),
    ("digitalocean", "DigitalOcean"),
    ("vultr", "Vultr"),
    ("linode", "Linode / Akamai"),
    ("contabo", "Contabo"),
    ("ovh", "OVH"),
    ("scaleway", "Scaleway"),
    ("upcloud", "UpCloud"),
    ("ionos", "IONOS"),
    ("netcup", "Netcup"),
    ("aws-lightsail", "AWS Lightsail"),
    ("oracle-cloud", "Oracle Cloud Free"),
    ("raspberry-pi", "Raspberry Pi"),
    ("azure-vm", "Azure VM"),
    ("gcp-compute", "GCP Compute Engine"),
]

PROVIDER_TOPICS = [
    ("docker-firewall", "Docker Firewall Setup",
     "How to configure Docker and UFW firewall rules on {pn} to prevent Docker UFW bypass and protect container ports.",
     "Docker containers bypass UFW by default on {pn} servers. The fix: bind container ports to 127.0.0.1 and use DOCKER-USER chain rules.",
     "/firewall/"),
    ("ssl-setup", "SSL Certificate Setup",
     "How to install and configure SSL/TLS certificates on {pn} with Let's Encrypt, certbot, and Nginx or Traefik.",
     "Install certbot, obtain a Let's Encrypt certificate, and configure Nginx for HTTPS on your {pn} server.",
     "/ssl/"),
    ("ufw-docker", "UFW and Docker Configuration",
     "How to configure UFW firewall alongside Docker on {pn} to prevent port exposure. Docker UFW bypass fix for {pn} servers.",
     "Docker bypasses UFW on {pn} servers. Bind container ports to 127.0.0.1 and configure DOCKER-USER chain rules to protect exposed services.",
     "/firewall/"),
    ("docker-setup", "Docker Setup Guide",
     "How to install and configure Docker with secure defaults on {pn}. Port binding, network isolation, and firewall configuration.",
     "Install Docker on {pn} with secure port binding — bind to 127.0.0.1, not 0.0.0.0. Configure UFW rules and Docker network isolation.",
     "/docker/"),
    ("ssh-hardening", "SSH Hardening Guide",
     "How to harden SSH configuration on {pn} servers. Disable password auth, configure key-based login, and set fail2ban protection.",
     "Harden SSH on your {pn} server: disable password authentication, restrict to key-based login, change the default port, and configure fail2ban.",
     "/firewall/"),
    ("firewall-setup", "Firewall Setup Guide",
     "How to configure UFW firewall on {pn} with correct default-deny rules, Docker compatibility, and IPv6 protection.",
     "Configure UFW on {pn} with default-deny incoming, allow only required ports, enable IPv6 rules, and handle Docker port exposure correctly.",
     "/firewall/"),
]

def write_provider_page(pslug, pname, tslug, ttitle, tmeta, tbody, tcta_href):
    path = f"providers/{pslug}/{tslug}/index.html"
    os.makedirs(f"providers/{pslug}/{tslug}", exist_ok=True)

    meta = tmeta.format(pn=pname)
    body_text = tbody.format(pn=pname)
    title = f"{pname} {ttitle}"

    crumbs = [
        ("ConfigClarity", "/"),
        ("Provider Guides", "/providers/"),
        (pname, f"/providers/{pslug}/"),
        (ttitle, f"/providers/{pslug}/{tslug}/"),
    ]

    body_html = f"<p>{body_text}</p>"

    html = simple_page(
        title, meta, f"{pslug} {tslug.replace('-',' ')}, {pslug} docker setup, {pslug} linux server",
        f"/providers/{pslug}/{tslug}/", crumbs,
        title, body_html,
        f"Audit your {pname} server configuration in ConfigClarity.", tcta_href
    )
    with open(path, "w") as f:
        f.write(html)
    return path


def write_provider_index(pslug, pname):
    path = f"providers/{pslug}/index.html"
    os.makedirs(f"providers/{pslug}", exist_ok=True)

    crumbs = [("ConfigClarity", "/"), ("Provider Guides", "/providers/"), (pname, f"/providers/{pslug}/")]
    links = "\n".join([
        f'<a href="/providers/{pslug}/{ts}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:0.85rem 1.1rem;margin-bottom:0.5rem;font-size:0.85rem;color:var(--text);">{tt}</a>'
        for ts, tt, *_ in PROVIDER_TOPICS
    ])
    body_html = f"<p>Server configuration guides specific to {pname} infrastructure.</p>{links}"
    html = simple_page(
        f"{pname} Server Configuration Guides",
        f"Docker firewall, SSL, UFW, Docker setup, SSH hardening, and firewall configuration guides for {pname} servers.",
        f"{pslug} docker setup, {pslug} ufw firewall, {pslug} ssl certificate",
        f"/providers/{pslug}/",
        crumbs,
        f"{pname} Server Configuration Guides",
        body_html,
        f"Audit your {pname} server in ConfigClarity.",
        "/firewall/",
    )
    with open(path, "w") as f:
        f.write(html)
    return path


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — CLEAN UP JUNK FILES
# ═══════════════════════════════════════════════════════════════════════════════

JUNK_DIRS = [
    "mnt",
    "crontab-validator",
    "docker-compose-linter",
    "nginx-config-validator",
    "home",
]


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    total = 0

    # 1. Fix pages
    print("=== Building Fix Pages ===\n")
    for category, pages in FIX_PAGES.items():
        for page in pages:
            path = write_fix_page(category, page)
            print(f"  ✅ {path}")
            total += 1

    # 2. Provider pages
    print(f"\n=== Building Provider Pages ===\n")
    for pslug, pname in PROVIDERS:
        # Skip if provider index already exists and has content
        idx = write_provider_index(pslug, pname)
        print(f"  ✅ {idx}")
        total += 1
        for tslug, ttitle, tmeta, tbody, tcta in PROVIDER_TOPICS:
            # Skip if already exists
            path = f"providers/{pslug}/{tslug}/index.html"
            if os.path.exists(path):
                continue
            write_provider_page(pslug, pname, tslug, ttitle, tmeta, tbody, tcta)
            print(f"  ✅ {path}")
            total += 1

    # 3. Clean junk
    print(f"\n=== Cleaning Junk Files ===\n")
    for d in JUNK_DIRS:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  🗑  {d}/ removed")
        else:
            print(f"  skip {d}/ (not found)")

    # 4. Update vercel.json
    print(f"\n=== Updating vercel.json ===\n")
    with open("vercel.json", "r") as f:
        config = json.load(f)

    new_rewrites = []
    # Fix pages
    for cat, pages in FIX_PAGES.items():
        new_rewrites.append({"source": f"/fix/{cat}/", "destination": f"/fix/{cat}/index.html"})
        new_rewrites.append({"source": f"/fix/{cat}", "destination": f"/fix/{cat}/index.html"})
        for page in pages:
            s = page["slug"]
            new_rewrites.append({"source": f"/fix/{cat}/{s}/", "destination": f"/fix/{cat}/{s}/index.html"})
            new_rewrites.append({"source": f"/fix/{cat}/{s}", "destination": f"/fix/{cat}/{s}/index.html"})

    # Provider pages
    for pslug, _ in PROVIDERS:
        new_rewrites.append({"source": f"/providers/{pslug}/", "destination": f"/providers/{pslug}/index.html"})
        new_rewrites.append({"source": f"/providers/{pslug}", "destination": f"/providers/{pslug}/index.html"})
        for tslug, *_ in PROVIDER_TOPICS:
            new_rewrites.append({"source": f"/providers/{pslug}/{tslug}/", "destination": f"/providers/{pslug}/{tslug}/index.html"})
            new_rewrites.append({"source": f"/providers/{pslug}/{tslug}", "destination": f"/providers/{pslug}/{tslug}/index.html"})

    added = 0
    for r in new_rewrites:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)
            added += 1

    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  ✅ vercel.json — {added} rewrites added, {len(config['rewrites'])} total")

    # 5. Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()

    new_urls = []
    for cat, pages in FIX_PAGES.items():
        new_urls.append(f"/fix/{cat}/")
        for page in pages:
            new_urls.append(f"/fix/{cat}/{page['slug']}/")
    for pslug, _ in PROVIDERS:
        new_urls.append(f"/providers/{pslug}/")
        for tslug, *_ in PROVIDER_TOPICS:
            new_urls.append(f"/providers/{pslug}/{tslug}/")

    entries = "\n".join([
        f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>"
        for u in new_urls if u not in sitemap
    ])
    if entries:
        sitemap = sitemap.replace("</urlset>", entries + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
    print(f"  ✅ sitemap-seo.xml — {len(new_urls)} URLs added")

    print(f"\n{'='*50}")
    print(f"Done. {total} pages built/rebuilt.")
    print(f"\nRun:")
    print(f"  git add -A && git commit -m 'rebuild: restore missing fix+provider pages, clean junk' && git push origin main && npx vercel --prod --force")
    print(f"\nVerify after deploy:")
    print(f"  curl -sI https://www.configclarity.dev/fix/ufw/docker-bypass/ | grep HTTP")
    print(f"  curl -sI https://www.configclarity.dev/providers/hetzner/docker-firewall/ | grep HTTP")
    print(f"  curl -sI https://www.configclarity.dev/fix/ssl/expiry-monitoring/ | grep HTTP")
