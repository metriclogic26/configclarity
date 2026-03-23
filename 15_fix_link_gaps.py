#!/usr/bin/env python3
"""
Fix manual glossary link gaps identified by audit.
Run from: ~/Projects/CronSight/
"""

FIXES = {
    "fix/docker/ufw-bypass/index.html": [
        ("docker-ufw-bypass", "Docker UFW Bypass"),
        ("port-binding", "Port Binding"),
    ],
    "fix/docker/hardcoded-secrets/index.html": [
        ("hardcoded-secrets", "Hardcoded Secrets"),
    ],
    "fix/docker/missing-healthcheck/index.html": [
        ("healthcheck", "Docker Healthcheck"),
    ],
    "fix/docker/port-exposure/index.html": [
        ("port-binding", "Port Binding"),
        ("docker-ufw-bypass", "Docker UFW Bypass"),
    ],
}

GLOSSARY_GAPS = {
    "glossary/docker-ufw-bypass/index.html": [
        ("/fix/ufw/port-exposed-after-docker/", "Port still exposed after UFW deny"),
    ],
    "glossary/port-binding/index.html": [
        ("/fix/docker/ufw-bypass/", "Docker UFW bypass fix"),
    ],
    "glossary/reverse-proxy/index.html": [
        ("/fix/proxy/dangling-routes/", "Dangling routes fix"),
        ("/fix/proxy/missing-ssl-redirect/", "Missing SSL redirect fix"),
    ],
    "glossary/dangling-route/index.html": [
        ("/fix/proxy/dangling-routes/", "Dangling routes fix"),
    ],
    "glossary/resource-limits/index.html": [
        ("/fix/docker/port-exposure/", "Docker port exposure fix"),
    ],
    "glossary/log-overflow/index.html": [
        ("/fix/docker/missing-healthcheck/", "Docker missing healthcheck fix"),
    ],
}

BLOG_GAPS = {
    "blog/docker-ufw-bypass-explained/index.html": [
        ("/glossary/docker-ufw-bypass/", "Docker UFW Bypass"),
    ],
    "blog/cron-job-best-practices/index.html": [
        ("/glossary/cron-job-collision/", "Cron Job Collision"),
        ("/glossary/flock-safety/", "flock Safety"),
    ],
    "blog/ssl-certificate-monitoring-guide/index.html": [
        ("/glossary/ssl-certificate-expiry/", "SSL Certificate Expiry"),
    ],
    "blog/traefik-v2-to-v3-migration/index.html": [
        ("/glossary/traefik-labels/", "Traefik Labels"),
        ("/glossary/reverse-proxy/", "Reverse Proxy"),
    ],
}

UL_STYLE = 'style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;"'


def inject(filepath, links_html, section_title="Related Glossary Terms"):
    with open(filepath, "r") as f:
        content = f.read()

    # Skip if first link already present
    first_href = links_html.split('href="')[1].split('"')[0]
    if first_href in content:
        print(f"  SKIP {filepath} — already has {first_href}")
        return

    insert = f'\n    <h2>{section_title}</h2>\n    <ul {UL_STYLE}>{links_html}</ul>\n'

    if "<footer" in content:
        content = content.replace("<footer", insert + "  <footer", 1)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  OK   {filepath}")
    else:
        print(f"  FAIL {filepath} — no <footer> anchor found")


if __name__ == "__main__":
    print("=== Fixing Manual Link Gaps ===\n")

    print("--- Docker fix pages → glossary ---")
    for filepath, terms in FIXES.items():
        links = "".join([
            f'<li><a href="/glossary/{s}/">{n}</a></li>'
            for s, n in terms
        ])
        inject(filepath, links)

    print("\n--- Glossary pages → fix pages ---")
    for filepath, links_data in GLOSSARY_GAPS.items():
        links = "".join([
            f'<li><a href="{url}">{label}</a></li>'
            for url, label in links_data
        ])
        inject(filepath, links, "Related Fix Guides")

    print("\n--- Blog posts → glossary ---")
    for filepath, links_data in BLOG_GAPS.items():
        links = "".join([
            f'<li><a href="{url}">{label}</a></li>'
            for url, label in links_data
        ])
        inject(filepath, links, "Related Glossary Terms")

    print("\nDone.")
