#!/usr/bin/env python3
"""
Build 5 blog posts in human voice.
Run from: ~/Projects/CronSight/
"""

import os
from datetime import date

TODAY = date.today().isoformat()
BASE = "https://configclarity.dev"

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

CSS = """
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root {
        --bg: #0b0d14; --bg2: #1e2130; --purple: #6c63ff;
        --green: #22c55e; --orange: #f97316; --red: #ef4444;
        --text: #e2e4f0; --muted: #8a8fb5;
      }
      body { background: var(--bg); color: var(--text); font-family: 'JetBrains Mono', monospace; min-height: 100vh; line-height: 1.8; }
      a { color: var(--purple); text-decoration: none; }
      a:hover { text-decoration: underline; }
      .header { padding: 1.5rem 2rem; border-bottom: 1px solid #2a2d3d; display: flex; align-items: center; gap: 1rem; }
      .header-logo { font-size: 1.1rem; font-weight: 700; color: var(--text); }
      .header-logo span { color: var(--purple); }
      .header-nav { margin-left: auto; display: flex; gap: 1rem; font-size: 0.8rem; }
      .header-nav a { color: var(--muted); }
      .hero { max-width: 720px; margin: 0 auto; padding: 3rem 2rem 1.5rem; }
      .hero-meta { font-size: 0.75rem; color: var(--muted); margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; }
      .hero-tag { background: rgba(108,99,255,.15); color: var(--purple); padding: 0.15rem 0.6rem; border-radius: 4px; }
      h1 { font-size: 1.75rem; font-weight: 700; line-height: 1.35; margin-bottom: 1rem; }
      .lede { font-size: 1rem; color: var(--muted); margin-bottom: 2rem; line-height: 1.75; }
      .content { max-width: 720px; margin: 0 auto; padding: 0 2rem 4rem; }
      h2 { font-size: 1.15rem; font-weight: 700; margin: 2.5rem 0 0.75rem; color: var(--text); }
      h3 { font-size: 0.95rem; font-weight: 700; margin: 1.75rem 0 0.5rem; color: var(--text); }
      p { font-size: 0.875rem; color: var(--muted); margin-bottom: 1.1rem; }
      strong { color: var(--text); }
      pre { background: #0d0f1a; border: 1px solid #2a2d3d; border-radius: 8px; padding: 1.25rem 1.5rem; font-size: 0.78rem; overflow-x: auto; margin: 1rem 0 1.5rem; line-height: 1.7; }
      code { background: #1e2130; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.82rem; color: var(--text); }
      .callout { background: var(--bg2); border-left: 3px solid var(--purple); border-radius: 0 8px 8px 0; padding: 1.1rem 1.4rem; margin: 1.5rem 0; font-size: 0.875rem; }
      .callout.warn { border-color: var(--orange); }
      .callout.danger { border-color: var(--red); }
      .callout.good { border-color: var(--green); }
      .callout p { margin-bottom: 0; }
      .cta { background: var(--bg2); border: 1px solid #2a2d3d; border-radius: 8px; padding: 1.5rem; margin: 2.5rem 0; text-align: center; }
      .cta p { color: var(--text); font-size: 0.875rem; margin-bottom: 0.75rem; }
      .cta a { display: inline-block; background: var(--purple); color: #fff; padding: 0.5rem 1.25rem; border-radius: 6px; font-size: 0.82rem; font-weight: 700; text-decoration: none; }
      .breadcrumb { padding: 1rem 2rem 0; max-width: 720px; margin: 0 auto; font-size: 0.75rem; color: var(--muted); }
      .breadcrumb a { color: var(--muted); }
      .divider { border: none; border-top: 1px solid #2a2d3d; margin: 2rem 0; }
      footer { text-align: center; padding: 2rem; font-size: 0.75rem; color: var(--muted); border-top: 1px solid #2a2d3d; }
      @media (max-width: 600px) { h1 { font-size: 1.4rem; } .hero, .content { padding-left: 1.25rem; padding-right: 1.25rem; } }
    </style>
"""

HEADER = """
  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a><a href="/ssl/">SSL</a><a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a><a href="/proxy/">Proxy</a><a href="/robots/">robots.txt</a>
      <a href="/blog/" style="color:var(--purple);">Blog</a>
    </nav>
  </header>
"""

FOOTER = """
  <footer>
    <p>Part of the <a href="https://metriclogic.dev">MetricLogic</a> network &nbsp;·&nbsp;
    <a href="https://configclarity.dev">ConfigClarity</a> &nbsp;·&nbsp;
    <a href="/blog/">More articles</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>
"""

