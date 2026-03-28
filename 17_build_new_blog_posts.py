#!/usr/bin/env python3
"""
Script 17: Build 3 new high-priority blog posts.
1. Fail2ban misconfiguration
2. Docker Compose security checklist
3. Traefik v3 what broke in the wild
Run from: ~/Projects/CronSight/
"""

import os, json

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

CSS = """
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root { --bg:#0b0d14; --bg2:#1e2130; --purple:#6c63ff; --green:#22c55e; --orange:#f97316; --red:#ef4444; --text:#e2e4f0; --muted:#8a8fb5; }
      body { background:var(--bg); color:var(--text); font-family:'JetBrains Mono',monospace; min-height:100vh; line-height:1.8; }
      a { color:var(--purple); text-decoration:none; } a:hover { text-decoration:underline; }
      .header { padding:1.5rem 2rem; border-bottom:1px solid #2a2d3d; display:flex; align-items:center; gap:1rem; }
      .header-logo { font-size:1.1rem; font-weight:700; color:var(--text); }
      .header-logo span { color:var(--purple); }
      .header-nav { margin-left:auto; display:flex; gap:1rem; font-size:0.8rem; }
      .header-nav a { color:var(--muted); }
      .breadcrumb { padding:1rem 2rem 0; max-width:720px; margin:0 auto; font-size:0.78rem; color:var(--muted); }
      .breadcrumb a { color:var(--muted); }
      .hero { max-width:720px; margin:0 auto; padding:3rem 2rem 1.5rem; }
      .hero-meta { font-size:0.75rem; color:var(--muted); margin-bottom:1rem; display:flex; gap:1rem; flex-wrap:wrap; align-items:center; }
      .hero-tag { background:rgba(108,99,255,.15); color:var(--purple); padding:0.15rem 0.6rem; border-radius:4px; font-size:0.72rem; }
      h1 { font-size:1.75rem; font-weight:700; line-height:1.35; margin-bottom:1rem; }
      .lede { font-size:1rem; color:var(--muted); margin-bottom:2rem; line-height:1.75; }
      .content { max-width:720px; margin:0 auto; padding:0 2rem 4rem; }
      h2 { font-size:1.15rem; font-weight:700; margin:2.5rem 0 0.75rem; }
      h3 { font-size:0.95rem; font-weight:700; margin:1.75rem 0 0.5rem; }
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1.1rem; }
      strong { color:var(--text); }
      pre { background:#0d0f1a; border:1px solid #2a2d3d; border-radius:8px; padding:1.25rem 1.5rem; font-size:0.78rem; overflow-x:auto; margin:1rem 0 1.5rem; line-height:1.7; color:var(--text); }
      code { background:#1e2130; padding:0.1rem 0.4rem; border-radius:3px; font-size:0.82rem; color:var(--text); }
      .callout { background:var(--bg2); border-left:3px solid var(--orange); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.5rem 0; }
      .callout.danger { border-color:var(--red); }
      .callout.good { border-color:var(--green); }
      .callout p { margin-bottom:0; color:var(--text); font-size:0.875rem; }
      .checklist { list-style:none; padding:0; margin:1rem 0 1.5rem; }
      .checklist li { font-size:0.875rem; color:var(--muted); padding:0.6rem 0; border-bottom:1px solid #1a1c26; display:flex; gap:0.75rem; align-items:flex-start; line-height:1.6; }
      .checklist li:last-child { border-bottom:none; }
      .checklist li::before { content:"☐"; color:var(--purple); flex-shrink:0; font-size:1rem; }
      .cta { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.5rem; margin:2.5rem 0; text-align:center; }
      .cta p { color:var(--text); font-size:0.875rem; margin-bottom:0.75rem; }
      .cta-row { display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap; }
      .cta a { display:inline-block; background:var(--purple); color:#fff; padding:0.5rem 1.25rem; border-radius:6px; font-size:0.82rem; font-weight:700; text-decoration:none; }
      .cta a.sec { background:transparent; border:1px solid var(--purple); color:var(--purple); }
      footer { text-align:center; padding:2rem; font-size:0.75rem; color:var(--muted); border-top:1px solid #2a2d3d; }
    </style>
"""

