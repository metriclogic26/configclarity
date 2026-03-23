#!/usr/bin/env python3
"""
Script 2: Build 4 index parent pages.
Run from: ~/Projects/configclarity-fresh/
"""

import os

CSS = """
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root {
        --bg: #0b0d14; --bg2: #1e2130; --purple: #6c63ff;
        --green: #22c55e; --orange: #f97316; --red: #ef4444;
        --text: #e2e4f0; --muted: #8a8fb5;
      }
      body { background: var(--bg); color: var(--text); font-family: 'JetBrains Mono', monospace; min-height: 100vh; }
      a { color: var(--purple); text-decoration: none; }
      a:hover { text-decoration: underline; }
      .header { padding: 1.5rem 2rem; border-bottom: 1px solid #2a2d3d; display: flex; align-items: center; gap: 1rem; }
      .header-logo { font-size: 1.1rem; font-weight: 700; color: var(--text); }
      .header-logo span { color: var(--purple); }
      .header-nav { margin-left: auto; display: flex; gap: 1rem; font-size: 0.8rem; color: var(--muted); }
      .header-nav a { color: var(--muted); }
      .hero { padding: 3rem 2rem 2rem; max-width: 900px; margin: 0 auto; }
      .hero h1 { font-size: 1.8rem; font-weight: 700; margin-bottom: 0.75rem; }
      .hero p { color: var(--muted); font-size: 0.9rem; line-height: 1.7; max-width: 600px; }
      .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; padding: 0 2rem 3rem; max-width: 900px; margin: 0 auto; }
      .card { background: var(--bg2); border: 1px solid #2a2d3d; border-radius: 8px; padding: 1.25rem 1.5rem; transition: border-color .2s; }
      .card:hover { border-color: var(--purple); }
      .card-title { font-size: 0.95rem; font-weight: 600; margin-bottom: 0.4rem; }
      .card-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.6; }
      .badge { display: inline-block; font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 4px; margin-bottom: 0.5rem; }
      .badge-green { background: rgba(34,197,94,.15); color: var(--green); }
      .badge-red { background: rgba(239,68,68,.15); color: var(--red); }
      .badge-orange { background: rgba(249,115,22,.15); color: var(--orange); }
      .breadcrumb { padding: 1rem 2rem 0; max-width: 900px; margin: 0 auto; font-size: 0.78rem; color: var(--muted); }
      .breadcrumb a { color: var(--muted); }
      .section-label { padding: 0 2rem; max-width: 900px; margin: 1.5rem auto 0.75rem; font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }
      footer { text-align: center; padding: 2rem; font-size: 0.75rem; color: var(--muted); border-top: 1px solid #2a2d3d; }
    </style>
"""

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

FOOTER = """
  <footer>
    <p>Part of the <a href="https://metriclogic.dev">MetricLogic</a> network &nbsp;·&nbsp;
    <a href="https://configclarity.dev">ConfigClarity</a> &nbsp;·&nbsp;
    <a href="https://domainpreflight.dev">DomainPreflight</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub</a></p>
  </footer>
"""

HEADER = """
  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a>
      <a href="/ssl/">SSL</a>
      <a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a>
      <a href="/proxy/">Proxy</a>
      <a href="/robots/">robots.txt</a>
    </nav>
  </header>
"""

# ─── /error/index.html ────────────────────────────────────────────────────────

ERROR_PAGES = [
    ("docker-ufw-bypass", "Docker UFW Bypass", "Docker traffic bypassing UFW firewall rules via iptables. Containers expose ports to the internet despite UFW deny rules.", "red"),
    ("nginx-502-bad-gateway", "Nginx 502 Bad Gateway", "Nginx cannot reach the upstream application server. Common causes: app crashed, wrong port, socket path mismatch.", "red"),
    ("cron-not-running", "Cron Job Not Running", "Scheduled cron jobs silently failing. Causes include missing PATH, wrong user permissions, environment variable issues.", "orange"),
    ("ufw-inactive-still-open", "UFW Inactive — Ports Still Open", "UFW is disabled but ports remain accessible. iptables rules from Docker or manual rules persist after UFW is stopped.", "orange"),
    ("permission-denied-docker-socket", "Permission Denied: Docker Socket", "User cannot run Docker commands. /var/run/docker.sock permission denied — user not in docker group.", "orange"),
]