def page(slug, title, meta_desc, keywords, date_str, tags, lede, body, schema_extra=""):
    tag_html = "".join([f'<span class="hero-tag">{t}</span>' for t in tags])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — ConfigClarity</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{BASE}/blog/{slug}/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{BASE}/blog/{slug}/">
  <meta property="og:type" content="article">
  {FONT}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{meta_desc}",
    "url": "{BASE}/blog/{slug}/",
    "datePublished": "{date_str}",
    "dateModified": "{date_str}",
    "author": {{"@type": "Organization", "name": "MetricLogic", "url": "https://metriclogic.dev"}},
    "publisher": {{"@type": "Organization", "name": "ConfigClarity", "url": "https://configclarity.dev"}},
    "isPartOf": {{"@type": "Blog", "name": "ConfigClarity Blog", "url": "{BASE}/blog/"}}
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"{BASE}"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"{BASE}/blog/"}},
    {{"@type":"ListItem","position":3,"name":"{title}","item":"{BASE}/blog/{slug}/"}}
  ]}}
  </script>
  {schema_extra}
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › {title}</div>
  <div class="hero">
    <div class="hero-meta">
      <span>{date_str}</span>
      <span>·</span>
      {tag_html}
    </div>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
  <div class="content">
    {body}
  </div>
{FOOTER}
</body>
</html>"""


# ─── POST 1 ────────────────────────────────────────────────────────────────────

POST_1_BODY = """
<p>I've seen this exact situation play out dozens of times. Someone sets up a Docker server, installs UFW, adds a deny rule for their database port, checks <code>ufw status</code>, sees "Status: active" and the deny rule listed, and assumes they're protected.</p>

<p>Then they run a port scan from an external machine and their Redis instance is wide open.</p>

<p>This isn't a bug. It's how Docker works. But it trips up almost everyone the first time — and sometimes the second time too.</p>