HEADER = """  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a><a href="/ssl/">SSL</a><a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a><a href="/proxy/">Proxy</a><a href="/robots/">robots.txt</a>
      <a href="/blog/" style="color:var(--purple);">Blog</a>
    </nav>
  </header>"""

FOOTER = """  <footer>
    <p>Part of the <a href="https://metriclogic.dev">MetricLogic</a> network &nbsp;·&nbsp;
    <a href="/blog/">More articles</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>"""

def build_page(slug, title, meta_desc, keywords, date_str, tags, lede, body):
    tag_html = "".join([f'<span class="hero-tag">{t}</span>' for t in tags])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title} — ConfigClarity</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="https://configclarity.dev/blog/{slug}/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="https://configclarity.dev/blog/{slug}/">
  <meta property="og:type" content="article">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article",
    "headline":"{title}",
    "description":"{meta_desc}",
    "url":"https://configclarity.dev/blog/{slug}/",
    "datePublished":"{date_str}",
    "dateModified":"{date_str}",
    "author":{{"@type":"Organization","name":"MetricLogic","url":"https://metriclogic.dev"}},
    "publisher":{{"@type":"Organization","name":"ConfigClarity","url":"https://configclarity.dev"}},
    "isPartOf":{{"@type":"Blog","name":"ConfigClarity Blog","url":"https://configclarity.dev/blog/"}}
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"https://configclarity.dev/blog/"}},
    {{"@type":"ListItem","position":3,"name":"{title}","item":"https://configclarity.dev/blog/{slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › {title}</div>
  <div class="hero">
    <div class="hero-meta"><span>{date_str}</span> · {tag_html}</div>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
  <div class="content">{body}</div>
{FOOTER}
</body>
</html>"""


# ── POST 1: Fail2ban ──────────────────────────────────────────────────────────

POST1_BODY = """
<p>Fail2ban is one of those tools that gets installed once and never looked at again. It shows up in every "secure your VPS" guide. People install it, see the service is running, and assume they're protected.</p>

<p>Most of the time they're not. The default configuration is wrong for modern Ubuntu servers, the ban times are too short to matter, and the most common setup has a gap that lets brute force attacks run for hours before a single ban fires.</p>

<p>Here's how to check your setup in 5 minutes.</p>

<h2>Check 1: Is fail2ban actually running?</h2>

<pre>sudo systemctl status fail2ban
sudo fail2ban-client status</pre>

<p>The second command is the important one. It shows you active jails. If you see <code>|- Number of jail: 0</code> — fail2ban is running but protecting nothing. No jails means no bans.</p>

<h2>Check 2: Is the SSH jail active?</h2>

<pre>sudo fail2ban-client status sshd</pre>

<p>If this returns <code>ERROR No such jail: sshd</code> — your SSH port is completely unprotected by fail2ban despite the service running.</p>

<p>On Ubuntu 22.04 with systemd, the default jail name is <code>sshd</code>. On older configs it might be <code>ssh</code>. If neither works, your SSH jail is not configured.</p>

<h2>Check 3: What backend is fail2ban using?</h2>

<pre>grep "backend" /etc/fail2ban/jail.conf /etc/fail2ban/jail.local 2>/dev/null</pre>

<p>On Ubuntu 20.04+, the correct backend is <code>systemd</code> because SSH logs go to the journal, not to <code>/var/log/auth.log</code>. If fail2ban is configured with <code>backend = auto</code> or <code>backend = polling</code> on a systemd server, it may be reading the wrong log source and missing all SSH login attempts.</p>

<div class="callout danger">
  <p><strong>This is the most common misconfiguration:</strong> fail2ban is running, the sshd jail is active, but it is reading from <code>/var/log/auth.log</code> on a server where SSH logs only go to journald. Zero bans fire. Zero protection.</p>
</div>

<h2>Check 4: Are your ban times long enough to matter?</h2>

<pre>sudo fail2ban-client get sshd bantime
sudo fail2ban-client get sshd maxretry
sudo fail2ban-client get sshd findtime</pre>

<p>Default values: <code>bantime = 10m</code>, <code>maxretry = 5</code>, <code>findtime = 10m</code>.</p>

<p>10 minutes is not a deterrent. A distributed brute force attack rotates IPs. Ban an IP for 10 minutes and the attacker just waits or switches. A useful ban time is at least <code>1h</code> — better is <code>1d</code> for repeat offenders using recidive jail.</p>

<h2>The correct configuration for Ubuntu 22.04</h2>

<p>Create or edit <code>/etc/fail2ban/jail.local</code> — never edit <code>jail.conf</code> directly, it gets overwritten on updates.</p>

<pre># /etc/fail2ban/jail.local
[DEFAULT]
bantime  = 1h
findtime = 10m
maxretry = 3
backend  = systemd

[sshd]
enabled  = true
port     = ssh
logpath  = %(sshd_log)s
backend  = %(sshd_backend)s
maxretry = 3
bantime  = 24h

[recidive]
enabled  = true
logpath  = /var/log/fail2ban.log
banaction = %(banaction_allports)s
bantime  = 1w
findtime = 1d
maxretry = 5</pre>

<p>The <code>recidive</code> jail bans IPs that have been banned multiple times — for a full week, on all ports. This is the configuration that actually stops persistent attackers.</p>

<pre>sudo systemctl restart fail2ban
sudo fail2ban-client status sshd
# Should show: Currently banned: 0, Total banned: N</pre>

<h2>Check 5: Is your SSH port in the ban list?</h2>

<p>If you changed your SSH port from 22, fail2ban's sshd jail needs to know. By default it only watches port 22.</p>

<pre># Check your SSH port:
grep "^Port" /etc/ssh/sshd_config

# If it's not 22, update jail.local:
[sshd]
port = 2222  # Your actual SSH port</pre>

<h2>Check 6: Is localhost ignored?</h2>

<pre>sudo fail2ban-client get sshd ignoreip</pre>

<p>Should include <code>127.0.0.1/8 ::1</code>. If you've locked yourself out before by accidentally triggering a ban on your own IP, add your static IP or home network here.</p>

<div class="cta">
  <p>Paste your <code>ufw status verbose</code> to audit firewall rules alongside your fail2ban setup — UFW and fail2ban work together but can have gaps.</p>
  <div class="cta-row">
    <a href="/firewall/">Firewall Auditor →</a>
  </div>
</div>

<h2>Quick audit script</h2>

<pre>#!/bin/bash
echo "=== Fail2ban Status ==="
systemctl is-active fail2ban

echo "=== Active Jails ==="
fail2ban-client status 2>/dev/null | grep "Jail list"

echo "=== SSH Jail ==="
fail2ban-client status sshd 2>/dev/null || echo "sshd jail NOT active"

echo "=== Ban Settings ==="
fail2ban-client get sshd bantime 2>/dev/null
fail2ban-client get sshd maxretry 2>/dev/null
fail2ban-client get sshd findtime 2>/dev/null

echo "=== Backend ==="
grep -h "backend" /etc/fail2ban/jail.local /etc/fail2ban/jail.conf 2>/dev/null | head -3</pre>

<p>Run this on any server you manage. If you see missing jails, wrong backend, or 10-minute ban times — fix them before the next scan hits your SSH port.</p>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/glossary/docker-ufw-bypass/">Docker UFW bypass — why fail2ban alone is not enough</a></li>
  <li><a href="/fix/ufw/default-deny-missing/">UFW default-deny missing fix</a></li>
  <li><a href="/blog/docker-ufw-bypass-explained/">Docker bypasses UFW — explained</a></li>
</ul>
"""

# ── POST 2: Docker Compose Security Checklist ─────────────────────────────────

POST2_BODY = """
<p>Most Docker Compose files are written to get the service running. Security comes later — usually when something goes wrong. This checklist covers everything to check before a Docker Compose setup goes anywhere near a public-facing server.</p>

<p>It is not exhaustive. It is the 20% of checks that catch 80% of the real issues.</p>

<h2>1. Port bindings — the most common mistake</h2>

<p>Every port in your Compose file that uses <code>HOST:CONTAINER</code> format binds to <code>0.0.0.0</code> — all interfaces, including your public IP. UFW does not protect these ports. Docker bypasses UFW entirely.</p>

<pre># Bad — publicly accessible:
ports:
  - "6379:6379"
  - "5432:5432"
  - "27017:27017"

# Good — localhost only, access via reverse proxy:
ports:
  - "127.0.0.1:6379:6379"
  - "127.0.0.1:5432:5432"</pre>

<p>Databases, caches, and internal APIs should never be bound to <code>0.0.0.0</code>. Only your reverse proxy (Nginx, Traefik, Caddy) needs public port access — and only on 80 and 443.</p>

<h2>2. Hardcoded credentials</h2>

<pre># Bad — credentials in compose file:
environment:
  POSTGRES_PASSWORD: mysecretpassword
  API_KEY: sk-abc123

# Good — reference from .env:
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  API_KEY: ${API_KEY}</pre>

<p>The <code>.env</code> file must be in <code>.gitignore</code> and must never be committed. Check your git history if you're not sure:</p>

<pre>git log --all -p | grep -i "password|secret|api_key" | head -20</pre>

<h2>3. Missing healthchecks</h2>

<p>Without a healthcheck, Docker marks a container as healthy the moment it starts — even if the application inside is still booting, running migrations, or has crashed. Dependent services start immediately against an unready backend.</p>

<pre>healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s</pre>

<p>The <code>start_period</code> is the grace period before failures count — essential for Java apps, services running DB migrations, or anything with a slow startup.</p>

<h2>4. Missing resource limits</h2>

<p>A memory leak or runaway process in one container can OOM-kill everything else on the host. Set limits.</p>

<pre>deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      memory: 256M</pre>

<div class="callout">
  <p>Compose v3 resource limits require <code>docker compose</code> (not <code>docker-compose</code> v1) or Swarm mode. For standalone Compose v2 format use <code>mem_limit: 512m</code> and <code>cpus: '1.0'</code> at the service level.</p>
</div>

<h2>5. Log rotation</h2>

<p>Docker's default logging driver writes to JSON files with no size limit. A verbose service running 24/7 fills your disk. When the disk fills, containers start failing in confusing ways.</p>

<pre>logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"</pre>

<p>Or set it globally in <code>/etc/docker/daemon.json</code> so every container gets rotation by default:</p>

<pre>{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}</pre>

<h2>6. network_mode: host — never use this in production</h2>

<p><code>network_mode: host</code> removes Docker's network isolation entirely. The container shares the host's network stack directly. Every port the container opens is immediately accessible on the host's public IP with no Docker NAT or port mapping involved — bypassing every network security layer.</p>

<pre># Red flag — remove this:
network_mode: host</pre>

<p>It exists for performance-sensitive cases (high-frequency trading, certain monitoring tools). For a web service, API, or database — there is no valid reason to use it.</p>

<h2>7. Privileged mode</h2>

<pre># Red flag:
privileged: true

# Also red flag:
cap_add:
  - SYS_ADMIN
  - NET_ADMIN</pre>

<p>Privileged containers have root access to the host kernel. A vulnerability in a privileged container is a host compromise. The only legitimate uses are very specific system-level tools. If a tutorial tells you to add <code>privileged: true</code> for a web app, find a better tutorial.</p>

<h2>8. Volume mounts — be specific</h2>

<pre># Dangerous — mounts entire host filesystem:
volumes:
  - /:/host

# Also risky — mounts Docker socket (root equivalent):
volumes:
  - /var/run/docker.sock:/var/run/docker.sock

# Better — mount only what the container needs:
volumes:
  - ./data:/app/data
  - ./config:/app/config:ro</pre>

<p>Mounting <code>/var/run/docker.sock</code> gives the container full control over the Docker daemon — it can start, stop, and modify any container on the host. Only monitoring tools (Portainer, Watchtower) legitimately need this.</p>

<h2>The full checklist</h2>

<ul class="checklist">
  <li>All database/cache ports bound to 127.0.0.1, not 0.0.0.0</li>
  <li>No hardcoded credentials in environment: blocks — all use ${VAR} references</li>
  <li>.env file is in .gitignore and not committed</li>
  <li>Every service has a healthcheck defined</li>
  <li>Resource limits set on all services (memory + CPU)</li>
  <li>Log rotation configured (max-size + max-file)</li>
  <li>No network_mode: host unless specifically required</li>
  <li>No privileged: true unless specifically required</li>
  <li>Volume mounts are specific — no / or /etc mounts</li>
  <li>Docker socket not mounted unless required by monitoring tool</li>
</ul>

<div class="cta">
  <p>Paste your docker-compose.yml to catch exposed ports, hardcoded secrets, missing healthchecks, and resource limits automatically.</p>
  <div class="cta-row">
    <a href="/docker/">Docker Auditor →</a>
    <a href="/firewall/" class="sec">Firewall Auditor →</a>
  </div>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/blog/docker-ufw-bypass-explained/">Docker bypasses UFW — why port binding matters</a></li>
  <li><a href="/fix/docker/hardcoded-secrets/">Hardcoded secrets fix guide</a></li>
  <li><a href="/fix/docker/missing-healthcheck/">Missing healthcheck fix guide</a></li>
  <li><a href="/glossary/hardcoded-secrets/">What are hardcoded secrets?</a></li>
  <li><a href="/incidents/docker-secrets-exposed/">Incident: hardcoded secrets in docker-compose files</a></li>
</ul>
"""

# ── POST 3: Traefik v3 what broke ─────────────────────────────────────────────

POST3_BODY = """
<p>Traefik v3 has been out for months. The migration from v2 should have been straightforward — most of the core label syntax is identical. Instead, r/selfhosted and r/docker are full of threads from people whose routes silently stopped working after the upgrade.</p>

<p>Here's what's actually breaking and why.</p>

<h2>The silent failure problem</h2>

<p>Traefik v3 does not error on invalid or deprecated configuration. It starts successfully. It logs nothing obvious. Your containers are running. The routes just don't exist.</p>

<p>This is why the migration catches people off guard. There's no clear failure signal — just 404s from routes that used to work.</p>

<h2>What broke for most people</h2>

<h3>1. Docker network not explicitly configured</h3>

<p>This is the most common failure. In v2, Traefik could usually figure out which Docker network to use for routing. In v3, if Traefik and your containers are on different networks, the route is created but has no healthy backends — returns 404.</p>

<pre># The fix — create a shared external network:
docker network create traefik-public

# Traefik service:
services:
  traefik:
    networks:
      - traefik-public

# Every routed service:
services:
  myapp:
    networks:
      - traefik-public
    labels:
      - "traefik.docker.network=traefik-public"

networks:
  traefik-public:
    external: true</pre>

<p>The <code>traefik.docker.network</code> label is now required when multiple networks are involved. In v2 it was optional.</p>

<h3>2. Old v1 labels still in compose files</h3>

<p>Traefik v1 labels (<code>traefik.frontend.*</code>, <code>traefik.backend</code>, <code>traefik.port</code>) were deprecated in v2 but silently accepted. In v3 they are completely ignored — no warning, no error, no route.</p>

<pre># These do nothing in v3 — remove them:
traefik.frontend.rule=Host:app.example.com
traefik.backend=myapp
traefik.port=3000
traefik.frontend.entryPoints=https

# Replace with:
traefik.enable=true
traefik.http.routers.myapp.rule=Host("app.example.com")
traefik.http.routers.myapp.entrypoints=websecure
traefik.http.routers.myapp.tls.certresolver=letsencrypt
traefik.http.services.myapp.loadbalancer.server.port=3000</pre>

<h3>3. swarmMode in static config</h3>

<p>If your <code>traefik.yml</code> has <code>swarmMode: false</code> inside the Docker provider block, Traefik v3 throws a startup error because Swarm configuration moved to a separate provider.</p>

<pre># v2 static config (breaks in v3):
providers:
  docker:
    swarmMode: false  # Remove this line

# v3 — Swarm is now a separate provider:
providers:
  docker:
    exposedByDefault: false
  # swarm: (only add if actually using Swarm)</pre>

<h3>4. allowEmptyServices removed</h3>

<p>If you had <code>allowEmptyServices: true</code> in your Docker provider config to allow Traefik to start when backends are down — it's gone. Remove it from your config. Traefik v3 handles empty services differently and the option is no longer needed.</p>

<h2>How to diagnose what broke</h2>

<pre># Check Traefik's view of your routers:
curl http://localhost:8080/api/http/routers | python3 -m json.tool | grep -A5 "status"

# Look for routers with no services or "error" status
# Check which containers Traefik can see:
curl http://localhost:8080/api/http/services | python3 -m json.tool</pre>

<p>Enable the Traefik dashboard if you haven't already — it shows you exactly which routes exist and whether their backends are healthy. A router with 0 healthy servers is your problem.</p>

<h2>The labels that still work identically</h2>

<p>To be clear — the core v2 label syntax is unchanged in v3. These still work:</p>

<pre>traefik.enable=true
traefik.http.routers.NAME.rule=Host("domain.com")
traefik.http.routers.NAME.tls.certresolver=letsencrypt
traefik.http.services.NAME.loadbalancer.server.port=3000
traefik.http.middlewares.NAME.redirectscheme.scheme=https</pre>

<p>If your setup only uses basic routing with TLS, you may not need to change anything except add the explicit network configuration.</p>

<h2>Quick migration checklist</h2>

<ul class="checklist">
  <li>Create explicit external Docker network and attach Traefik + all services to it</li>
  <li>Add traefik.docker.network label to every routed service</li>
  <li>Remove any traefik.frontend.*, traefik.backend, traefik.port labels</li>
  <li>Remove swarmMode: false from Docker provider static config</li>
  <li>Remove allowEmptyServices from static config</li>
  <li>Check dashboard or API for routers with 0 healthy backends</li>
</ul>

<div class="cta">
  <p>Paste your docker-compose.yml or nginx.conf to detect Traefik v1 label patterns and get exact v3 replacements.</p>
  <div class="cta-row">
    <a href="/proxy/">Reverse Proxy Mapper →</a>
  </div>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/proxy/traefik-v2-to-v3/">Traefik v2 to v3 migration fix guide</a></li>
  <li><a href="/glossary/traefik-labels/">Traefik labels glossary</a></li>
  <li><a href="/fix/proxy/dangling-routes/">Dangling routes fix guide</a></li>
  <li><a href="/blog/traefik-v2-to-v3-migration/">Traefik migration — what actually broke</a></li>
</ul>
"""

POSTS = [
    {
        "slug": "fail2ban-misconfigured",
        "title": "Fail2ban is Misconfigured on Most Servers. Here's How to Check.",
        "meta_desc": "The default fail2ban configuration is wrong for Ubuntu 22.04 with systemd. Wrong backend, short ban times, inactive jails. How to audit and fix your setup in 5 minutes.",
        "keywords": "fail2ban misconfigured, fail2ban systemd backend, fail2ban ssh not working, fail2ban ubuntu 22 fix",
        "date": "2026-03-27",
        "tags": ["Linux", "Security", "fail2ban", "SSH"],
        "lede": "Fail2ban is running. The service shows active. The sshd jail exists. And brute force attempts are sailing straight through because the backend is wrong and the ban times are 10 minutes. Here is how to check yours right now.",
        "body": POST1_BODY,
    },
    {
        "slug": "docker-compose-security-checklist",
        "title": "The Docker Compose Security Checklist Before You Go Live",
        "meta_desc": "10 Docker Compose security checks before deploying to a public server — exposed ports, hardcoded secrets, missing healthchecks, resource limits, privileged mode, and volume mounts.",
        "keywords": "docker compose security checklist, docker security before deploy, docker compose best practices security, docker compose hardening",
        "date": "2026-03-27",
        "tags": ["Docker", "Security", "DevOps", "Checklist"],
        "lede": "Most Docker Compose files are written to get the service running. Security comes later — usually when something goes wrong. This is the 20% of checks that catch 80% of the real issues.",
        "body": POST2_BODY,
    },
    {
        "slug": "traefik-v3-what-broke-in-the-wild",
        "title": "Traefik v3 Is Out. Here's What Broke in the Wild.",
        "meta_desc": "Traefik v3 silently breaks routes with no error output. Docker network configuration, old v1 labels, swarmMode removal — the actual issues causing 404s after upgrading.",
        "keywords": "traefik v3 breaking changes, traefik v3 routes not working, traefik upgrade 404, traefik v3 docker network",
        "date": "2026-03-27",
        "tags": ["Traefik", "Docker", "Reverse Proxy", "Migration"],
        "lede": "Traefik v3 starts successfully. Logs nothing obvious. Your containers are running. The routes just return 404. No error. No warning. This is what is actually breaking and why.",
        "body": POST3_BODY,
    },
]

if __name__ == "__main__":
    print("=== Building 3 New Blog Posts ===\n")

    for post in POSTS:
        slug = post["slug"]
        os.makedirs(f"blog/{slug}", exist_ok=True)
        html = build_page(
            slug, post["title"], post["meta_desc"], post["keywords"],
            post["date"], post["tags"], post["lede"], post["body"]
        )
        with open(f"blog/{slug}/index.html", "w") as f:
            f.write(html)
        print(f"  ✅ blog/{slug}/index.html ({len(html):,} bytes)")

    # Update blog index
    with open("blog/index.html", "r") as f:
        content = f.read()

    new_cards = ""
    for post in POSTS:
        if post["slug"] not in content:
            tag_html = "&nbsp;".join([
                f'<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">{t}</span>'
                for t in post["tags"]
            ])
            new_cards += f"""    <a href="/blog/{post['slug']}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">{post['date']} &nbsp;·&nbsp; {tag_html}</div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">{post['title']}</div>
      <div style="font-size:0.82rem;color:var(--muted);">{post['meta_desc'][:120]}...</div>
    </a>\n"""

    if new_cards:
        marker = '<h1 style="font-size:1.6rem'
        content = content.replace(marker, new_cards + "    " + marker, 1)
        with open("blog/index.html", "w") as f:
            f.write(content)
        print(f"\n  ✅ blog/index.html — 3 posts added")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)

    added = 0
    for post in POSTS:
        slug = post["slug"]
        for rule in [
            {"source": f"/blog/{slug}/", "destination": f"/blog/{slug}/index.html"},
            {"source": f"/blog/{slug}", "destination": f"/blog/{slug}/index.html"},
        ]:
            if rule not in config["rewrites"]:
                config["rewrites"].append(rule)
                added += 1

    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  ✅ vercel.json — {added} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()

    entries = []
    for post in POSTS:
        url = f"/blog/{post['slug']}/"
        if url not in sitemap:
            entries.append(f"  <url><loc>https://www.configclarity.dev{url}</loc><lastmod>{post['date']}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>")

    if entries:
        sitemap = sitemap.replace("</urlset>", "\n".join(entries) + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
        print(f"  ✅ sitemap-seo.xml — {len(entries)} URLs added")

    # Validate JSON-LD
    import re, json as jsonlib
    errors = []
    for post in POSTS:
        filepath = f"blog/{post['slug']}/index.html"
        with open(filepath) as f:
            html = f.read()
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        for i, b in enumerate(blocks):
            try:
                jsonlib.loads(b)
            except Exception as e:
                errors.append(f"{filepath} block {i}: {e}")

    if errors:
        print(f"\n  ⚠️  JSON-LD errors:")
        for e in errors: print(f"    {e}")
    else:
        print(f"  ✅ JSON-LD valid on all 3 posts")

    print(f"\nDone. Blog is now 9 posts.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: 3 new blog posts — fail2ban, docker checklist, traefik v3' && git push origin main && npx vercel --prod --force")
    print("\nReddit targets:")
    print("  fail2ban post    → r/selfhosted, r/sysadmin (NPF Friday)")
    print("  docker checklist → r/docker, r/selfhosted")
    print("  traefik v3       → r/selfhosted, r/docker")
