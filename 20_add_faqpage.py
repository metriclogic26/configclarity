#!/usr/bin/env python3
"""
Script 20: Add FAQPage schema to 5 tool pages missing it.
Run from: ~/Projects/CronSight/
"""
import re, json

FAQS = {
    "index.html": [
        ("What does the Cron Visualiser check?",
         "It parses your crontab and renders a 24-hour timeline showing every job's execution window. It detects overlapping jobs, server load spikes at peak minutes, missing flock safety, and @reboot jobs."),
        ("Does this tool send my crontab anywhere?",
         "No. All processing happens entirely in your browser using JavaScript. Your crontab output never leaves your machine."),
        ("What is a cron job overlap?",
         "A cron job overlap occurs when two or more jobs are scheduled to run at the same time and compete for the same server resources — CPU, disk I/O, or database connections. This can cause performance degradation or data corruption."),
        ("What is flock safety for cron jobs?",
         "flock safety means wrapping your cron command with flock -n /tmp/jobname.lock command. If the previous run is still executing when the next scheduled run starts, the new invocation exits immediately instead of running concurrently."),
    ],
    "ssl/index.html": [
        ("What does the SSL Certificate Checker do?",
         "It checks multiple domains at once for certificate expiry dates, issuer information, CDN domain detection, and certificate chain validation. It flags anything expiring within 200 days — not the standard 30 — to catch broken renewal pipelines early."),
        ("Does this tool send my domain list anywhere?",
         "The tool queries the public Certificate Transparency log API (crt.sh) using your domain names. No data is stored. The queries are the same as any browser making a public API request."),
        ("Why does ConfigClarity flag certificates at 200 days instead of 30?",
         "Let's Encrypt certificates expire every 90 days and are designed to auto-renew at 60 days remaining. If renewal breaks on day 1, a 30-day alert fires at day 60 — giving you 30 days to debug a failure that has been silent for 60. The 200-day threshold catches broken renewal pipelines while you still have runway."),
        ("What does the orange CDN flag mean on SSL results?",
         "An orange flag indicates the domain is fronted by a CDN (Cloudflare, Fastly, Akamai). CDN-fronted domains have two certificates — the CDN edge certificate and the origin certificate. The tool flags these because most monitoring only checks the CDN cert, missing the origin cert expiry."),
    ],
    "firewall/index.html": [
        ("What does the Firewall Auditor check?",
         "It analyses your ufw status verbose output for Docker UFW bypass risk, missing default-deny rules, high-risk open ports (Redis, PostgreSQL, Docker socket, VNC, Jupyter), IPv4 and IPv6 rule mismatches, and missing localhost bindings on container ports."),
        ("Does this tool send my firewall rules anywhere?",
         "No. All analysis happens in your browser. Your ufw status output is parsed locally using JavaScript and never transmitted to any server."),
        ("What is the Docker UFW bypass problem?",
         "Docker inserts rules into the iptables FORWARD chain which is evaluated before UFW's INPUT chain. This means container ports published with ports: PORT:PORT in docker-compose.yml are accessible from the internet even when UFW has a deny rule for that port. The fix is to bind container ports to 127.0.0.1."),
        ("What are high-risk open ports?",
         "High-risk ports are service ports that should never be publicly accessible — Redis (6379), PostgreSQL (5432), MongoDB (27017), MySQL (3306), Docker socket (2375), Elasticsearch (9200), and others. These services are commonly exposed accidentally via Docker and are frequent targets for automated scanners."),
    ],
    "proxy/index.html": [
        ("What does the Reverse Proxy Mapper check?",
         "It parses your nginx.conf or docker-compose.yml with Traefik labels to detect dangling routes pointing to stopped services, missing SSL redirects, duplicate CORS headers, and deprecated Traefik v1 label patterns that silently do nothing in v3."),
        ("Does this tool send my nginx config anywhere?",
         "No. All parsing happens in your browser using JavaScript. Your configuration files never leave your machine."),
        ("What is a dangling reverse proxy route?",
         "A dangling route is a proxy configuration entry pointing to a backend that no longer exists — a container that was stopped, a service that was removed, or a hostname that no longer resolves. Nginx returns 502 for all requests to dangling routes."),
        ("What Traefik v1 labels does the tool detect?",
         "The tool detects traefik.frontend.rule, traefik.backend, traefik.port, and traefik.frontend.entryPoints — v1-style labels that were deprecated in v2 and completely ignored in v3. These labels produce no routes and no errors, making them silent failures after a Traefik upgrade."),
    ],
    "robots/index.html": [
        ("What does the robots.txt Validator check?",
         "It checks for syntax errors, accidental Disallow: / rules that block all crawlers, missing Sitemap directives, crawl-delay values over 10 seconds, unknown directives, and AI bot coverage — GPTBot, ClaudeBot, PerplexityBot, Bytespider, and Google-Extended."),
        ("Does this tool send my robots.txt content anywhere?",
         "In URL mode the tool fetches your live robots.txt from the public URL. In Paste mode all analysis happens in your browser. No data is stored or transmitted beyond the initial URL fetch."),
        ("What is the AI bot coverage check?",
         "The tool checks whether your robots.txt explicitly addresses major AI training crawlers — GPTBot (OpenAI), ClaudeBot (Anthropic), PerplexityBot, Bytespider (ByteDance), and Google-Extended. Explicit Allow directives improve GEO (Generative Engine Optimisation) — the likelihood your content is cited in AI search answers."),
        ("What does the robots.txt health score mean?",
         "The health score (0-100) summarises all checks. 100 means no issues detected. Points are deducted for missing sitemap reference, crawl-delay over 10 seconds, conflicting Allow and Disallow rules, missing AI bot directives, and syntax errors."),
    ],
}

