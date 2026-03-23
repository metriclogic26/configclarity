#!/usr/bin/env python3
"""
Script 5: Update sitemap-seo.xml and vercel.json for all new pages.
Run from: ~/Projects/configclarity-fresh/
"""

import json
from datetime import date

TODAY = date.today().isoformat()
BASE = "https://configclarity.dev"

# All new pages from Dev6
NEW_PAGES = [
    # SoftwareApplication schema — no new pages

    # Index parent pages (4)
    ("/error/", "0.8", "monthly"),
    ("/vs/", "0.7", "monthly"),
    ("/fix/", "0.9", "weekly"),
    ("/providers/", "0.7", "monthly"),

    # Glossary (16)
    ("/glossary/", "0.9", "weekly"),
    ("/glossary/docker-ufw-bypass/", "0.8", "monthly"),
    ("/glossary/port-binding/", "0.8", "monthly"),
    ("/glossary/ssl-certificate-expiry/", "0.8", "monthly"),
    ("/glossary/cron-job-collision/", "0.8", "monthly"),
    ("/glossary/reverse-proxy/", "0.8", "monthly"),
    ("/glossary/traefik-labels/", "0.8", "monthly"),
    ("/glossary/flock-safety/", "0.8", "monthly"),
    ("/glossary/hardcoded-secrets/", "0.8", "monthly"),
    ("/glossary/healthcheck/", "0.8", "monthly"),
    ("/glossary/nftables/", "0.8", "monthly"),
    ("/glossary/ipv6-mismatch/", "0.8", "monthly"),
    ("/glossary/dangling-route/", "0.8", "monthly"),
    ("/glossary/resource-limits/", "0.8", "monthly"),
    ("/glossary/log-overflow/", "0.8", "monthly"),

    # robots.txt fix pages (26 including index)
    ("/fix/robots/", "0.8", "monthly"),
    ("/fix/robots/accidental-disallow-all/", "0.8", "monthly"),
    ("/fix/robots/blocking-css-js/", "0.8", "monthly"),
    ("/fix/robots/blocking-ai-bots/", "0.8", "monthly"),
    ("/fix/robots/missing-sitemap-reference/", "0.8", "monthly"),
    ("/fix/robots/wildcard-too-broad/", "0.7", "monthly"),
    ("/fix/robots/conflicting-rules/", "0.7", "monthly"),
    ("/fix/robots/crawl-delay-too-high/", "0.7", "monthly"),
    ("/fix/robots/case-sensitive-path/", "0.7", "monthly"),
    ("/fix/robots/noindex-vs-disallow/", "0.7", "monthly"),
    ("/fix/robots/wordpress/", "0.8", "monthly"),
    ("/fix/robots/shopify/", "0.8", "monthly"),
    ("/fix/robots/nextjs/", "0.8", "monthly"),
    ("/fix/robots/nuxt/", "0.8", "monthly"),
    ("/fix/robots/gatsby/", "0.7", "monthly"),
    ("/fix/robots/hugo/", "0.7", "monthly"),
    ("/fix/robots/block-gptbot/", "0.8", "monthly"),
    ("/fix/robots/block-claudebot/", "0.8", "monthly"),
    ("/fix/robots/block-perplexitybot/", "0.7", "monthly"),
    ("/fix/robots/block-bytespider/", "0.7", "monthly"),
    ("/fix/robots/block-all-ai-bots/", "0.8", "monthly"),
    ("/fix/robots/allow-ai-bots/", "0.8", "monthly"),
    ("/fix/robots/robots-txt-vs-noindex/", "0.8", "monthly"),
    ("/fix/robots/robots-txt-cheat-sheet/", "0.8", "monthly"),
    ("/fix/robots/what-is-crawl-budget/", "0.8", "monthly"),
    ("/fix/robots/robots-txt-for-ecommerce/", "0.8", "monthly"),
]

