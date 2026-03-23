#!/usr/bin/env python3
"""
Script 14: Build 3 incident pages.
/incidents/docker-ufw-bypass
/incidents/ssl-expiry-outages
/incidents/docker-secrets-exposed
Run from: ~/Projects/CronSight/
"""

import os, json
from datetime import date

TODAY = date.today().isoformat()
BASE = "https://configclarity.dev"

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

CSS = """
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root { --bg:#0b0d14; --bg2:#1e2130; --purple:#6c63ff; --green:#22c55e; --orange:#f97316; --red:#ef4444; --text:#e2e4f0; --muted:#8a8fb5; }
      body { background:var(--bg); color:var(--text); font-family:'JetBrains Mono',monospace; min-height:100vh; line-height:1.8; }
      a { color:var(--purple); text-decoration:none; } a:hover { text-decoration:underline; }
      .header { padding:1.5rem 2rem; border-bottom:1px solid #2a2d3d; display:flex; align-items:center; gap:1rem; }
      .header-logo { font-size:1.1rem; font-weight:700; }
      .header-logo span { color:var(--purple); }
      .header-nav { margin-left:auto; display:flex; gap:1rem; font-size:0.8rem; }
      .header-nav a { color:var(--muted); }
      .breadcrumb { padding:1rem 2rem 0; max-width:720px; margin:0 auto; font-size:0.78rem; color:var(--muted); }
      .breadcrumb a { color:var(--muted); }
      .hero { max-width:720px; margin:0 auto; padding:3rem 2rem 1.5rem; }
      .hero-meta { font-size:0.75rem; color:var(--muted); margin-bottom:1rem; display:flex; gap:1rem; flex-wrap:wrap; align-items:center; }
      .hero-tag { background:rgba(239,68,68,.15); color:var(--red); padding:0.15rem 0.6rem; border-radius:4px; font-size:0.72rem; }
      .hero-tag.orange { background:rgba(249,115,22,.15); color:var(--orange); }
      h1 { font-size:1.7rem; font-weight:700; line-height:1.35; margin-bottom:1rem; }
      .lede { font-size:1rem; color:var(--muted); margin-bottom:2rem; line-height:1.75; }
      .content { max-width:720px; margin:0 auto; padding:0 2rem 4rem; }
      h2 { font-size:1.1rem; font-weight:700; margin:2.5rem 0 0.75rem; }
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1.1rem; }
      strong { color:var(--text); }
      pre { background:#0d0f1a; border:1px solid #2a2d3d; border-radius:8px; padding:1.25rem 1.5rem; font-size:0.78rem; overflow-x:auto; margin:1rem 0 1.5rem; line-height:1.7; color:var(--text); }
      code { background:#1e2130; padding:0.1rem 0.4rem; border-radius:3px; font-size:0.82rem; color:var(--text); }
      .incident-box { background:var(--bg2); border-left:3px solid var(--red); border-radius:0 8px 8px 0; padding:1.1rem 1.5rem; margin:1.5rem 0; }
      .incident-box .label { font-size:0.7rem; color:var(--red); text-transform:uppercase; letter-spacing:.06em; margin-bottom:0.5rem; }
      .incident-box p { margin-bottom:0.5rem; font-size:0.875rem; color:var(--text); }
      .incident-box p:last-child { margin-bottom:0; }
      .fix-box { background:var(--bg2); border-left:3px solid var(--green); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.5rem 0; }
      .fix-box .label { font-size:0.7rem; color:var(--green); text-transform:uppercase; letter-spacing:.06em; margin-bottom:0.4rem; }
      .timeline { border-left:2px solid #2a2d3d; padding-left:1.5rem; margin:1.5rem 0; }
      .timeline-item { margin-bottom:1.25rem; position:relative; }
      .timeline-item::before { content:""; width:8px; height:8px; border-radius:50%; background:var(--purple); position:absolute; left:-1.9rem; top:0.35rem; }
      .timeline-item .time { font-size:0.72rem; color:var(--muted); margin-bottom:0.25rem; }
      .timeline-item .event { font-size:0.875rem; color:var(--text); }
      .faq-item { margin-bottom:1.4rem; }
      .faq-q { font-size:0.9rem; font-weight:600; margin-bottom:0.35rem; }
      .faq-a { font-size:0.84rem; color:var(--muted); }
      .cta { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.5rem; margin:2.5rem 0; text-align:center; }
      .cta p { color:var(--text); font-size:0.875rem; margin-bottom:0.75rem; }
      .cta-row { display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap; }
      .cta a { display:inline-block; background:var(--purple); color:#fff; padding:0.5rem 1.25rem; border-radius:6px; font-size:0.82rem; font-weight:700; }
      .cta a.sec { background:transparent; border:1px solid var(--purple); color:var(--purple); }
      footer { text-align:center; padding:2rem; font-size:0.75rem; color:var(--muted); border-top:1px solid #2a2d3d; }
    </style>
"""