<h2>What UFW actually does (and doesn't do)</h2>

<p>UFW manages Linux's iptables rules. Specifically, it manages the <strong>INPUT chain</strong> — the chain that handles traffic coming into the host machine itself.</p>

<p>Here's the problem: Docker doesn't use the INPUT chain for container traffic. It uses the <strong>FORWARD chain</strong> and a custom <strong>DOCKER chain</strong> it creates itself. Traffic destined for a container gets routed through FORWARD before it ever reaches INPUT.</p>

<p>So when you run <code>ufw deny 6379</code>, you're blocking direct connections to port 6379 on the host. But when Docker maps a container's Redis port to <code>0.0.0.0:6379</code>, that traffic flows through the DOCKER chain — and UFW never sees it.</p>

<div class="callout danger">
  <p><strong>The result:</strong> Your UFW rules look correct. Your Redis port is open to the internet anyway.</p>
</div>

<h2>How to actually see the problem</h2>

<p>Run this:</p>

<pre>sudo iptables -L DOCKER --line-numbers</pre>

<p>You'll see ACCEPT rules that Docker added. Every port-mapped container gets one. These rules run before your UFW INPUT rules ever fire.</p>

<p>Now run:</p>

<pre>sudo iptables -L FORWARD | grep DOCKER</pre>

<p>Docker inserts itself into the FORWARD chain too. It's thorough about this.</p>

<h2>The fixes — pick one</h2>

<h3>Option 1: Bind to 127.0.0.1 (cleanest, recommended)</h3>

<p>Instead of letting Docker bind to all interfaces, tell it to bind only to localhost. Traffic then only reaches the container via your reverse proxy, not directly from the internet.</p>

<p>In <code>docker-compose.yml</code>:</p>

<pre># Before — exposed to internet:
ports:
  - "6379:6379"

# After — localhost only:
ports:
  - "127.0.0.1:6379:6379"</pre>

<p>This works because Docker's iptables rules only forward traffic from the bound interface. If it's bound to 127.0.0.1, external traffic never triggers the forwarding rule.</p>

<h3>Option 2: DOCKER-USER chain rules</h3>

<p>Docker reserves a chain called DOCKER-USER specifically for user-defined rules that run before Docker's own rules. Rules you add here actually stick.</p>

<pre>sudo iptables -I DOCKER-USER -p tcp --dport 6379 -j DROP
sudo iptables -I DOCKER-USER -p tcp --dport 6379 -s 127.0.0.1 -j ACCEPT</pre>

<p>The catch: these rules don't survive a reboot unless you persist them with <code>iptables-persistent</code>.</p>

<pre>sudo apt install iptables-persistent
sudo netfilter-persistent save</pre>

<h3>Option 3: Internal Docker networks (for container-to-container traffic)</h3>

<p>If you just need containers to talk to each other without exposing ports to the host, don't publish ports at all. Use Docker's internal networking:</p>

<pre>services:
  app:
    networks:
      - internal
  redis:
    networks:
      - internal
    # No ports: block at all

networks:
  internal:
    internal: true</pre>

<p>With <code>internal: true</code>, the network has no external connectivity. Containers can reach each other by service name, but nothing outside the Docker network can reach them.</p>

<h2>How to verify you're actually protected</h2>

<p>Don't trust <code>ufw status</code> alone. Run a real test from outside:</p>

<pre># From another machine (replace with your server IP):
nc -zv YOUR_SERVER_IP 6379

# Or use nmap:
nmap -p 6379 YOUR_SERVER_IP</pre>

<p>If the port is closed, you're done. If it's open, you have the bypass problem.</p>

<div class="callout good">
  <p><strong>Quick check:</strong> Paste your <code>ufw status verbose</code> output into the <a href="/firewall/">ConfigClarity Firewall Auditor</a>. It flags Docker bypass risk and shows which ports are potentially exposed despite your UFW rules.</p>
</div>

<h2>Why this happens on fresh installs</h2>

<p>The default Docker install modifies iptables without asking. The default UFW install doesn't know about Docker. Neither tool warns you about the conflict. So you end up with two systems that both appear to be working correctly but are silently fighting each other.</p>

<p>The fix is a one-line change to your docker-compose.yml. Do it for every service that doesn't need to be publicly accessible — databases, caches, internal APIs, anything behind a reverse proxy.</p>

<div class="cta">
  <p>Paste your <code>ufw status verbose</code> output and get an instant audit of your firewall rules — Docker bypass detection included.</p>
  <a href="/firewall/">Open Firewall Auditor →</a>
</div>
"""

POST_1 = page(
    slug="docker-ufw-bypass-explained",
    title="Docker Bypasses UFW. Here's Why — and How to Fix It.",
    meta_desc="Docker's iptables rules bypass UFW's deny rules, exposing container ports to the internet. Why this happens, how to verify it, and three ways to fix it.",
    keywords="docker ufw bypass, docker firewall bypass, ufw docker not blocking, docker iptables ufw",
    date_str="2026-03-23",
    tags=["Docker", "UFW", "Security", "Linux"],
    lede="UFW is active. You added a deny rule for your database port. You checked — it's there. Your Redis is still open to the internet. Here's what's actually happening.",
    body=POST_1_BODY,
)

# ─── POST 2 ────────────────────────────────────────────────────────────────────

POST_2_BODY = """
<p>Most cron jobs are set up once and never touched again. That's fine when they're simple. It stops being fine when you have six of them all running at midnight, one of them silently failing for three weeks, and nobody notices until the backup you needed doesn't exist.</p>

<p>Here are the patterns that actually matter — things I've seen go wrong on real servers.</p>

<h2>Schedule them so they don't pile up</h2>

<p>The instinct is to run things at midnight or at the top of the hour. Everyone does this. The result is a server that idles all day then spikes at 00:00 when five jobs hit simultaneously.</p>

<p>Spread them out. Not by much — even five minutes apart makes a difference:</p>

<pre># Bad — everything at midnight:
0 0 * * * /usr/local/bin/backup.sh
0 0 * * * /usr/local/bin/cleanup.sh
0 0 * * * /usr/local/bin/report.sh

# Better — staggered:
0 0 * * *  /usr/local/bin/backup.sh
5 0 * * *  /usr/local/bin/cleanup.sh
15 0 * * * /usr/local/bin/report.sh</pre>

<p>The backup job finishes before cleanup starts. The disk I/O from the backup doesn't compete with cleanup's I/O. Simple.</p>

<h2>Use flock — always</h2>

<p>A cron job scheduled to run every 5 minutes that sometimes takes 7 minutes will eventually run twice at the same time. This is not hypothetical. It will happen.</p>

<p>When it does, two instances of your script will be writing to the same files, hitting the same database, or sending the same emails twice.</p>

<pre># Wrap any job that shouldn't run concurrently:
*/5 * * * * flock -n /tmp/sync.lock /usr/local/bin/sync.sh</pre>

<p><code>flock -n</code> means non-blocking — if the lock is already held (previous run still going), the new invocation exits immediately without doing anything. No error, no data corruption, no duplicate emails.</p>

<p>The lock file is just a regular file. It doesn't need to exist before you run the command. And when the process exits — even if it crashes — the kernel releases the lock automatically. No cleanup required.</p>

<div class="callout">
  <p>Use a unique lock file per job. <code>/tmp/sync.lock</code> and <code>/tmp/backup.lock</code> — not both using <code>/tmp/job.lock</code>.</p>
</div>

<h2>Capture output or you'll never know it failed</h2>

<p>By default, cron emails output to the local root mailbox. On most servers, nobody reads that. So when your job starts failing, the errors disappear into a mailbox that hasn't been opened in two years.</p>

<p>Two options — pick one:</p>

<pre># Option 1: Log to a file with timestamps:
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# Option 2: Silence successful runs, keep errors visible (my preference):
0 2 * * * /usr/local/bin/backup.sh 2>/var/log/backup-errors.log</pre>

<p>Then set up log rotation so these files don't grow forever:</p>

<pre># /etc/logrotate.d/backup
/var/log/backup.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
}</pre>

<h2>Set the PATH explicitly</h2>

<p>Cron runs with a stripped-down environment. The PATH is minimal — usually just <code>/usr/bin:/bin</code>. If your script calls anything in <code>/usr/local/bin</code> or uses a tool installed via npm or pip, it won't be found.</p>

<p>The fix is either to use absolute paths everywhere in your scripts, or to set PATH at the top of your crontab:</p>

<pre># At the top of crontab -e:
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Now your jobs can call things in /usr/local/bin:
0 3 * * * certbot renew --quiet</pre>

<h2>Test before you rely on it</h2>

<p>The most common cron debugging mistake is editing the crontab and waiting to see if the job runs at the scheduled time. You might be waiting hours.</p>

<p>Test it now:</p>

<pre># Run exactly what cron would run, in a minimal environment:
env -i HOME=/root PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin /usr/local/bin/your-script.sh</pre>