def make_faqpage(faqs):
    items = ",\n".join([
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faqs
    ])
    return f'''  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}
  </script>'''

if __name__ == "__main__":
    print("=== Adding FAQPage schema to 5 tool pages ===\n")
    count = 0
    errors = []

    for filepath, faqs in FAQS.items():
        with open(filepath, "r") as f:
            content = f.read()

        if '"FAQPage"' in content:
            print(f"  SKIP {filepath} — FAQPage already present")
            continue

        schema = make_faqpage(faqs)

        # Validate JSON before injecting
        block = schema.split('<script type="application/ld+json">')[1].split("</script>")[0]
        try:
            json.loads(block)
        except Exception as e:
            print(f"  ERROR {filepath} — invalid JSON: {e}")
            errors.append(filepath)
            continue

        content = content.replace("</head>", schema + "\n</head>", 1)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  OK  {filepath}")
        count += 1

    # Final validation
    print(f"\n=== Validating all 6 tool pages ===\n")
    all_ok = True
    for filepath in ["index.html", "ssl/index.html", "docker/index.html",
                     "firewall/index.html", "proxy/index.html", "robots/index.html"]:
        with open(filepath) as f:
            content = f.read()
        has_faq = '"FAQPage"' in content
        has_howto = '"HowTo"' in content
        has_software = '"SoftwareApplication"' in content

        # Validate all JSON-LD
        import re as _re
        blocks = _re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, _re.DOTALL)
        schema_ok = True
        for b in blocks:
            try:
                json.loads(b)
            except:
                schema_ok = False

        status = "OK" if (has_faq and has_howto and has_software and schema_ok) else "MISSING"
        if status == "MISSING":
            all_ok = False
        print(f"  {status}  {filepath}  FAQ:{has_faq} HowTo:{has_howto} SoftwareApp:{has_software} JSON:{schema_ok}")

    print(f"\n{'All 6 tool pages complete' if all_ok else 'ISSUES FOUND'}")
    if not errors and all_ok:
        print("\nRun:")
        print("  git add -A && git commit -m 'seo: FAQPage schema on all 6 tool pages' && git push origin main && npx vercel --prod --force")
