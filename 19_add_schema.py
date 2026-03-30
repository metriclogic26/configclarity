#!/usr/bin/env python3
"""
Script 19: Add HowTo schema to 5 missing tool pages + ItemList to cron/providers indexes.
Run from: ~/Projects/CronSight/
"""
import re, json

HOWTO_SCHEMAS = {
    "index.html": {
        "name": "How to visualise cron job overlaps and fix scheduling conflicts",
        "description": "Use ConfigClarity Cron Visualiser to detect overlapping jobs, server load spikes, and add flock safety to your crontab",
        "steps": [
            ("Paste your crontab", "Run crontab -l in your terminal and paste the output into the text area, one job per line."),
            ("Click Visualise", "Click the Visualise button to render a 24-hour timeline showing every job and its execution window."),
            ("Review the Overlap Report", "Check the Overlap Report section for jobs that run simultaneously. Enable flock safety toggle to generate safe versions of conflicting jobs."),
            ("Export or Share", "Use Export PNG to save the timeline or Share Timeline URL to send it to your team."),
        ]
    },
    "ssl/index.html": {
        "name": "How to check SSL certificate expiry across multiple domains",
        "description": "Use ConfigClarity SSL Checker to monitor certificate expiry, detect CDN domain risks, and verify certificate chains",
        "steps": [
            ("Enter your domains", "Paste one domain per line into the input area. No https:// needed — just the bare domain names."),
            ("Click Check domains", "The tool queries Certificate Transparency logs for each domain and retrieves expiry dates and issuer information."),
            ("Review expiry warnings", "Domains expiring within 200 days are flagged with exact days remaining. CDN-fronted domains are shown in orange."),
            ("Export results", "Use Export PNG to save a certificate status report for your records or team."),
        ]
    },
    "firewall/index.html": {
        "name": "How to audit UFW firewall rules for Docker bypass and security gaps",
        "description": "Use ConfigClarity Firewall Auditor to detect Docker UFW bypass, missing default-deny, and IPv6 mismatches in your firewall configuration",
        "steps": [
            ("Run ufw status verbose", "On your server run: sudo ufw status verbose and copy the full output."),
            ("Paste the output", "Paste the ufw status output into the text area. The tool auto-detects UFW format."),
            ("Click Audit", "The tool analyses your rules for Docker bypass risk, missing default-deny, high-risk open ports, and IPv4/IPv6 mismatches."),
            ("Apply the fixes", "Each finding includes the exact ufw command or docker-compose.yml change to resolve the issue."),
        ]
    },
    "proxy/index.html": {
        "name": "How to audit Nginx and Traefik reverse proxy configuration",
        "description": "Use ConfigClarity Reverse Proxy Mapper to detect dangling routes, missing SSL redirects, and Traefik v2 to v3 migration issues",
        "steps": [
            ("Paste your config", "Copy your nginx.conf or docker-compose.yml with Traefik labels and paste it into the input area."),
            ("Click Analyse", "The tool parses all proxy_pass targets, server blocks, and Traefik labels to build a route map."),
            ("Review findings", "Dangling routes, missing SSL redirects, and deprecated Traefik v1 labels are flagged with exact fixes."),
            ("Apply fixes", "Each issue includes the corrected Nginx block or Traefik label to copy-paste into your config."),
        ]
    },
    "robots/index.html": {
        "name": "How to validate robots.txt and check AI bot coverage",
        "description": "Use ConfigClarity robots.txt Validator to detect syntax errors, accidental crawl blocks, and missing AI bot directives",
        "steps": [
            ("Enter URL or paste content", "Switch to URL Mode to fetch your live robots.txt automatically, or use Paste Mode to validate a draft."),
            ("Click Audit", "The tool checks syntax, crawl-delay values, wildcard patterns, sitemap references, and AI bot coverage."),
            ("Review the health score", "A 0-100 health score summarises all issues. Each finding includes a Copy Fix button with the corrected directive."),
            ("Test specific URLs", "Use the URL Tester to check whether any path is BLOCKED or ALLOWED for a specific bot."),
        ]
    },
}

