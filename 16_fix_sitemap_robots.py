#!/usr/bin/env python3
"""
Script 16: Fix robots.txt (missing), sitemap-seo.xml gaps, llms.txt incidents.
Run from: ~/Projects/CronSight/
"""

import os
from datetime import date

TODAY = date.today().isoformat()
BASE = "https://configclarity.dev"

# ── 1. robots.txt ─────────────────────────────────────────────────────────────

ROBOTS = """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: https://configclarity.dev/sitemap.xml
Sitemap: https://configclarity.dev/sitemap-seo.xml
"""

# ── 2. Missing sitemap-seo.xml entries ────────────────────────────────────────

# Blog posts missing from sitemap (ollama + openclaw + index shows 7, need 9)
MISSING_BLOG = [
    "/blog/",
    "/blog/docker-ufw-bypass-explained/",
    "/blog/cron-job-best-practices/",
    "/blog/ssl-certificate-monitoring-guide/",
    "/blog/ollama-server-security/",
    "/blog/openclaw-server-audit/",
    "/blog/traefik-v2-to-v3-migration/",
    "/blog/ollama-server-security/",
    "/blog/openclaw-server-audit/",
]

# error/vs only show 1 each — need full lists
MISSING_ERROR = [
    "/error/",
    "/error/docker-ufw-bypass/",
    "/error/nginx-502-bad-gateway/",
    "/error/cron-not-running/",
    "/error/ufw-inactive-still-open/",
    "/error/permission-denied-docker-socket/",
]

MISSING_VS = [
    "/vs/",
    "/vs/crontab-guru/",
    "/vs/docker-bench-security/",
    "/vs/ssl-labs/",
]

# ── 3. llms.txt additions ─────────────────────────────────────────────────────

LLMS_ADDITIONS = """
## Incident Reports
- https://configclarity.dev/incidents/
- https://configclarity.dev/incidents/docker-ufw-bypass/
- https://configclarity.dev/incidents/ssl-expiry-outages/
- https://configclarity.dev/incidents/docker-secrets-exposed/

## Blog (additional posts)
- https://configclarity.dev/blog/ollama-server-security/
- https://configclarity.dev/blog/openclaw-server-audit/
"""


if __name__ == "__main__":
    print("=== Fixing robots.txt, sitemap-seo.xml, llms.txt ===\n")

    # 1. Write robots.txt
    with open("robots.txt", "w") as f:
        f.write(ROBOTS)
    print("  ✅ robots.txt created")
    print("     AI crawlers: GPTBot, ClaudeBot, PerplexityBot, Bytespider, Google-Extended")
    print("     Sitemaps: sitemap.xml + sitemap-seo.xml")

    # 2. Fix sitemap-seo.xml
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()

    added = 0
    all_missing = []

    # Deduplicate — build a clean list of URLs not already in sitemap
    seen = set()
    for url in MISSING_BLOG + MISSING_ERROR + MISSING_VS:
        if url in seen:
            continue
        seen.add(url)
        if url not in sitemap:
            all_missing.append(url)

    if all_missing:
        entries = "\n".join([
            f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
            for u in all_missing
        ])
        sitemap = sitemap.replace("</urlset>", entries + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
        added = len(all_missing)

    print(f"\n  ✅ sitemap-seo.xml — {added} missing URLs added")

    # Recount
    blog_count = sitemap.count("/blog/")
    error_count = sitemap.count("/error/")
    vs_count = sitemap.count("/vs/")
    incidents_count = sitemap.count("/incidents/")
    total = sitemap.count("<loc>")
    print(f"     Total URLs: {total}")
    print(f"     blog: {blog_count} | error: {error_count} | vs: {vs_count} | incidents: {incidents_count}")

    # 3. Fix llms.txt
    with open("llms.txt", "r") as f:
        llms = f.read()

    added_llms = []
    if "incidents" not in llms:
        llms = llms.rstrip() + "\n" + LLMS_ADDITIONS
        added_llms.append("incidents section")
    if "ollama-server-security" not in llms:
        added_llms.append("ollama post")
    if "openclaw-server-audit" not in llms:
        added_llms.append("openclaw post")

    with open("llms.txt", "w") as f:
        f.write(llms)

    if added_llms:
        print(f"\n  ✅ llms.txt — added: {', '.join(added_llms)}")
    else:
        print(f"\n  SKIP llms.txt — all entries already present")

    print(f"\n=== Verification ===")
    print(f"  robots.txt exists: {os.path.exists('robots.txt')}")
    print(f"  robots.txt size:   {os.path.getsize('robots.txt')} bytes")

    print(f"\nPush:")
    print(f"  git add -A && git commit -m 'fix: robots.txt, sitemap gaps, llms.txt incidents' && git push origin main && npx vercel --prod --force")

    print(f"\nVerify live:")
    print(f"  curl https://www.configclarity.dev/robots.txt")
    print(f"  curl -sI https://www.configclarity.dev/sitemap-seo.xml | grep HTTP")
