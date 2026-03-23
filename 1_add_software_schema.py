#!/usr/bin/env python3
"""
Script 1: Add SoftwareApplication schema to all 6 tool pages.
Run from: ~/Projects/configclarity-fresh/
"""

import re

TOOLS = [
    {
        "file": "index.html",
        "name": "Cron Job Visualiser",
        "url": "https://configclarity.dev/",
        "description": "Free browser-based cron job visualiser and auditor. Paste your crontab, detect overlapping jobs, flock conflicts, and server load spikes. Generates exact fix commands for your stack.",
        "keywords": "cron job visualiser, crontab auditor, overlapping cron jobs, flock safety, server load spike"
    },
    {
        "file": "ssl/index.html",
        "name": "SSL Certificate Checker",
        "url": "https://configclarity.dev/ssl/",
        "description": "Free browser-based SSL certificate checker. Scan multiple domains for expiry, CDN risks, missing intermediates, and self-signed certs. Generates renewal config for Nginx, Traefik, and Cloudflare.",
        "keywords": "SSL certificate checker, cert expiry monitor, HTTPS certificate audit, Let's Encrypt renewal, CDN SSL"
    },
    {
        "file": "docker/index.html",
        "name": "Docker Compose Auditor",
        "url": "https://configclarity.dev/docker/",
        "description": "Free browser-based Docker Compose auditor. Paste your docker-compose.yml and .env to detect hardcoded secrets, missing healthchecks, port collisions, and 0.0.0.0 bindings. Generates exact fixes.",
        "keywords": "docker compose audit, docker security checker, hardcoded secrets docker, docker healthcheck, port collision"
    },
    {
        "file": "firewall/index.html",
        "name": "Firewall Auditor",
        "url": "https://configclarity.dev/firewall/",
        "description": "Free browser-based UFW firewall auditor. Paste ufw status verbose output to detect high-risk open ports, missing default-deny rules, and IPv4/IPv6 mismatches. Generates exact ufw fix commands.",
        "keywords": "UFW firewall audit, open port checker, default deny firewall, IPv6 mismatch ufw, firewall security"
    },
    {
        "file": "proxy/index.html",
        "name": "Reverse Proxy Mapper",
        "url": "https://configclarity.dev/proxy/",
        "description": "Free browser-based reverse proxy auditor. Paste your nginx.conf or Docker Compose labels to detect dangling routes, missing SSL redirects, and Traefik v2 to v3 migration issues.",
        "keywords": "reverse proxy audit, nginx config checker, Traefik v2 v3 migration, SSL redirect missing, dangling route"
    },
    {
        "file": "robots/index.html",
        "name": "robots.txt Validator",
        "url": "https://configclarity.dev/robots/",
        "description": "Free browser-based robots.txt validator. Fetch live or paste content to detect syntax errors, accidental crawl blocks, missing AI bot directives, and sitemap references. Generates corrected robots.txt.",
        "keywords": "robots.txt validator, robots txt checker, GPTBot block, ClaudeBot robots, crawl budget, sitemap robots"
    },
]

def make_schema(tool):
    return f'''
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{tool['name']}",
    "url": "{tool['url']}",
    "applicationCategory": "DeveloperApplication",
    "applicationSubCategory": "Security",
    "operatingSystem": "Any",
    "browserRequirements": "Requires JavaScript",
    "offers": {{
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    }},
    "description": "{tool['description']}",
    "keywords": "{tool['keywords']}",
    "author": {{
      "@type": "Organization",
      "name": "MetricLogic",
      "url": "https://metriclogic.dev"
    }},
    "isPartOf": {{
      "@type": "WebSite",
      "name": "ConfigClarity",
      "url": "https://configclarity.dev"
    }},
    "license": "https://opensource.org/licenses/MIT",
    "softwareVersion": "1.0",
    "releaseNotes": "Free, client-side only. No signup, no backend, no tracking."
  }}
  </script>'''

def inject_schema(filepath, schema):
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already has SoftwareApplication
    if '"SoftwareApplication"' in content:
        print(f"  SKIP {filepath} — SoftwareApplication already present")
        return False

    # Find </head> and insert before it
    if '</head>' in content:
        content = content.replace('</head>', schema + '\n</head>', 1)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✅ {filepath} — SoftwareApplication schema injected")
        return True
    else:
        print(f"  ❌ {filepath} — no </head> found")
        return False

if __name__ == '__main__':
    import os
    print("=== Adding SoftwareApplication Schema ===\n")
    ok = 0
    for tool in TOOLS:
        if os.path.exists(tool['file']):
            schema = make_schema(tool)
            if inject_schema(tool['file'], schema):
                ok += 1
        else:
            print(f"  ❌ {tool['file']} — FILE NOT FOUND (run from repo root)")
    print(f"\nDone: {ok}/{len(TOOLS)} files updated")
    print("\nVerify: grep -c 'SoftwareApplication' index.html ssl/index.html docker/index.html firewall/index.html proxy/index.html robots/index.html")