ITEMLIST_SCHEMAS = {
    "cron/index.html": {
        "name": "Common Cron Expressions Reference",
        "url": "https://configclarity.dev/cron/",
        "items": [
            ("Every minute", "https://configclarity.dev/cron/every-minute/"),
            ("Every 5 minutes", "https://configclarity.dev/cron/every-5-minutes/"),
            ("Every 15 minutes", "https://configclarity.dev/cron/every-15-minutes/"),
            ("Every hour", "https://configclarity.dev/cron/every-hour/"),
            ("Every day at midnight", "https://configclarity.dev/cron/every-day-midnight/"),
            ("Every weekday", "https://configclarity.dev/cron/every-weekday/"),
            ("Every Monday", "https://configclarity.dev/cron/every-monday/"),
            ("First day of month", "https://configclarity.dev/cron/first-day-of-month/"),
            ("Every Sunday 2am", "https://configclarity.dev/cron/every-sunday-2am/"),
            ("Every 6 hours", "https://configclarity.dev/cron/every-6-hours/"),
            ("At reboot", "https://configclarity.dev/cron/reboot/"),
            ("Twice a day", "https://configclarity.dev/cron/twice-a-day/"),
        ]
    },
    "providers/index.html": {
        "name": "VPS and Cloud Provider Server Configuration Guides",
        "url": "https://configclarity.dev/providers/",
        "items": [
            ("Hetzner", "https://configclarity.dev/providers/hetzner/"),
            ("DigitalOcean", "https://configclarity.dev/providers/digitalocean/"),
            ("Vultr", "https://configclarity.dev/providers/vultr/"),
            ("Linode / Akamai", "https://configclarity.dev/providers/linode/"),
            ("Contabo", "https://configclarity.dev/providers/contabo/"),
            ("OVH", "https://configclarity.dev/providers/ovh/"),
            ("Scaleway", "https://configclarity.dev/providers/scaleway/"),
            ("AWS Lightsail", "https://configclarity.dev/providers/aws-lightsail/"),
            ("Oracle Cloud Free", "https://configclarity.dev/providers/oracle-cloud/"),
            ("Raspberry Pi", "https://configclarity.dev/providers/raspberry-pi/"),
            ("Azure VM", "https://configclarity.dev/providers/azure-vm/"),
            ("GCP Compute Engine", "https://configclarity.dev/providers/gcp-compute/"),
        ]
    },
}

def make_howto(data):
    steps = ",\n".join([
        f'{{"@type":"HowToStep","name":"{n}","text":"{t}"}}'
        for n, t in data["steps"]
    ])
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "{data['name']}",
    "description": "{data['description']}",
    "estimatedCost": {{"@type":"MonetaryAmount","currency":"USD","value":"0"}},
    "step": [{steps}]
  }}
  </script>'''

def make_itemlist(data):
    items = ",\n".join([
        f'{{"@type":"ListItem","position":{i+1},"name":"{name}","url":"{url}"}}'
        for i, (name, url) in enumerate(data["items"])
    ])
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "{data['name']}",
    "url": "{data['url']}",
    "itemListElement": [{items}]
  }}
  </script>'''

def inject(filepath, schema_block):
    with open(filepath, "r") as f:
        content = f.read()
    schema_type = "HowTo" if "HowTo" in schema_block else "ItemList"
    if f'"@type": "{schema_type}"' in content or f'"@type":"{schema_type}"' in content:
        print(f"  SKIP {filepath} — {schema_type} already present")
        return False
    content = content.replace("</head>", schema_block + "\n</head>", 1)
    with open(filepath, "w") as f:
        f.write(content)
    return True

def validate_jsonld(filepath):
    with open(filepath) as f:
        content = f.read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
        except Exception as e:
            return False, f"block {i}: {e}"
    return True, "ok"

if __name__ == "__main__":
    print("=== Adding HowTo schema to 5 tool pages ===\n")
    howto_count = 0
    for filepath, data in HOWTO_SCHEMAS.items():
        schema = make_howto(data)
        if inject(filepath, schema):
            ok, msg = validate_jsonld(filepath)
            status = "OK" if ok else f"SCHEMA ERROR: {msg}"
            print(f"  {status}  {filepath}")
            howto_count += 1

    print(f"\n=== Adding ItemList schema to cron + providers indexes ===\n")
    itemlist_count = 0
    for filepath, data in ITEMLIST_SCHEMAS.items():
        schema = make_itemlist(data)
        if inject(filepath, schema):
            ok, msg = validate_jsonld(filepath)
            status = "OK" if ok else f"SCHEMA ERROR: {msg}"
            print(f"  {status}  {filepath}")
            itemlist_count += 1

    print(f"\nDone. {howto_count} HowTo + {itemlist_count} ItemList schemas added.")
    print("\nRun:")
    print("  git add -A && git commit -m 'seo: HowTo schema on all 6 tools, ItemList on cron+providers indexes' && git push origin main && npx vercel --prod --force")
    print("\nGSC — validate fix on Enhancements after deploy.")