def build_sitemap_entries():
    return "\n".join([
        f"""  <url>
    <loc>{BASE}{path}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        for path, priority, freq in NEW_PAGES
    ])

def update_sitemap():
    try:
        with open("sitemap-seo.xml", "r") as f:
            content = f.read()
    except FileNotFoundError:
        # Create fresh if not found
        content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>"""

    new_entries = build_sitemap_entries()

    # Remove closing tag and append new entries
    content = content.replace("</urlset>", "")
    content = content.rstrip() + "\n" + new_entries + "\n</urlset>"

    with open("sitemap-seo.xml", "w") as f:
        f.write(content)

    entry_count = content.count("<loc>")
    print(f"  ✅ sitemap-seo.xml updated — {entry_count} total URLs, {len(NEW_PAGES)} new")


def update_vercel_json():
    try:
        with open("vercel.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {"rewrites": []}

    if "rewrites" not in config:
        config["rewrites"] = []

    # Build new rewrite rules for all new directory pages
    new_rewrites = []

    # Index parent pages
    for slug in ["error", "vs", "fix", "providers"]:
        rule = {"source": f"/{slug}", "destination": f"/{slug}/index.html"}
        if rule not in config["rewrites"]:
            new_rewrites.append(rule)

    # Glossary
    rule = {"source": "/glossary", "destination": "/glossary/index.html"}
    if rule not in config["rewrites"]:
        new_rewrites.append(rule)

    glossary_slugs = [
        "docker-ufw-bypass", "port-binding", "ssl-certificate-expiry",
        "cron-job-collision", "reverse-proxy", "traefik-labels", "flock-safety",
        "hardcoded-secrets", "healthcheck", "nftables", "ipv6-mismatch",
        "dangling-route", "resource-limits", "log-overflow"
    ]
    for slug in glossary_slugs:
        rule = {"source": f"/glossary/{slug}", "destination": f"/glossary/{slug}/index.html"}
        if rule not in config["rewrites"]:
            new_rewrites.append(rule)

    # robots.txt fix pages
    robots_slugs = [
        "accidental-disallow-all", "blocking-css-js", "blocking-ai-bots",
        "missing-sitemap-reference", "wildcard-too-broad", "conflicting-rules",
        "crawl-delay-too-high", "case-sensitive-path", "noindex-vs-disallow",
        "wordpress", "shopify", "nextjs", "nuxt", "gatsby", "hugo",
        "block-gptbot", "block-claudebot", "block-perplexitybot", "block-bytespider",
        "block-all-ai-bots", "allow-ai-bots",
        "robots-txt-vs-noindex", "robots-txt-cheat-sheet",
        "what-is-crawl-budget", "robots-txt-for-ecommerce"
    ]
    rule = {"source": "/fix/robots", "destination": "/fix/robots/index.html"}
    if rule not in config["rewrites"]:
        new_rewrites.append(rule)

    for slug in robots_slugs:
        rule = {"source": f"/fix/robots/{slug}", "destination": f"/fix/robots/{slug}/index.html"}
        if rule not in config["rewrites"]:
            new_rewrites.append(rule)

    config["rewrites"].extend(new_rewrites)

    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"  ✅ vercel.json updated — {len(new_rewrites)} new rewrites added, {len(config['rewrites'])} total")


def update_llms_txt():
    new_lines = [
        "",
        "## Glossary",
    ] + [
        f"- https://configclarity.dev/glossary/{slug}/"
        for slug in [
            "docker-ufw-bypass", "port-binding", "ssl-certificate-expiry",
            "cron-job-collision", "reverse-proxy", "traefik-labels", "flock-safety",
            "hardcoded-secrets", "healthcheck", "nftables", "ipv6-mismatch",
            "dangling-route", "resource-limits", "log-overflow"
        ]
    ] + [
        "",
        "## robots.txt Fix Guides",
    ] + [
        f"- https://configclarity.dev/fix/robots/{slug}/"
        for slug in [
            "accidental-disallow-all", "blocking-css-js", "blocking-ai-bots",
            "missing-sitemap-reference", "wildcard-too-broad", "conflicting-rules",
            "crawl-delay-too-high", "case-sensitive-path", "noindex-vs-disallow",
            "wordpress", "shopify", "nextjs", "nuxt", "gatsby", "hugo",
            "block-gptbot", "block-claudebot", "block-perplexitybot", "block-bytespider",
            "block-all-ai-bots", "allow-ai-bots",
            "robots-txt-vs-noindex", "robots-txt-cheat-sheet",
            "what-is-crawl-budget", "robots-txt-for-ecommerce"
        ]
    ]

    try:
        with open("llms.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "# ConfigClarity\n"

    # Avoid duplicates
    if "## Glossary" not in content:
        content = content.rstrip() + "\n" + "\n".join(new_lines)
        with open("llms.txt", "w") as f:
            f.write(content)
        print(f"  ✅ llms.txt updated with glossary + robots.txt fix pages")
    else:
        print("  SKIP llms.txt — glossary section already present")


if __name__ == '__main__':
    print("=== Updating sitemap-seo.xml, vercel.json, llms.txt ===\n")
    update_sitemap()
    update_vercel_json()
    update_llms_txt()
    print(f"\nDone. {len(NEW_PAGES)} new pages registered.")
    print("\nNext steps:")
    print("  1. git add -A && git commit -m 'feat: glossary, index pages, robots.txt fix guides' && git push origin main")
    print("  2. npx vercel --prod --force")
    print("  3. Submit new pages to GSC (10/day, start with glossary index + highest-value fix pages)")
    print("\nTop 10 GSC submissions for Day 1:")
    print("  https://configclarity.dev/glossary/")
    print("  https://configclarity.dev/fix/")
    print("  https://configclarity.dev/glossary/docker-ufw-bypass/")
    print("  https://configclarity.dev/glossary/flock-safety/")
    print("  https://configclarity.dev/glossary/ssl-certificate-expiry/")
    print("  https://configclarity.dev/fix/robots/blocking-ai-bots/")
    print("  https://configclarity.dev/fix/robots/accidental-disallow-all/")
    print("  https://configclarity.dev/fix/robots/block-gptbot/")
    print("  https://configclarity.dev/fix/robots/wordpress/")
    print("  https://configclarity.dev/fix/robots/nextjs/")