<p>The <code>env -i</code> strips your current environment variables. If the script works in your shell but fails here, you've found your problem — usually a missing PATH entry or an environment variable your script assumed would exist.</p>

<h2>@reboot jobs need special care</h2>

<p>Jobs with <code>@reboot</code> run once when the system starts. They run before most services are ready — before your database is up, before your network is fully configured, before your mounted drives are necessarily mounted.</p>

<pre># Add a sleep to let things settle first:
@reboot sleep 30 && /usr/local/bin/start-service.sh</pre>

<p>30 seconds is usually enough for a standard VPS. If your startup script depends on a database, add a proper wait loop instead:</p>

<pre>@reboot sleep 10 && until pg_isready; do sleep 2; done && /usr/local/bin/start-service.sh</pre>

<div class="cta">
  <p>Paste your crontab output to visualise every job on a 24-hour timeline — see overlaps, collision risks, and get flock-safe versions of all your jobs.</p>
  <a href="/">Open Cron Visualiser →</a>
</div>
"""

POST_2 = page(
    slug="cron-job-best-practices",
    title="Cron Job Best Practices That Actually Matter",
    meta_desc="flock safety, staggered scheduling, output logging, PATH issues — the cron patterns that prevent silent failures and data corruption on Linux servers.",
    keywords="cron job best practices, cron flock safety, cron logging, cron PATH issue, linux cron tips",
    date_str="2026-03-23",
    tags=["Cron", "Linux", "DevOps"],
    lede="Most cron problems are invisible. The job appears to run. The logs are empty. The output was silently discarded. And nobody notices until the backup that should have been running for three weeks simply isn't there.",
    body=POST_2_BODY,
)

# ─── POST 3 ────────────────────────────────────────────────────────────────────

POST_3_BODY = """
<p>SSL certificate expiry is one of the most preventable causes of outages. The date is embedded in the certificate itself. You can check it months in advance. There's no surprise — just a failure to look.</p>

<p>And yet it keeps happening, because most setups have a monitoring gap somewhere: the renewal cron job that silently failed, the CDN cert that's separate from the origin cert, the domain someone forgot was still pointing at a server.</p>

<p>Here's how to actually monitor it.</p>

<h2>The 200-day rule</h2>

<p>Most guides say to alert at 30 days. That's too late. Here's why:</p>

<p>Let's Encrypt certificates expire every 90 days. They're designed to auto-renew at 60 days remaining. If auto-renewal breaks the day after issuance, you have 89 days of silent failure before the 30-day alert fires.</p>

<p>Check at 200 days. If something is expiring in under 200 days and it shouldn't be — your renewal pipeline is broken and you have time to fix it before anything actually breaks.</p>

<div class="callout warn">
  <p>The 30-day alert is for catching emergencies. The 200-day check is for catching broken renewal pipelines while you still have runway.</p>
</div>

<h2>The CDN trap</h2>

<p>If your site is behind Cloudflare, Fastly, or any other CDN, you have two certificates:</p>

<ol style="padding-left:1.5rem;font-size:0.875rem;color:var(--muted);line-height:2;">
  <li>The CDN's certificate — the one your visitors see</li>
  <li>Your origin certificate — the one between the CDN and your server</li>
</ol>

<p>Most monitoring tools check from the outside. They see the CDN cert — which is usually auto-managed and fine. The origin cert can be expiring unnoticed behind the CDN's edge.</p>

<p>Check your origin cert directly:</p>

<pre>openssl s_client -connect YOUR_SERVER_IP:443 -servername yourdomain.com 2>/dev/null | \
  openssl x509 -noout -dates</pre>

<p>And check what the CDN is serving to visitors:</p>

<pre>openssl s_client -connect yourdomain.com:443 2>/dev/null | \
  openssl x509 -noout -dates</pre>

<p>Both should have comfortable expiry dates. The origin cert is the one that breaks silently.</p>

<h2>A simple monitoring script</h2>

<p>This checks a list of domains and emails you if anything expires within 200 days:</p>

<pre>#!/bin/bash
# /usr/local/bin/check-ssl.sh
DOMAINS=("yourdomain.com" "api.yourdomain.com" "app.yourdomain.com")
ALERT_DAYS=200
EMAIL="you@yourdomain.com"

for domain in "${DOMAINS[@]}"; do
  expiry=$(openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null | \
    openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

  if [ -z "$expiry" ]; then
    echo "WARN: $domain — could not fetch cert" | mail -s "SSL Check: $domain" "$EMAIL"
    continue
  fi

  expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null || date -jf "%b %e %T %Y %Z" "$expiry" +%s)
  now_epoch=$(date +%s)
  days_left=$(( (expiry_epoch - now_epoch) / 86400 ))

  if [ "$days_left" -lt "$ALERT_DAYS" ]; then
    echo "$domain expires in $days_left days ($expiry)" | \
      mail -s "SSL expiry warning: $domain ($days_left days)" "$EMAIL"
  fi
done</pre>

<p>Add to cron to run weekly:</p>

<pre>0 9 * * 1 flock -n /tmp/ssl-check.lock /usr/local/bin/check-ssl.sh</pre>

