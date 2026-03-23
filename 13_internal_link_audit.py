#!/usr/bin/env python3
"""
Script 13: Internal linking audit.
Checks:
  - Every fix page → links to relevant glossary terms
  - Every glossary term → links back to relevant fix pages
  - Every blog post → links to relevant tools and fix pages
  - Every provider page → links to relevant fix pages
Outputs a report of gaps and optionally injects missing links.
Run from: ~/Projects/CronSight/
"""

import os, re, glob

BASE = "https://configclarity.dev"

# ── LINK MAP — what each page type should link to ─────────────────────────────

# fix page slug → glossary slugs it should reference
FIX_TO_GLOSSARY = {
    "docker/ufw-bypass":       ["docker-ufw-bypass", "port-binding"],
    "docker/hardcoded-secrets":["hardcoded-secrets"],
    "docker/missing-healthcheck":["healthcheck"],
    "docker/port-exposure":    ["port-binding", "docker-ufw-bypass"],
    "ufw/docker-bypass":       ["docker-ufw-bypass", "port-binding"],
    "ufw/ipv6-mismatch":       ["ipv6-mismatch"],
    "ufw/default-deny-missing":["docker-ufw-bypass"],
    "ufw/port-exposed-after-docker":["docker-ufw-bypass", "port-binding"],
    "nftables/ubuntu-22":      ["nftables"],
    "nftables/docker-conflict":["nftables", "docker-ufw-bypass"],
    "cron/overlapping-jobs":   ["cron-job-collision", "flock-safety"],
    "cron/silent-failure":     ["cron-job-collision"],
    "cron/flock-safety":       ["flock-safety", "cron-job-collision"],
    "cron/server-load-spike":  ["cron-job-collision"],
    "cron/ai-agent-collision": ["cron-job-collision", "flock-safety"],
    "ssl/expiry-monitoring":   ["ssl-certificate-expiry"],
    "ssl/cdn-domain":          ["ssl-certificate-expiry"],
    "ssl/traefik-renewal":     ["ssl-certificate-expiry", "traefik-labels"],
    "ssl/nginx-renewal":       ["ssl-certificate-expiry"],
    "ssl/200-day-warning":     ["ssl-certificate-expiry"],
    "nginx/502-bad-gateway":   ["dangling-route", "reverse-proxy"],
    "nginx/upstream-timeout":  ["reverse-proxy"],
    "nginx/ssl-redirect-missing":["reverse-proxy"],
    "proxy/traefik-v2-to-v3":  ["traefik-labels", "reverse-proxy"],
    "proxy/dangling-routes":   ["dangling-route", "reverse-proxy"],
    "proxy/missing-ssl-redirect":["reverse-proxy"],
    "proxy/cors-double-header":["reverse-proxy"],
}

# glossary slug → fix page slugs it should link to
GLOSSARY_TO_FIX = {
    "docker-ufw-bypass":    ["fix/docker/ufw-bypass", "fix/ufw/docker-bypass", "fix/ufw/port-exposed-after-docker"],
    "port-binding":         ["fix/docker/port-exposure", "fix/docker/ufw-bypass"],
    "ssl-certificate-expiry":["fix/ssl/expiry-monitoring", "fix/ssl/nginx-renewal", "fix/ssl/traefik-renewal"],
    "cron-job-collision":   ["fix/cron/overlapping-jobs", "fix/cron/flock-safety", "fix/cron/server-load-spike"],
    "flock-safety":         ["fix/cron/flock-safety", "fix/cron/overlapping-jobs"],
    "reverse-proxy":        ["fix/nginx/502-bad-gateway", "fix/proxy/dangling-routes", "fix/proxy/missing-ssl-redirect"],
    "traefik-labels":       ["fix/proxy/traefik-v2-to-v3"],
    "hardcoded-secrets":    ["fix/docker/hardcoded-secrets"],
    "healthcheck":          ["fix/docker/missing-healthcheck"],
    "nftables":             ["fix/nftables/ubuntu-22", "fix/nftables/docker-conflict"],
    "ipv6-mismatch":        ["fix/ufw/ipv6-mismatch"],
    "dangling-route":       ["fix/proxy/dangling-routes", "fix/nginx/502-bad-gateway"],
    "resource-limits":      ["fix/docker/port-exposure"],
    "log-overflow":         ["fix/docker/missing-healthcheck"],
}

# blog slug → tools/pages it should link to
BLOG_TO_TOOLS = {
    "docker-ufw-bypass-explained": ["/firewall/", "/docker/", "/glossary/docker-ufw-bypass/"],
    "cron-job-best-practices":     ["/", "/glossary/cron-job-collision/", "/glossary/flock-safety/"],
    "ssl-certificate-monitoring-guide": ["/ssl/", "/glossary/ssl-certificate-expiry/"],
    "traefik-v2-to-v3-migration":  ["/proxy/", "/glossary/traefik-labels/", "/glossary/reverse-proxy/"],
    "ollama-server-security":      ["/docker/", "/firewall/"],
    "openclaw-server-audit":       ["/docker/", "/firewall/"],
}

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def check_links(content, required_hrefs):
    """Return list of hrefs that are missing from content."""
    missing = []
    for href in required_hrefs:
        # Check for the href in any <a href="..."> pattern
        if href not in content:
            missing.append(href)
    return missing

