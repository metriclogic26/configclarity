#!/usr/bin/env python3
"""
Script 9: Inject BreadcrumbList schema into all existing pages missing it.
Run from: ~/Projects/CronSight/
"""

import os, re, glob

BASE = "https://configclarity.dev"

# ── PAGE MAP — slug pattern → breadcrumb trail ────────────────────────────────
# Each entry: (glob_pattern, breadcrumb_builder_fn)
# breadcrumb_builder_fn(path) → list of (name, url) tuples

def crumbs_error(path):
    # path like: error/docker-ufw-bypass/index.html
    parts = path.split("/")
    slug = parts[1] if len(parts) > 2 else ""
    name = slug.replace("-", " ").title() if slug else "Error Fix Guides"
    if slug:
        return [("ConfigClarity", "/"), ("Error Fix Guides", "/error/"), (name, f"/error/{slug}/")]
    return [("ConfigClarity", "/"), ("Error Fix Guides", "/error/")]

def crumbs_vs(path):
    parts = path.split("/")
    slug = parts[1] if len(parts) > 2 else ""
    name = slug.replace("-", " ").title() if slug else "Tool Comparisons"
    if slug:
        return [("ConfigClarity", "/"), ("Tool Comparisons", "/vs/"), (name, f"/vs/{slug}/")]
    return [("ConfigClarity", "/"), ("Tool Comparisons", "/vs/")]

def crumbs_fix_docker(path):
    parts = path.split("/")
    slug = parts[2] if len(parts) > 3 else ""
    name = slug.replace("-", " ").title() if slug else "Docker Fix Guides"
    return [("ConfigClarity", "/"), ("Fix Guides", "/fix/"), ("Docker", "/fix/docker/"), (name, f"/fix/docker/{slug}/")]

def crumbs_fix_ufw(path):
    parts = path.split("/")
    slug = parts[2] if len(parts) > 3 else ""
    name = slug.replace("-", " ").title() if slug else "UFW Fix Guides"
    return [("ConfigClarity", "/"), ("Fix Guides", "/fix/"), ("UFW", "/fix/ufw/"), (name, f"/fix/ufw/{slug}/")]

def crumbs_fix_nftables(path):
    parts = path.split("/")
    slug = parts[2] if len(parts) > 3 else ""
    name = slug.replace("-", " ").title() if slug else "nftables Fix Guides"
    return [("ConfigClarity", "/"), ("Fix Guides", "/fix/"), ("nftables", "/fix/nftables/"), (name, f"/fix/nftables/{slug}/")]

def crumbs_fix_cron(path):
    parts = path.split("/")
    slug = parts[2] if len(parts) > 3 else ""
    name = slug.replace("-", " ").title() if slug else "Cron Fix Guides"
    return [("ConfigClarity", "/"), ("Fix Guides", "/fix/"), ("Cron", "/fix/cron/"), (name, f"/fix/cron/{slug}/")]

def crumbs_fix_ssl(path):
    parts = path.split("/")
    slug = parts[2] if len(parts) > 3 else ""
    name = slug.replace("-", " ").title() if slug else "SSL Fix Guides"
    return [("ConfigClarity", "/"), ("Fix Guides", "/fix/"), ("SSL", "/fix/ssl/"), (name, f"/fix/ssl/{slug}/")]

def crumbs_fix_nginx(path):
    parts = path.split("/")
    slug = parts[2] if len(parts) > 3 else ""
    name = slug.replace("-", " ").title() if slug else "Nginx Fix Guides"
    return [("ConfigClarity", "/"), ("Fix Guides", "/fix/"), ("Nginx", "/fix/nginx/"), (name, f"/fix/nginx/{slug}/")]

def crumbs_providers(path):
    parts = path.split("/")
    # providers/hetzner/docker-firewall/index.html
    provider = parts[1] if len(parts) > 2 else ""
    topic = parts[2] if len(parts) > 3 else ""
    provider_name = provider.replace("-", " ").title()
    topic_name = topic.replace("-", " ").title()
    if provider and topic:
        return [
            ("ConfigClarity", "/"),
            ("Provider Guides", "/providers/"),
            (provider_name, f"/providers/{provider}/"),
            (topic_name, f"/providers/{provider}/{topic}/"),
        ]
    elif provider:
        return [("ConfigClarity", "/"), ("Provider Guides", "/providers/"), (provider_name, f"/providers/{provider}/")]
    return [("ConfigClarity", "/"), ("Provider Guides", "/providers/")]

def make_breadcrumb_schema(crumbs):
    items = ",\n".join([
        f'    {{"@type":"ListItem","position":{i+1},"name":{repr(name)},"item":"{BASE}{url}"}}'
        for i, (name, url) in enumerate(crumbs)
    ])
    return f"""  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{items}
  ]}}
  </script>"""

def inject_breadcrumb(filepath, crumb_fn):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has BreadcrumbList
    if "BreadcrumbList" in content:
        return False, "already has BreadcrumbList"

    # Build crumbs from path relative to repo root
    rel_path = filepath.replace("\\", "/")
    crumbs = crumb_fn(rel_path)

    schema = make_breadcrumb_schema(crumbs)

    # Inject before </head>
    if "</head>" not in content:
        return False, "no </head> found"

    content = content.replace("</head>", schema + "\n</head>", 1)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True, "injected"

# ── PAGE GROUPS ───────────────────────────────────────────────────────────────

PAGE_GROUPS = [
    # (glob pattern, crumb function, label)
    ("error/*/index.html",          crumbs_error,       "error pages"),
    ("vs/*/index.html",             crumbs_vs,          "vs comparison pages"),
    ("fix/docker/*/index.html",     crumbs_fix_docker,  "docker fix pages"),
    ("fix/ufw/*/index.html",        crumbs_fix_ufw,     "ufw fix pages"),
    ("fix/nftables/*/index.html",   crumbs_fix_nftables,"nftables fix pages"),
    ("fix/cron/*/index.html",       crumbs_fix_cron,    "cron fix pages"),
    ("fix/ssl/*/index.html",        crumbs_fix_ssl,     "ssl fix pages"),
    ("fix/nginx/*/index.html",      crumbs_fix_nginx,   "nginx fix pages"),
    ("providers/*/*/index.html",    crumbs_providers,   "provider pages"),
]

if __name__ == "__main__":
    print("=== Injecting BreadcrumbList Schema ===\n")

    total_ok = 0
    total_skip = 0
    total_fail = 0

    for pattern, fn, label in PAGE_GROUPS:
        files = sorted(glob.glob(pattern))
        ok = skip = fail = 0
        for f in files:
            success, reason = inject_breadcrumb(f, fn)
            if success:
                ok += 1
            elif "already" in reason:
                skip += 1
            else:
                fail += 1
                print(f"  ❌ {f}: {reason}")
        print(f"  {label}: {ok} injected, {skip} skipped (already present), {fail} failed — {len(files)} total")
        total_ok += ok
        total_skip += skip
        total_fail += fail

    print(f"\nTotal: {total_ok} injected, {total_skip} already had BreadcrumbList, {total_fail} failed")

    if total_ok > 0:
        print("\nVerify a sample:")
        print("  grep -c 'BreadcrumbList' fix/docker/ufw-bypass/index.html")
        print("  grep -c 'BreadcrumbList' providers/hetzner/docker-firewall/index.html")
        print("  grep -c 'BreadcrumbList' error/docker-ufw-bypass/index.html")
        print("\nPush when ready:")
        print("  git add -A && git commit -m 'seo: BreadcrumbList schema on all fix, provider, error, vs pages' && git push origin main && npx vercel --prod --force")