<h2>Checking multiple domains at once</h2>

<p>If you manage more than a few domains, the command-line approach gets unwieldy. The ConfigClarity SSL Checker takes a list of domains, fetches their certificates via crt.sh, and flags anything expiring within 200 days — along with a note for CDN-fronted domains where the cert ownership is ambiguous.</p>

<h2>The renewal pipeline audit</h2>

<p>If you're using certbot, verify the renewal is actually working:</p>

<pre># Test renewal without actually renewing:
certbot renew --dry-run

# Check the certbot timer is active (systemd):
systemctl status certbot.timer

# Check the renewal log:
cat /var/log/letsencrypt/letsencrypt.log | grep -E "Cert not|renewed|error"</pre>

<p>A common failure mode: the certbot renewal works fine for a year, then a server migration or DNS change breaks the ACME challenge. The renewal silently fails. You find out 89 days later when the 30-day alert fires. By then you're under pressure.</p>

<p>Run <code>certbot renew --dry-run</code> monthly. Add it to cron. It takes 10 seconds and tells you immediately if something is broken.</p>

<div class="callout good">
  <p>The ConfigClarity SSL Checker flags certificates expiring within 200 days — not the standard 30. Paste a list of domains and get expiry status, CDN detection, and chain validation in one pass.</p>
</div>

<div class="cta">
  <p>Check multiple domains at once — expiry dates, CDN detection, certificate chain, and 200-day early warnings.</p>
  <a href="/ssl/">Open SSL Checker →</a>
</div>
"""

POST_3 = page(
    slug="ssl-certificate-monitoring-guide",
    title="SSL Certificate Monitoring: Why 30 Days Is Too Late",
    meta_desc="Why monitoring SSL expiry at 30 days misses broken renewal pipelines. The 200-day rule, CDN cert traps, and a simple bash script to catch expiry before it becomes an outage.",
    keywords="ssl certificate monitoring, ssl expiry monitoring, lets encrypt renewal check, ssl cert expiry alert, certificate monitoring linux",
    date_str="2026-03-23",
    tags=["SSL", "Monitoring", "Let's Encrypt", "DevOps"],
    lede="The standard advice is to alert when your SSL cert has 30 days left. That's too late. By then your renewal pipeline has already been broken for two months and you just didn't know yet.",
    body=POST_3_BODY,
)

# ─── POST 4 ────────────────────────────────────────────────────────────────────

POST_4_BODY = """
<p>Ollama has made it genuinely easy to run large language models on your own hardware. A few commands and you have a local API serving Llama, Mistral, or whatever model fits your VRAM. The problem is that the default setup is wide open, and most guides don't mention this.</p>

<p>Here's what you need to lock down before you put an Ollama server anywhere near the internet.</p>

<h2>Ollama binds to 0.0.0.0 by default</h2>

<p>Out of the box, Ollama listens on <code>0.0.0.0:11434</code>. That means every network interface — including whatever public IP your VPS has. Anyone who can reach port 11434 can make requests to your model.</p>

<p>This isn't theoretical. Exposed Ollama instances show up in Shodan searches. People use them for free inference. Your expensive GPU hours, someone else's prompts.</p>

<p>Check if yours is exposed right now:</p>

<pre>curl http://YOUR_SERVER_IP:11434/api/tags</pre>

<p>If you get a JSON response listing your models, it's publicly accessible.</p>

<h2>Fix 1: Bind to localhost only</h2>

<p>The simplest fix is to tell Ollama to only listen on the loopback interface:</p>

<pre># In your ollama systemd service override:
sudo systemctl edit ollama.service

# Add:
[Service]
Environment="OLLAMA_HOST=127.0.0.1"</pre>

<pre>sudo systemctl daemon-reload
sudo systemctl restart ollama</pre>

<p>Now Ollama only accepts connections from the same machine. Your applications on the same server can still reach it at <code>http://localhost:11434</code>, but nothing external can.</p>

<h2>Fix 2: Put it behind Nginx with authentication</h2>

<p>If you need to access Ollama from other machines — a development laptop, another server — run it behind Nginx with HTTP basic auth. Don't expose the Ollama port directly.</p>

<pre># /etc/nginx/sites-available/ollama
server {
    listen 443 ssl;
    server_name ollama.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/ollama.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ollama.yourdomain.com/privkey.pem;

    auth_basic "Ollama";
    auth_basic_user_file /etc/nginx/.ollama-htpasswd;

    location / {
        proxy_pass http://127.0.0.1:11434;
        proxy_set_header Host $host;
        proxy_read_timeout 300s;  # Models can take a while to respond
    }
}</pre>

<pre># Generate the password file:
sudo htpasswd -c /etc/nginx/.ollama-htpasswd yourusername</pre>

<p>Set a long timeout. Model inference takes time, and nothing is more frustrating than a 60-second nginx timeout killing a response that was 30 seconds from finishing.</p>

<h2>Fix 3: UFW rules (but watch out for Docker)</h2>

<p>If you're running Ollama directly (not in Docker), UFW will protect it:</p>

<pre>sudo ufw deny 11434</pre>