def build_error_index():
    schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Linux & Docker Error Fix Guides",
    "url": "https://configclarity.dev/error/",
    "description": "Fix guides for common Linux server, Docker, UFW, Nginx, and cron errors. Exact copy-paste commands for your stack.",
    "isPartOf": {"@type": "WebSite", "name": "ConfigClarity", "url": "https://configclarity.dev"},
    "mainEntity": {
      "@type": "ItemList",
      "name": "Error Fix Guides",
      "itemListElement": [
        {"@type":"ListItem","position":1,"url":"https://configclarity.dev/error/docker-ufw-bypass","name":"Docker UFW Bypass Fix"},
        {"@type":"ListItem","position":2,"url":"https://configclarity.dev/error/nginx-502-bad-gateway","name":"Nginx 502 Bad Gateway Fix"},
        {"@type":"ListItem","position":3,"url":"https://configclarity.dev/error/cron-not-running","name":"Cron Job Not Running Fix"},
        {"@type":"ListItem","position":4,"url":"https://configclarity.dev/error/ufw-inactive-still-open","name":"UFW Inactive Still Open Fix"},
        {"@type":"ListItem","position":5,"url":"https://configclarity.dev/error/permission-denied-docker-socket","name":"Docker Socket Permission Denied Fix"}
      ]
    }
  }
  </script>"""

    breadcrumb_schema = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"},
    {"@type":"ListItem","position":2,"name":"Error Fix Guides","item":"https://configclarity.dev/error/"}
  ]}
  </script>"""

    cards = "\n".join([
        f'''    <a href="/error/{slug}/" class="card" style="display:block;">
      <span class="badge badge-{badge}">{badge.upper()}</span>
      <div class="card-title">{title}</div>
      <div class="card-desc">{desc}</div>
    </a>'''
        for slug, title, desc, badge in ERROR_PAGES
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Linux & Docker Error Fix Guides — ConfigClarity</title>
  <meta name="description" content="Fix guides for common Linux server, Docker, UFW, Nginx, and cron errors. Exact copy-paste commands for Ubuntu, Debian, Nginx, and Docker stacks.">
  <meta name="keywords" content="docker ufw bypass fix, nginx 502 fix, cron not running, ufw inactive, docker socket permission denied">
  <link rel="canonical" href="https://configclarity.dev/error/">
  <meta property="og:title" content="Linux & Docker Error Fix Guides — ConfigClarity">
  <meta property="og:description" content="Exact fix commands for Docker, UFW, Nginx, and cron errors.">
  <meta property="og:url" content="https://configclarity.dev/error/">
  <meta property="og:type" content="website">
  {FONT}
{schema}
{breadcrumb_schema}
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › Error Fix Guides</div>
  <section class="hero">
    <h1>Error Fix Guides</h1>
    <p>Common Linux server, Docker, UFW, Nginx, and cron errors — with exact copy-paste fix commands for your stack. No generic advice.</p>
  </section>
  <div class="grid">
{cards}
  </div>
{FOOTER}
</body>
</html>"""

# ─── /vs/index.html ────────────────────────────────────────────────────────────

VS_PAGES = [
    ("configclarity-vs-securityheaders", "ConfigClarity vs securityheaders.com", "ConfigClarity generates the exact Nginx/Cloudflare config to fix your headers. securityheaders.com only gives you a grade."),
    ("configclarity-vs-ssl-labs", "ConfigClarity vs SSL Labs", "ConfigClarity checks multiple domains at once with 200-day early warnings. SSL Labs tests one domain with no actionable fix output."),
    ("configclarity-vs-mxtoolbox", "ConfigClarity vs MXToolbox", "ConfigClarity is a fixer, not a checker. MXToolbox tells you what's wrong; ConfigClarity tells you the exact config to paste."),
]

def build_vs_index():
    schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "ConfigClarity Comparison Guides",
    "url": "https://configclarity.dev/vs/",
    "description": "How ConfigClarity compares to securityheaders.com, SSL Labs, MXToolbox, and other developer tools.",
    "isPartOf": {"@type":"WebSite","name":"ConfigClarity","url":"https://configclarity.dev"},
    "mainEntity": {
      "@type": "ItemList",
      "name": "Tool Comparisons",
      "itemListElement": [
        {"@type":"ListItem","position":1,"url":"https://configclarity.dev/vs/configclarity-vs-securityheaders","name":"ConfigClarity vs securityheaders.com"},
        {"@type":"ListItem","position":2,"url":"https://configclarity.dev/vs/configclarity-vs-ssl-labs","name":"ConfigClarity vs SSL Labs"},
        {"@type":"ListItem","position":3,"url":"https://configclarity.dev/vs/configclarity-vs-mxtoolbox","name":"ConfigClarity vs MXToolbox"}
      ]
    }
  }
  </script>"""

    cards = "\n".join([
        f'''    <a href="/vs/{slug}/" class="card" style="display:block;">
      <div class="card-title">{title}</div>
      <div class="card-desc">{desc}</div>
    </a>'''
        for slug, title, desc in VS_PAGES
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ConfigClarity vs Alternatives — Tool Comparison Guides</title>
  <meta name="description" content="How ConfigClarity compares to securityheaders.com, SSL Labs, MXToolbox, and other server audit tools. Fixers not checkers.">
  <meta name="keywords" content="configclarity alternative, securityheaders.com alternative, ssl labs alternative, mxtoolbox alternative">
  <link rel="canonical" href="https://configclarity.dev/vs/">
  <meta property="og:title" content="ConfigClarity vs Alternatives — Tool Comparison Guides">
  <meta property="og:description" content="How ConfigClarity compares to securityheaders.com, SSL Labs, MXToolbox. Fixers not checkers.">
  <meta property="og:url" content="https://configclarity.dev/vs/">
  {FONT}
{schema}
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › Tool Comparisons</div>
  <section class="hero">
    <h1>ConfigClarity vs Alternatives</h1>
    <p>ConfigClarity is a fixer, not a checker. Here's how it compares to the tools developers already know — and why "shipping the fix" changes everything.</p>
  </section>
  <div class="grid">
{cards}
  </div>
{FOOTER}
</body>
</html>"""

# ─── /fix/index.html ────────────────────────────────────────────────────────────

FIX_CATEGORIES = [
    ("docker", "Docker Fix Guides", "Hardcoded secrets, missing healthchecks, port collisions, UFW bypass, 0.0.0.0 bindings.", "green"),
    ("ufw", "UFW Firewall Fix Guides", "Docker bypass, default-deny missing, IPv6 mismatch, port exposed after Docker.", "green"),
    ("nftables", "nftables Fix Guides", "Ubuntu 22 nftables setup, Docker conflict resolution.", "green"),
    ("cron", "Cron Job Fix Guides", "Overlapping jobs, silent failure, flock safety, server load spikes, AI agent collision.", "green"),
    ("ssl", "SSL Certificate Fix Guides", "Expiry monitoring, CDN domain risks, Traefik renewal, Nginx renewal, 200-day warnings.", "green"),
    ("nginx", "Nginx Fix Guides", "502 Bad Gateway, upstream timeout, missing SSL redirect.", "green"),
    ("robots", "robots.txt Fix Guides", "Accidental crawl blocks, missing AI bot directives, sitemap reference, crawl-delay.", "orange"),
    ("proxy", "Reverse Proxy Fix Guides", "Traefik v2→v3 migration, dangling routes, CORS double headers, missing rate limits.", "orange"),
]

def build_fix_index():
    schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Linux Server Fix Guides — ConfigClarity",
    "url": "https://configclarity.dev/fix/",
    "description": "Exact copy-paste fix guides for Docker, UFW, Nginx, SSL, cron, and robots.txt issues on Linux servers.",
    "isPartOf": {"@type":"WebSite","name":"ConfigClarity","url":"https://configclarity.dev"},
    "mainEntity": {
      "@type": "ItemList",
      "name": "Fix Guide Categories",
      "itemListElement": [
        {"@type":"ListItem","position":1,"url":"https://configclarity.dev/fix/docker/","name":"Docker Fix Guides"},
        {"@type":"ListItem","position":2,"url":"https://configclarity.dev/fix/ufw/","name":"UFW Firewall Fix Guides"},
        {"@type":"ListItem","position":3,"url":"https://configclarity.dev/fix/cron/","name":"Cron Job Fix Guides"},
        {"@type":"ListItem","position":4,"url":"https://configclarity.dev/fix/ssl/","name":"SSL Certificate Fix Guides"},
        {"@type":"ListItem","position":5,"url":"https://configclarity.dev/fix/nginx/","name":"Nginx Fix Guides"},
        {"@type":"ListItem","position":6,"url":"https://configclarity.dev/fix/robots/","name":"robots.txt Fix Guides"},
        {"@type":"ListItem","position":7,"url":"https://configclarity.dev/fix/proxy/","name":"Reverse Proxy Fix Guides"},
        {"@type":"ListItem","position":8,"url":"https://configclarity.dev/fix/nftables/","name":"nftables Fix Guides"}
      ]
    }
  }
  </script>"""

    cards = "\n".join([
        f'''    <a href="/fix/{slug}/" class="card" style="display:block;">
      <span class="badge badge-{badge}">{slug.upper()}</span>
      <div class="card-title">{title}</div>
      <div class="card-desc">{desc}</div>
    </a>'''
        for slug, title, desc, badge in FIX_CATEGORIES
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Linux Server Fix Guides — ConfigClarity</title>
  <meta name="description" content="Exact copy-paste fix guides for Docker, UFW, Nginx, SSL certificate, cron job, and robots.txt issues on Linux servers. Stack-specific commands for Ubuntu, Debian, and Nginx.">
  <meta name="keywords" content="docker fix guide, ufw firewall fix, nginx fix, ssl certificate fix, cron job fix, linux server fix">
  <link rel="canonical" href="https://configclarity.dev/fix/">
  <meta property="og:title" content="Linux Server Fix Guides — ConfigClarity">
  <meta property="og:description" content="Exact copy-paste fix guides for Docker, UFW, Nginx, SSL, and cron on Linux servers.">
  <meta property="og:url" content="https://configclarity.dev/fix/">
  {FONT}
{schema}
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › Fix Guides</div>
  <section class="hero">
    <h1>Linux Server Fix Guides</h1>
    <p>Exact copy-paste fix commands for Docker, UFW, Nginx, SSL, cron, and robots.txt issues. Stack-specific — the fix for Ubuntu looks different from the fix for Debian.</p>
  </section>
  <div class="grid">
{cards}
  </div>
{FOOTER}
</body>
</html>"""

# ─── /providers/index.html ─────────────────────────────────────────────────────

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

def build_providers_index():
    schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "VPS & Cloud Provider Fix Guides — ConfigClarity",
    "url": "https://configclarity.dev/providers/",
    "description": "Stack-specific Docker, SSL, UFW, and SSH hardening fix guides for Hetzner, DigitalOcean, Vultr, Linode, and 11 more cloud providers.",
    "isPartOf": {"@type":"WebSite","name":"ConfigClarity","url":"https://configclarity.dev"}
  }
  </script>"""

    cards = "\n".join([
        f'''    <a href="/providers/{slug}/" class="card" style="display:block;">
      <div class="card-title">{name}</div>
      <div class="card-desc">Docker firewall setup, SSL, UFW/Docker rules, SSH hardening — specific to {name} infrastructure.</div>
    </a>'''
        for slug, name in PROVIDERS
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VPS & Cloud Provider Fix Guides — ConfigClarity</title>
  <meta name="description" content="Stack-specific Docker, SSL, UFW firewall, and SSH hardening guides for Hetzner, DigitalOcean, Vultr, Linode, AWS Lightsail, Oracle Cloud, and more.">
  <meta name="keywords" content="hetzner docker setup, digitalocean ufw docker, vultr ssl setup, linode firewall, cloud vps hardening">
  <link rel="canonical" href="https://configclarity.dev/providers/">
  <meta property="og:title" content="VPS & Cloud Provider Fix Guides — ConfigClarity">
  <meta property="og:description" content="Provider-specific Docker, SSL, UFW, and SSH hardening guides for 15 cloud providers.">
  <meta property="og:url" content="https://configclarity.dev/providers/">
  {FONT}
{schema}
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › Provider Guides</div>
  <section class="hero">
    <h1>VPS &amp; Cloud Provider Guides</h1>
    <p>Docker firewall setup, SSL configuration, UFW rules, and SSH hardening — specific to your hosting provider. Because the fix for Hetzner looks different from the fix for DigitalOcean.</p>
  </section>
  <div class="grid">
{cards}
  </div>
{FOOTER}
</body>
</html>"""

if __name__ == '__main__':
    pages = [
        ("error/index.html", build_error_index()),
        ("vs/index.html", build_vs_index()),
        ("fix/index.html", build_fix_index()),
        ("providers/index.html", build_providers_index()),
    ]

    print("=== Building Index Parent Pages ===\n")
    for path, html in pages:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(html)
        print(f"  ✅ {path} ({len(html):,} bytes)")

    print(f"\nDone. 4 index pages built.")
    print("\nNext: add to vercel.json rewrites and sitemap-seo.xml")