def inject_related_links(filepath, missing_glossary):
    """Inject missing glossary links into a fix page's Related Guides section or append one."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    links_html = "\n".join([
        f'<li><a href="/glossary/{slug}/">{slug.replace("-", " ").title()}</a></li>'
        for slug in missing_glossary
    ])

    # Try to find existing Related Guides / ul list near the bottom
    if '<h2>Related Guides</h2>' in content:
        content = content.replace(
            '<h2>Related Guides</h2>',
            f'<h2>Related Guides</h2>\n    <ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">{links_html}</ul>'
        )
    elif '</div>\n' + FOOTER_MARKER in content or FOOTER_MARKER in content:
        # Append before footer
        insert = f'\n    <h2>Related Glossary Terms</h2>\n    <ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">{links_html}</ul>\n  '
        content = content.replace(FOOTER_MARKER, insert + FOOTER_MARKER)
    else:
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

FOOTER_MARKER = '<footer>'


# ── AUDIT ─────────────────────────────────────────────────────────────────────

def run_audit():
    gaps = []
    injected = []

    print("=== Internal Linking Audit ===\n")

    # 1. Fix pages → glossary
    print("--- Fix pages missing glossary links ---")
    fix_gap_count = 0
    for fix_rel, glossary_slugs in FIX_TO_GLOSSARY.items():
        filepath = f"fix/{fix_rel}/index.html"
        if not os.path.exists(filepath):
            continue
        content = read_file(filepath)
        required = [f"/glossary/{s}/" for s in glossary_slugs]
        missing = check_links(content, required)
        if missing:
            fix_gap_count += len(missing)
            gaps.append((filepath, missing))
            # Auto-inject
            missing_slugs = [m.strip("/").split("/")[-1] for m in missing]
            ok = inject_related_links(filepath, missing_slugs)
            if ok:
                injected.append(filepath)
                print(f"  ✅ FIXED {filepath} — injected: {', '.join(missing_slugs)}")
            else:
                print(f"  ⚠️  GAP  {filepath} — missing: {', '.join(missing)} (manual fix needed)")
    if fix_gap_count == 0:
        print("  All fix pages have required glossary links ✅")

    # 2. Glossary pages → fix pages
    print("\n--- Glossary pages missing fix links ---")
    glossary_gap_count = 0
    for slug, fix_paths in GLOSSARY_TO_FIX.items():
        filepath = f"glossary/{slug}/index.html"
        if not os.path.exists(filepath):
            continue
        content = read_file(filepath)
        required = [f"/{p}/" for p in fix_paths]
        missing = check_links(content, required)
        if missing:
            glossary_gap_count += len(missing)
            print(f"  ⚠️  GAP  {filepath} — missing: {', '.join(missing)}")
    if glossary_gap_count == 0:
        print("  All glossary pages have required fix links ✅")

    # 3. Blog posts → tools
    print("\n--- Blog posts missing tool links ---")
    blog_gap_count = 0
    for slug, hrefs in BLOG_TO_TOOLS.items():
        filepath = f"blog/{slug}/index.html"
        if not os.path.exists(filepath):
            continue
        content = read_file(filepath)
        missing = check_links(content, hrefs)
        if missing:
            blog_gap_count += len(missing)
            print(f"  ⚠️  GAP  {filepath} — missing: {', '.join(missing)}")
    if blog_gap_count == 0:
        print("  All blog posts have required tool links ✅")

    # 4. Provider pages — spot check for fix page links
    print("\n--- Provider pages — spot check ---")
    provider_files = glob.glob("providers/*/*/index.html")
    provider_with_links = sum(1 for f in provider_files if "/fix/" in read_file(f) or "configclarity.dev" in read_file(f))
    print(f"  {provider_with_links}/{len(provider_files)} provider pages contain internal links")
    if provider_with_links < len(provider_files) * 0.5:
        print("  ⚠️  Less than 50% of provider pages have internal links — consider adding fix page links")

    # Summary
    print(f"\n=== Summary ===")
    print(f"  Fix→Glossary gaps:  {fix_gap_count} (auto-injected where possible)")
    print(f"  Glossary→Fix gaps:  {glossary_gap_count} (manual — add to glossary pages)")
    print(f"  Blog→Tool gaps:     {blog_gap_count} (links already embedded in post content)")
    print(f"  Files modified:     {len(injected)}")

    if len(injected) > 0:
        print(f"\nFiles updated — push when ready:")
        print(f"  git add -A && git commit -m 'seo: inject missing glossary links into fix pages' && git push origin main && npx vercel --prod --force")
    else:
        print(f"\nNo auto-injections needed — all links already present.")

if __name__ == "__main__":
    run_audit()