<p>If you're running Ollama in a Docker container with a published port — see the Docker UFW bypass issue. Your <code>ufw deny</code> rule won't help. Bind to 127.0.0.1 in the container's port mapping instead:</p>

<pre># docker-compose.yml
services:
  ollama:
    image: ollama/ollama
    ports:
      - "127.0.0.1:11434:11434"  # Not 0.0.0.0:11434:11434</pre>

<h2>Rate limiting if you expose it</h2>

<p>If you're running a shared Ollama instance for a team, add rate limiting at the Nginx level to prevent any single user from monopolising the GPU:</p>

<pre># In nginx.conf, add a rate limit zone:
limit_req_zone $binary_remote_addr zone=ollama:10m rate=10r/m;

# In the server block:
location /api/generate {
    limit_req zone=ollama burst=5 nodelay;
    proxy_pass http://127.0.0.1:11434;
    proxy_read_timeout 300s;
}</pre>

<p>10 requests per minute per IP with a burst of 5 is a reasonable starting point for a team of 5–10 people. Adjust based on your usage.</p>

<h2>Model storage and disk</h2>

<p>Models are large. Llama 3 8B is about 5GB. Mistral 7B is similar. If you're pulling multiple models, your disk fills up faster than you'd expect.</p>

<pre># Check disk usage:
du -sh ~/.ollama/models/

# Or if running as a service:
du -sh /usr/share/ollama/.ollama/models/</pre>

<p>Set up a low-disk alert before this becomes a problem. When the disk fills, the server stops accepting writes. That usually means your Ollama service silently fails to pull updates and your logs stop rotating.</p>

<div class="cta">
  <p>Running Ollama in Docker? Check your firewall rules — Docker port mappings bypass UFW by default. Paste your ufw status output to get an instant audit.</p>
  <a href="/firewall/">Open Firewall Auditor →</a>
</div>
"""

POST_4 = page(
    slug="ollama-server-security",
    title="Securing an Ollama Server: Don't Leave Your GPU Open to the Internet",
    meta_desc="Ollama binds to 0.0.0.0 by default, exposing your local LLM to the internet. How to lock it down with localhost binding, Nginx auth, and Docker port safety.",
    keywords="ollama server security, ollama public access, ollama nginx reverse proxy, ollama docker security, secure ollama server",
    date_str="2026-03-23",
    tags=["Ollama", "Security", "Self-hosted", "Linux"],
    lede="Ollama's default install is great for local development. It's terrible for a server. Port 11434 is open, there's no authentication, and exposed instances show up in Shodan. Here's how to fix it in 10 minutes.",
    body=POST_4_BODY,
)

# ─── POST 5 ────────────────────────────────────────────────────────────────────

POST_5_BODY = """
<p>Traefik v3 shipped with breaking changes to its label syntax. If you upgraded without reading the migration guide — and many people did — your routes stopped working and the error messages weren't particularly helpful about why.</p>

<p>Here's a practical guide to what changed and what to update.</p>

<h2>What actually broke</h2>

<p>The core routing label syntax stayed the same. What changed was a set of specific features, middleware names, and some default behaviours. The two things that break the most setups:</p>

<p><strong>1. Docker provider changes</strong> — In v3, the Docker provider requires explicit network configuration if Traefik and your containers are on different Docker networks. In v2 it would figure this out automatically more often. In v3 it doesn't.</p>

<p><strong>2. allowEmptyServices removed</strong> — In v2 you could set <code>allowEmptyServices: true</code> to let Traefik start even when backends were down. This option was removed in v3. If you had it in your static config, Traefik v3 silently ignores it and may behave differently.</p>

<h2>The label syntax that still works</h2>

<p>Good news first — the core routing labels are identical between v2 and v3:</p>

<pre># These work in both v2 and v3:
traefik.enable=true
traefik.http.routers.myapp.rule=Host(`app.example.com`)
traefik.http.routers.myapp.tls.certresolver=letsencrypt
traefik.http.services.myapp.loadbalancer.server.port=3000</pre>

<p>If your setup only uses basic routing with TLS, you might not have anything to update.</p>

<h2>Old labels that no longer work</h2>

<p>These are Traefik v1 labels that some people were still using in v2 (where they were deprecated but worked). In v3 they do nothing:</p>

<pre># These are dead in v3 — remove them:
traefik.frontend.rule=Host:app.example.com     # v1 style
traefik.backend=myapp                           # v1 style
traefik.port=3000                               # v1 style
traefik.frontend.entryPoints=https             # v1 style</pre>

<p>If you see these in your compose files, they're silently doing nothing. Replace with the v2/v3 style:</p>

<pre># Equivalent v3 labels:
traefik.enable=true
traefik.http.routers.myapp.rule=Host(`app.example.com`)
traefik.http.routers.myapp.entrypoints=websecure
traefik.http.services.myapp.loadbalancer.server.port=3000</pre>

<h2>Middleware names changed</h2>

<p>Several built-in middleware types were renamed in v3. The most commonly used one:</p>

<pre># v2 — redirect to HTTPS:
traefik.http.middlewares.redirect-https.redirectscheme.scheme=https
traefik.http.middlewares.redirect-https.redirectscheme.permanent=true