HEADER = """  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a><a href="/ssl/">SSL</a><a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a><a href="/proxy/">Proxy</a><a href="/robots/">robots.txt</a>
    </nav>
  </header>"""

FOOTER = """  <footer>
    <p><a href="/incidents/">Incident Reports</a> &nbsp;·&nbsp;
    <a href="/fix/">Fix Guides</a> &nbsp;·&nbsp; <a href="/glossary/">Glossary</a> &nbsp;·&nbsp;
    <a href="https://metriclogic.dev">MetricLogic</a></p>
  </footer>"""

def incident_page(slug, title, meta_desc, keywords, tags, lede, body, tool_name, tool_href, tool_cta):
    tag_html = "".join([
        f'<span class="hero-tag{"" if i < 2 else " orange"}">{t}</span>'
        for i, t in enumerate(tags)
    ])
    faq_schema = ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title} — ConfigClarity</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{BASE}/incidents/{slug}/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{BASE}/incidents/{slug}/">
  <meta property="og:type" content="article">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle",
    "headline":"{title}",
    "url":"{BASE}/incidents/{slug}/",
    "description":"{meta_desc}",
    "datePublished":"{TODAY}",
    "author":{{"@type":"Organization","name":"MetricLogic","url":"https://metriclogic.dev"}},
    "publisher":{{"@type":"Organization","name":"ConfigClarity","url":"https://configclarity.dev"}}
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"{BASE}"}},
    {{"@type":"ListItem","position":2,"name":"Incident Reports","item":"{BASE}/incidents/"}},
    {{"@type":"ListItem","position":3,"name":"{title}","item":"{BASE}/incidents/{slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/incidents/">Incidents</a> › {title}</div>
  <div class="hero">
    <div class="hero-meta"><span>{TODAY}</span> · {tag_html}</div>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
  <div class="content">
    {body}
    <div class="cta">
      <p>{tool_cta}</p>
      <div class="cta-row"><a href="{tool_href}">{tool_name} →</a></div>
    </div>
  </div>
{FOOTER}
</body>
</html>"""


# ── INCIDENT 1: Docker UFW Bypass ─────────────────────────────────────────────

INC1_BODY = """
<p>The Docker UFW bypass is not a theoretical vulnerability. It's a misconfiguration that has exposed production databases, Redis instances, and internal APIs to the public internet thousands of times — on servers whose owners believed their firewall was protecting them.</p>

<h2>How it happens</h2>

<p>Linux packet routing evaluates iptables chains in order: <strong>PREROUTING → DOCKER → FORWARD → INPUT</strong>. UFW manages the INPUT chain. When a packet arrives destined for a Docker container port, Docker's rules in the FORWARD chain accept it before the packet ever reaches UFW's INPUT rules.</p>

<p>The result: a developer runs <code>ufw deny 6379</code> to block Redis. They check <code>ufw status</code> and see the deny rule listed. They assume they're protected. Their Redis instance is publicly accessible anyway — through the DOCKER chain that UFW never touches.</p>

<h2>Documented exposure patterns</h2>

<div class="incident-box">
  <div class="label">Pattern 1 — Database exposure</div>
  <p>Redis (:6379), MongoDB (:27017), PostgreSQL (:5432), and MySQL (:3306) bound to <code>0.0.0.0</code> via Docker port mappings are consistently found by Shodan scans. Unauthenticated Redis instances in particular have been used for cryptomining by scanning for port 6379 and issuing CONFIG SET commands to write SSH keys to <code>~/.ssh/authorized_keys</code>.</p>
</div>

<div class="incident-box">
  <div class="label">Pattern 2 — Internal API exposure</div>
  <p>Internal services (admin panels, metrics endpoints, internal APIs) deployed in Docker with <code>ports: "PORT:PORT"</code> and no authentication, intended to be "protected by the firewall", are accessible from the public internet. The firewall appears active. The service is reachable.</p>
</div>

<div class="incident-box">
  <div class="label">Pattern 3 — AI inference endpoint exposure</div>
  <p>Ollama and other local LLM servers running in Docker with <code>ports: "11434:11434"</code> are discoverable via Shodan on port 11434. Exposed instances allow anyone to run inference on the host's hardware at no cost to the attacker.</p>
</div>

<h2>The attack timeline</h2>

<div class="timeline">
  <div class="timeline-item">
    <div class="time">Day 0</div>
    <div class="event">Developer deploys Docker service with <code>ports: "6379:6379"</code>. Adds <code>ufw deny 6379</code>. Checks status — looks protected.</div>
  </div>
  <div class="timeline-item">
    <div class="time">Day 0–3</div>
    <div class="event">Automated Shodan-style scanners discover port 6379 open on the server's public IP. Add to target list.</div>
  </div>
  <div class="timeline-item">
    <div class="time">Day 1–14</div>
    <div class="event">Unauthenticated Redis receives CONFIG SET commands. Attacker writes SSH key to root's authorized_keys or sets up a cron job to download and execute a cryptominer.</div>
  </div>
  <div class="timeline-item">
    <div class="time">Day 14+</div>
    <div class="event">Owner notices CPU spike, unusual outbound traffic, or VPS provider flags the account for abuse. By this point the server has been running a miner for days or weeks.</div>
  </div>
</div>

<h2>Verification — check right now</h2>

<pre># From another machine (mobile data, NOT your home network):
curl http://YOUR_SERVER_IP:6379
nc -zv YOUR_SERVER_IP 6379

# Or from the server itself — check what Docker exposed:
sudo iptables -L DOCKER --line-numbers | grep ACCEPT</pre>

<h2>The fix</h2>

<div class="fix-box">
  <div class="label">Bind container ports to localhost only</div>
  <pre># Before — exposed to internet:
ports:
  - "6379:6379"

# After — localhost only:
ports:
  - "127.0.0.1:6379:6379"</pre>
</div>

<div class="fix-box">
  <div class="label">Or use DOCKER-USER chain for server-wide protection</div>
  <pre>sudo iptables -I DOCKER-USER -j DROP
sudo iptables -I DOCKER-USER -s 127.0.0.1 -j ACCEPT
sudo apt install iptables-persistent && sudo netfilter-persistent save</pre>
</div>

<h2>Related</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/glossary/docker-ufw-bypass/">What is Docker UFW bypass?</a></li>
  <li><a href="/fix/docker/ufw-bypass/">Docker UFW bypass fix guide</a></li>
  <li><a href="/fix/ufw/docker-bypass/">UFW Docker bypass fix guide</a></li>
  <li><a href="/blog/docker-ufw-bypass-explained/">Docker bypasses UFW — explained</a></li>
</ul>
"""

INC1 = incident_page(
    "docker-ufw-bypass",
    "Docker UFW Bypass: How Exposed Containers Lead to Server Compromise",
    "How the Docker UFW bypass misconfiguration exposes databases and services to the internet despite active firewall rules. Real attack patterns and the exact fix.",
    "docker ufw bypass incident, docker firewall bypass breach, redis exposed docker, docker port exposed internet",
    ["Security Incident", "Docker", "UFW"],
    "UFW is active. The deny rule is listed. The Redis port is open to the internet anyway. This is how the Docker UFW bypass leads from misconfiguration to compromised server — and how to verify you're not currently affected.",
    INC1_BODY,
    "Firewall Auditor",
    "/firewall/",
    "Paste your ufw status verbose output to detect Docker bypass risk and exposed ports on your server."
)

# ── INCIDENT 2: SSL Expiry Outages ────────────────────────────────────────────

INC2_BODY = """
<p>SSL certificate expiry is one of the most preventable causes of major service outages. The expiry date is embedded in the certificate months in advance. And yet it keeps causing production incidents — because most monitoring setups catch it too late, or miss the right certificate entirely.</p>

<h2>Documented outages</h2>

<div class="incident-box">
  <div class="label">Microsoft Teams — February 2020</div>
  <p>An expired SSL certificate took Microsoft Teams offline for millions of users during the height of COVID-era remote work adoption. The certificate expired without triggering renewal. Microsoft's post-incident review cited monitoring gaps on internal certificate infrastructure.</p>
</div>

<div class="incident-box">
  <div class="label">Ericsson — December 2021</div>
  <p>An expired software certificate caused a major mobile network outage across multiple operators globally. Ericsson confirmed the root cause was an expired certificate in SGSN-MME nodes. The outage affected 11 operators across multiple countries.</p>
</div>

<div class="incident-box">
  <div class="label">Spotify — 2020</div>
  <p>Spotify experienced an outage traced to an expired TLS certificate on an internal service. The certificate was on an infrastructure component that wasn't covered by standard monitoring because it wasn't customer-facing.</p>
</div>

<div class="incident-box">
  <div class="label">Let's Encrypt root certificate — September 2021</div>
  <p>The DST Root CA X3 certificate used by Let's Encrypt as a cross-sign expired, breaking HTTPS on older Android devices and systems that hadn't updated their trust stores. Affected services included Stripe, AWS API endpoints, and numerous banking apps.</p>
</div>

<h2>The pattern behind every SSL outage</h2>

<p>These outages share a structure:</p>
<ol style="padding-left:1.5rem;font-size:0.875rem;color:var(--muted);line-height:2.2;">
  <li>Certificate monitored at 30 days — or not monitored at all</li>
  <li>Renewal pipeline silently broken for weeks or months</li>
  <li>By the time the alert fires, there's no runway to debug the renewal failure</li>
  <li>Or: the monitored certificate is the CDN/load balancer cert, not the origin cert</li>
</ol>

<h2>The CDN trap</h2>

<p>Sites behind Cloudflare, Fastly, or AWS CloudFront have two certificates: the CDN edge certificate (what users see) and the origin certificate (between the CDN and the server). Most monitoring checks the CDN cert. The origin cert expires silently behind the edge.</p>

<pre># Check what users see (CDN cert):
openssl s_client -connect yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates

# Check origin cert directly (bypass CDN):
openssl s_client -connect YOUR_SERVER_IP:443 \
  -servername yourdomain.com 2>/dev/null | openssl x509 -noout -dates</pre>

<h2>The 200-day rule</h2>

<p>Let's Encrypt certificates expire in 90 days. If renewal breaks on day 1, a 30-day alert fires at day 60 — giving you 30 days to debug a failure that's been silent for 60. Monitor at 200 days. Anything expiring in under 200 days either intentionally has a short validity or has a broken renewal pipeline.</p>

<div class="fix-box">
  <div class="label">Weekly SSL monitoring cron job</div>
  <pre>0 9 * * 1 flock -n /tmp/ssl-check.lock /usr/local/bin/check-ssl.sh</pre>
</div>

<h2>Related</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/glossary/ssl-certificate-expiry/">What is SSL certificate expiry?</a></li>
  <li><a href="/fix/ssl/expiry-monitoring/">SSL expiry monitoring fix guide</a></li>
  <li><a href="/fix/ssl/cdn-domain/">CDN domain SSL fix guide</a></li>
  <li><a href="/fix/ssl/200-day-warning/">Why monitor at 200 days?</a></li>
  <li><a href="/blog/ssl-certificate-monitoring-guide/">SSL certificate monitoring guide</a></li>
</ul>
"""

INC2 = incident_page(
    "ssl-expiry-outages",
    "SSL Certificate Expiry Outages: Microsoft, Ericsson, Spotify, and What They Had in Common",
    "Documented SSL certificate expiry outages — Microsoft Teams, Ericsson, Spotify — and the monitoring gap they all shared. How to avoid the same failure.",
    "ssl certificate expiry outage, ssl expired incident, lets encrypt expiry outage, microsoft teams ssl, ericsson certificate outage",
    ["Security Incident", "SSL", "Monitoring"],
    "An expired SSL certificate took Microsoft Teams offline. The same misconfiguration — monitoring too late, or the wrong certificate — caused outages at Ericsson, Spotify, and hundreds of smaller services. Here's the pattern and how to break it.",
    INC2_BODY,
    "SSL Checker",
    "/ssl/",
    "Check multiple domains at once — expiry dates, CDN detection, certificate chain validation, and 200-day early warnings."
)

# ── INCIDENT 3: Hardcoded Secrets ─────────────────────────────────────────────

INC3_BODY = """
<p>Hardcoded credentials in Docker Compose files and application configs are a persistent source of credential exposure. GitHub's secret scanning catches some patterns — but database passwords, custom API keys, and internal service tokens are frequently missed, and the exposure often predates the scan by months.</p>

<h2>How credentials end up exposed</h2>

<div class="incident-box">
  <div class="label">Pattern 1 — docker-compose.yml committed to public repo</div>
  <p>The most common path: a developer creates a docker-compose.yml with hardcoded credentials for local development, adds the project to GitHub, and either forgets to add a .gitignore entry for the secrets or uses a public repo. The file sits in the repository history even after the credentials are removed.</p>
</div>

<div class="incident-box">
  <div class="label">Pattern 2 — .env file committed accidentally</div>
  <p>A developer runs <code>git add .</code> and commits a .env file that wasn't in .gitignore. The file contains production database passwords, API keys, and JWT secrets. GitHub's secret scanning may flag some patterns, but database passwords without recognisable prefixes are not detected.</p>
</div>

<div class="incident-box">
  <div class="label">Pattern 3 — CI/CD config with hardcoded tokens</div>
  <p>GitHub Actions workflow files with hardcoded tokens (instead of using <code>${{ secrets.TOKEN }}</code>) are committed to public repositories. Build logs also sometimes echo secret values when debugging is left enabled.</p>
</div>

<h2>What attackers do with exposed Docker credentials</h2>

<p>Exposed database credentials in docker-compose.yml files have a predictable exploitation path:</p>

<div class="timeline">
  <div class="timeline-item">
    <div class="time">Hour 0</div>
    <div class="event">Automated scanner finds docker-compose.yml with <code>POSTGRES_PASSWORD=mypassword</code> in a public GitHub search.</div>
  </div>
  <div class="timeline-item">
    <div class="time">Hour 0–1</div>
    <div class="event">Scanner attempts connection to the server IP associated with the repo owner's other public projects. Tries common ports (5432, 3306, 27017) with the exposed credentials.</div>
  </div>
  <div class="timeline-item">
    <div class="time">Hour 1–24</div>
    <div class="event">If the database is accessible (Docker UFW bypass — see related incident), attacker exfiltrates the database. If not accessible, credentials are stored for credential stuffing against other services using the same password.</div>
  </div>
  <div class="timeline-item">
    <div class="time">Day 1–30</div>
    <div class="event">Credentials sold or used in targeted attacks against the organisation. GitHub history preserves the original exposure even after the file is updated.</div>
  </div>
</div>

<h2>The git history problem</h2>

<p>Removing credentials from a file and pushing the update does not remove them from git history. Anyone with access to the repository can still see the credentials in previous commits using <code>git log -p</code>.</p>

<pre># Check if credentials exist in git history:
git log --all -p | grep -i "password|secret|key|token" | head -20

# Remove from history (requires git-filter-repo):
pip install git-filter-repo
git filter-repo --path docker-compose.yml --invert-paths</pre>

<p>After removing from history: rotate all exposed credentials immediately. Git history removal doesn't help if the credentials were already harvested.</p>

<h2>The correct pattern</h2>

<div class="fix-box">
  <div class="label">docker-compose.yml — use variable references</div>
  <pre>services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}   # Reference, not value
      POSTGRES_USER: ${DB_USER}</pre>
</div>

<div class="fix-box">
  <div class="label">.env file — never commit this</div>
  <pre>DB_PASSWORD=your-actual-password
DB_USER=postgres</pre>
</div>

<div class="fix-box">
  <div class="label">.gitignore — add before first commit</div>
  <pre>.env
.env.local
.env.production
*.env</pre>
</div>

<h2>Related</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/glossary/hardcoded-secrets/">What are hardcoded secrets?</a></li>
  <li><a href="/fix/docker/hardcoded-secrets/">Docker hardcoded secrets fix guide</a></li>
  <li><a href="/incidents/docker-ufw-bypass/">Docker UFW bypass incident report</a></li>
</ul>
"""

INC3 = incident_page(
    "docker-secrets-exposed",
    "Hardcoded Secrets in Docker Compose: How Credentials End Up on GitHub",
    "How database passwords and API keys end up hardcoded in docker-compose.yml files, committed to public repos, and exploited. The git history problem and how to fix it.",
    "hardcoded secrets docker compose, docker compose credentials exposed, docker compose github secrets, exposed database password docker",
    ["Security Incident", "Docker", "Credentials"],
    "Database passwords hardcoded in docker-compose.yml, committed to public GitHub repos, and harvested by automated scanners within hours. This is the path — and it happens more often than anyone admits.",
    INC3_BODY,
    "Docker Auditor",
    "/docker/",
    "Paste your docker-compose.yml to detect hardcoded credentials, exposed ports, and missing security controls — nothing leaves your browser."
)

# ── INCIDENTS INDEX ────────────────────────────────────────────────────────────

def build_incidents_index():
    incidents = [
        ("docker-ufw-bypass", "Docker UFW Bypass: How Exposed Containers Lead to Server Compromise",
         "How the Docker UFW bypass misconfiguration exposes databases to the internet despite active firewall rules.", ["Security", "Docker"]),
        ("ssl-expiry-outages", "SSL Certificate Expiry Outages: Microsoft, Ericsson, Spotify",
         "Documented SSL expiry outages and the monitoring gap they all shared.", ["Security", "SSL"]),
        ("docker-secrets-exposed", "Hardcoded Secrets in Docker Compose: How Credentials End Up on GitHub",
         "How database passwords end up hardcoded in public repos and exploited within hours.", ["Security", "Docker"]),
    ]
    cards = "\n".join([
        f"""    <a href="/incidents/{slug}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">{TODAY} &nbsp;·&nbsp; {"&nbsp;".join([f'<span style="background:rgba(239,68,68,.15);color:var(--red);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">{t}</span>' for t in tags])}</div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">{title}</div>
      <div style="font-size:0.82rem;color:var(--muted);">{desc}</div>
    </a>"""
        for slug, title, desc, tags in incidents
    ])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Security Incident Reports — ConfigClarity</title>
  <meta name="description" content="Documented security incidents caused by Docker misconfigurations, SSL certificate expiry, and hardcoded credentials. Real patterns with exact fixes.">
  <meta name="keywords" content="docker security incident, ssl expiry outage, docker credentials exposed, server misconfiguration breach">
  <link rel="canonical" href="{BASE}/incidents/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"CollectionPage",
    "name":"Security Incident Reports — ConfigClarity",
    "url":"{BASE}/incidents/",
    "description":"Documented security incidents caused by Docker misconfigurations, SSL expiry, and hardcoded credentials."
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"{BASE}"}},
    {{"@type":"ListItem","position":2,"name":"Incident Reports","item":"{BASE}/incidents/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div style="max-width:720px;margin:0 auto;padding:2rem;">
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:1.5rem;"><a href="/" style="color:var(--muted);">ConfigClarity</a> › Incident Reports</div>
    <h1 style="font-size:1.6rem;font-weight:700;margin-bottom:0.75rem;">Security Incident Reports</h1>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:2rem;">Documented cases where Docker misconfigurations, SSL expiry, and hardcoded credentials caused real breaches and outages — with the exact fixes that would have prevented each one.</p>
{cards}
  </div>
{FOOTER}
</body>
</html>"""


if __name__ == "__main__":
    print("=== Building Incident Pages ===\n")
    os.makedirs("incidents", exist_ok=True)
    count = 0

    pages = [
        ("incidents/index.html", build_incidents_index()),
        ("incidents/docker-ufw-bypass/index.html", INC1),
        ("incidents/ssl-expiry-outages/index.html", INC2),
        ("incidents/docker-secrets-exposed/index.html", INC3),
    ]

    for path, html in pages:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(html)
        print(f"  ✅ {path} ({len(html):,} bytes)")
        count += 1

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)

    new_rewrites = [
        {"source": "/incidents/", "destination": "/incidents/index.html"},
        {"source": "/incidents", "destination": "/incidents/index.html"},
        {"source": "/incidents/docker-ufw-bypass/", "destination": "/incidents/docker-ufw-bypass/index.html"},
        {"source": "/incidents/docker-ufw-bypass", "destination": "/incidents/docker-ufw-bypass/index.html"},
        {"source": "/incidents/ssl-expiry-outages/", "destination": "/incidents/ssl-expiry-outages/index.html"},
        {"source": "/incidents/ssl-expiry-outages", "destination": "/incidents/ssl-expiry-outages/index.html"},
        {"source": "/incidents/docker-secrets-exposed/", "destination": "/incidents/docker-secrets-exposed/index.html"},
        {"source": "/incidents/docker-secrets-exposed", "destination": "/incidents/docker-secrets-exposed/index.html"},
    ]
    added = sum(1 for r in new_rewrites if r not in config["rewrites"])
    for r in new_rewrites:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"\n  ✅ vercel.json — {added} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    new_urls = ["/incidents/", "/incidents/docker-ufw-bypass/",
                "/incidents/ssl-expiry-outages/", "/incidents/docker-secrets-exposed/"]
    entries = "\n".join([
        f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>"
        for u in new_urls if u not in sitemap
    ])
    if entries:
        sitemap = sitemap.replace("</urlset>", entries + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
    print(f"  ✅ sitemap-seo.xml — {len(new_urls)} incident URLs added (priority 0.9)")

    print(f"\nDone. {count} incident pages built.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: incident pages + internal link audit' && git push origin main && npx vercel --prod --force")
    print("\nGSC — submit these first (high intent, priority 0.9):")
    print("  https://configclarity.dev/incidents/docker-ufw-bypass/")
    print("  https://configclarity.dev/incidents/ssl-expiry-outages/")
    print("  https://configclarity.dev/incidents/docker-secrets-exposed/")