# v3 — same thing, same syntax (this one didn't change):
traefik.http.middlewares.redirect-https.redirectscheme.scheme=https
traefik.http.middlewares.redirect-https.redirectscheme.permanent=true</pre>

<p>The middleware syntax itself is mostly unchanged. What changed is that some middleware options that were implicit in v2 need to be explicit in v3. Check the Traefik v3 migration guide for the full list if you're using rate limiting, circuit breakers, or IP allowlisting middleware.</p>

<h2>The Docker network problem</h2>

<p>This is what actually breaks most setups. In v2, if Traefik and your container were both on the default bridge network, Traefik could usually reach the container. In v3 the Docker provider is stricter about network attachment.</p>

<p>The fix is to put Traefik and all routed containers on a shared external network:</p>

<pre># docker-compose.yml (Traefik service):
services:
  traefik:
    image: traefik:v3
    networks:
      - traefik-public
    ports:
      - "80:80"
      - "443:443"

networks:
  traefik-public:
    external: true</pre>

<pre># docker-compose.yml (application service):
services:
  myapp:
    image: myapp:latest
    networks:
      - traefik-public
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.myapp.rule=Host(`app.example.com`)"
      - "traefik.docker.network=traefik-public"  # Tell Traefik which network to use

networks:
  traefik-public:
    external: true</pre>

<p>Create the network once:</p>

<pre>docker network create traefik-public</pre>

<h2>Checking your labels before you upgrade</h2>

<p>Paste your docker-compose.yml into the ConfigClarity Reverse Proxy Mapper. It detects Traefik v1 label patterns and generates the exact v3 replacements — including the network configuration fix.</p>

<h2>The static config changes</h2>

<p>If you're using a <code>traefik.yml</code> static config file rather than CLI flags, a few options moved:</p>

<pre># v2 static config:
providers:
  docker:
    exposedByDefault: false
    swarmMode: false

# v3 static config (swarmMode moved to swarm provider):
providers:
  docker:
    exposedByDefault: false
  swarm:           # separate provider now
    exposedByDefault: false</pre>

<p>Most single-node setups don't use Swarm, so this doesn't apply. But if you had <code>swarmMode: false</code> in your Docker provider config, remove it — it'll cause a startup error in v3.</p>

<div class="cta">
  <p>Paste your docker-compose.yml or nginx.conf to detect Traefik v1 label patterns and get exact v3 replacements.</p>
  <a href="/proxy/">Open Reverse Proxy Mapper →</a>
</div>
"""

POST_5 = page(
    slug="traefik-v2-to-v3-migration",
    title="Traefik v2 to v3 Migration: What Actually Broke and How to Fix It",
    meta_desc="Traefik v3 breaking changes explained: Docker network requirements, removed allowEmptyServices, deprecated v1 labels, and the static config changes that cause startup failures.",
    keywords="traefik v2 to v3 migration, traefik v3 breaking changes, traefik v3 docker labels, traefik upgrade guide",
    date_str="2026-03-23",
    tags=["Traefik", "Docker", "Reverse Proxy", "Migration"],
    lede="Traefik v3 didn't rewrite everything — but what it did change breaks quietly. Routes stop working, no obvious error, and the label you've had in your compose file for two years just silently does nothing now.",
    body=POST_5_BODY,
)

# ─── BLOG INDEX ───────────────────────────────────────────────────────────────

POSTS_META = [
    {
        "slug": "docker-ufw-bypass-explained",
        "title": "Docker Bypasses UFW. Here's Why — and How to Fix It.",
        "desc": "UFW is active. You added a deny rule. Your Redis is still open. Here's what's actually happening and three ways to fix it.",
        "date": "2026-03-23",
        "tags": ["Docker", "UFW", "Security"],
    },
    {
        "slug": "cron-job-best-practices",
        "title": "Cron Job Best Practices That Actually Matter",
        "desc": "flock safety, staggered scheduling, output logging, PATH issues — the patterns that prevent silent failures.",
        "date": "2026-03-23",
        "tags": ["Cron", "Linux", "DevOps"],
    },
    {
        "slug": "ssl-certificate-monitoring-guide",
        "title": "SSL Certificate Monitoring: Why 30 Days Is Too Late",
        "desc": "The 200-day rule, CDN cert traps, and a simple bash script to catch expiry before it becomes an outage.",
        "date": "2026-03-23",
        "tags": ["SSL", "Monitoring", "DevOps"],
    },
    {
        "slug": "ollama-server-security",
        "title": "Securing an Ollama Server: Don't Leave Your GPU Open to the Internet",
        "desc": "Ollama binds to 0.0.0.0 by default. How to lock it down with localhost binding, Nginx auth, and Docker port safety.",
        "date": "2026-03-23",
        "tags": ["Ollama", "Security", "Self-hosted"],
    },
    {
        "slug": "traefik-v2-to-v3-migration",
        "title": "Traefik v2 to v3 Migration: What Actually Broke",
        "desc": "Docker network requirements, removed options, deprecated v1 labels, and the static config changes that cause startup failures.",
        "date": "2026-03-23",
        "tags": ["Traefik", "Docker", "Migration"],
    },
]

def build_blog_index():
    cards = "\n".join([
        f"""    <a href="/blog/{p['slug']}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">{p['date']} &nbsp;·&nbsp; {"&nbsp;".join([f'<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">{t}</span>' for t in p["tags"]])}</div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">{p['title']}</div>
      <div style="font-size:0.82rem;color:var(--muted);">{p['desc']}</div>
    </a>"""
        for p in POSTS_META
    ])

    blog_schema = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Blog",
    "name":"ConfigClarity Blog",
    "url":"https://configclarity.dev/blog/",
    "description":"Practical guides for Linux server management, Docker security, SSL monitoring, and DevOps.",
    "author":{"@type":"Organization","name":"MetricLogic","url":"https://metriclogic.dev"}
  }
  </script>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ConfigClarity Blog — Linux, Docker, SSL, DevOps</title>
  <meta name="description" content="Practical guides for Linux server management, Docker security, SSL monitoring, cron jobs, and DevOps. Written for sysadmins, not academics.">
  <meta name="keywords" content="linux server blog, docker security guide, ssl monitoring, devops blog, sysadmin tips">
  <link rel="canonical" href="https://configclarity.dev/blog/">
  <meta property="og:title" content="ConfigClarity Blog">
  <meta property="og:description" content="Practical guides for Linux server management, Docker, SSL, and DevOps.">
  <meta property="og:url" content="https://configclarity.dev/blog/">
  {FONT}
{blog_schema}
{CSS}
</head>
<body>
{HEADER}
  <div style="max-width:720px;margin:0 auto;padding:2rem;">
    <div style="font-size:0.75rem;color:var(--muted);margin-bottom:1.5rem;"><a href="/" style="color:var(--muted);">ConfigClarity</a> › Blog</div>
    <h1 style="font-size:1.6rem;font-weight:700;margin-bottom:0.5rem;">Blog</h1>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:2rem;">Practical guides for Linux server management, Docker security, SSL monitoring, and DevOps. Written for sysadmins, not academics.</p>
{cards}
  </div>
{FOOTER}
</body>
</html>"""


if __name__ == '__main__':
    print("=== Building Blog Posts ===\n")
    os.makedirs("blog", exist_ok=True)

    posts = [
        ("blog/index.html", build_blog_index()),
        ("blog/docker-ufw-bypass-explained/index.html", POST_1),
        ("blog/cron-job-best-practices/index.html", POST_2),
        ("blog/ssl-certificate-monitoring-guide/index.html", POST_3),
        ("blog/ollama-server-security/index.html", POST_4),
        ("blog/traefik-v2-to-v3-migration/index.html", POST_5),
    ]

    for path, html in posts:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(html)
        print(f"  ✅ {path} ({len(html):,} bytes)")

    # Update vercel.json
    import json
    with open('vercel.json', 'r') as f:
        config = json.load(f)

    blog_rewrites = [
        {"source": "/blog/", "destination": "/blog/index.html"},
        {"source": "/blog", "destination": "/blog/index.html"},
    ]
    for slug in [p["slug"] for p in POSTS_META]:
        blog_rewrites.append({"source": f"/blog/{slug}/", "destination": f"/blog/{slug}/index.html"})
        blog_rewrites.append({"source": f"/blog/{slug}", "destination": f"/blog/{slug}/index.html"})

    added = 0
    for rule in blog_rewrites:
        if rule not in config['rewrites']:
            config['rewrites'].append(rule)
            added += 1

    with open('vercel.json', 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\n  ✅ vercel.json — {added} blog rewrites added")

    # Update sitemap-seo.xml
    with open('sitemap-seo.xml', 'r') as f:
        sitemap = f.read()

    new_entries = "\n".join([
        f"""  <url>
    <loc>https://configclarity.dev/blog/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>""",
    ] + [
        f"""  <url>
    <loc>https://configclarity.dev/blog/{p['slug']}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
        for p in POSTS_META
    ])

    if "/blog/" not in sitemap:
        sitemap = sitemap.replace("</urlset>", new_entries + "\n</urlset>")
        with open('sitemap-seo.xml', 'w') as f:
            f.write(sitemap)
        print(f"  ✅ sitemap-seo.xml — 6 blog URLs added")

    # Update llms.txt
    with open('llms.txt', 'r') as f:
        llms = f.read()

    if "## Blog" not in llms:
        blog_lines = "\n## Blog\n" + "\n".join([
            f"- https://configclarity.dev/blog/{p['slug']}/"
            for p in POSTS_META
        ])
        with open('llms.txt', 'a') as f:
            f.write(blog_lines)
        print(f"  ✅ llms.txt — blog posts added")

    print(f"\nDone. 6 blog pages built.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: 5 blog posts in human voice' && git push origin main && npx vercel --prod --force")
    print("\nGSC Day 1 blog submissions:")
    print("  https://configclarity.dev/blog/")
    print("  https://configclarity.dev/blog/docker-ufw-bypass-explained/")
    print("  https://configclarity.dev/blog/cron-job-best-practices/")
    print("  https://configclarity.dev/blog/ssl-certificate-monitoring-guide/")
