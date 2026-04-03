# ConfigClarity

Browser-based DevOps audit tools. No backend. No signup. Everything runs client-side. → **[configclarity.dev](https://configclarity.dev)**

## Tools

| Tool | What it does | URL |
|---|---|---|
| 🕐 Cron Builder & Visualiser | Build cron expressions, visualise overlaps on a 24h timeline, detect conflicts, export PNG/Markdown | [/](https://configclarity.dev/) |
| 🔒 SSL Certificate Checker | Check expiry, chain issues, and CDN coverage across multiple domains. 200-day early warnings. | [/ssl/](https://configclarity.dev/ssl/) |
| 🐳 Docker Compose Auditor | Scan for hardcoded secrets, missing healthchecks, port collisions, 0.0.0.0 bindings, and NVIDIA GPU config | [/docker/](https://configclarity.dev/docker/) |
| 🛡️ Firewall Rule Auditor | Paste `ufw status verbose` — audit for Docker bypass risk, missing default-deny, and IPv4/IPv6 mismatches | [/firewall/](https://configclarity.dev/firewall/) |
| 🔀 Reverse Proxy Mapper | Paste your Nginx or Traefik config — detect dangling routes, missing SSL redirects, Traefik v2→v3 issues | [/proxy/](https://configclarity.dev/proxy/) |
| 🤖 robots.txt Validator | Audit crawl directives, AI bot coverage (GPTBot, ClaudeBot, PerplexityBot), sitemap health, health score 0–100 | [/robots/](https://configclarity.dev/robots/) |

## Why no backend?

You shouldn't have to trust a SaaS tool with your production configs. ConfigClarity runs entirely in your browser — nothing is sent to any server, stored anywhere, or logged. The architecture is deliberate:

- SSL checks use the public crt.sh API, with 800ms sequential delays between domains to respect rate limits
- Docker, Firewall, Proxy, and robots.txt audits are pure client-side parsers — your config never leaves the tab
- Cron visualisation is computed locally using cronstrue for human-readable descriptions
- No analytics, no tracking, no CDN fingerprinting — the only external resource is JetBrains Mono from Google Fonts

You can verify thiew-source on any tool page. Everything is in one HTML file.

## Stack

- Vanilla HTML, CSS, JavaScript — no frameworks, no build step
- Deployed on Vercel via vercel.json routing
- Zero npm dependencies in production
- Single-file architecture per tool (each tool is one index.html)

## Design tokens

All tools share a consistent visual language:
```css
--bg:     #0b0d14   /* page background */
--bg2:    #10131f   /* card background */
--bg3:    #161924   /* input background */
--border: #1e2236
--purple: #6c63ff   /* primary accent */
--green:  #22c55e   /* pass / safe */
--orange: #f97316   /* warning / CDN */
--red:    #ef4444   /* critical / fail */
--text:   #e2e4f0
--text2:  #8a8fb5   /* secondary text */
```

Font: JetBrains Mono

## Architecture decisions (frozen)

These were made deliberately and are not up for debate in PRs:

- **crt.sh for SSL data** — not cert.ist. crt.sh has broader coverage and a stable API
- **Sequential SSL checks, not parallel** — parallel requests at 5+ domains reliabgger rate limiting
- **800ms delay between domains** — not negotiable, this is what keeps the tool working reliably
- **No `&limit=` on wildcard queries** — oldest-first ordering makes limits produce wrong results
- **Orange for CDN domains (not red)** — CDN-issued certs are valid; the colour signals "check manually with openssl" not "this is broken"
- **No backend, ever** — the no-backend constraint is the product, not a technical limitation
- **Suite capped at 6 tools** — identity is locked as a DevOps config audit suite. New tools belong in other MetricLogic suites.

## Repo structure
```
/index.html         → Cron Builder & Visualiser (home tool)
/ssl/index.html     → SSL Certificate Checker
/docker/index.html  → Docker Compose Auditor
/firewall/index.html → Firewall Rule Auditor
/proxy/index.html   → Reverse Proxy Mapper
/robots/index.html  → robots.txt Validator
/vercel.json        → Vercel routing config
/sitemap.xml        → Sitemap (tool pages)
/robots.txt         → Craw/llms.txt           → GEO / AI crawler context file
```

## Contributing

Bug reports and edge case reports are the most valuable contributions. If a tool gives a wrong result, wrong severity, or misses something obvious — open an issue with the input that caused it.

PRs welcome for:
- New checks on existing tools
- Edge cases in existing parsers
- UI/UX improvements

PRs not accepted for:
- New tools — the suite is intentionally scoped to 6
- Backend additions — client-side only is a hard constraint
- Framework migrations — vanilla JS is intentional

## Part of the MetricLogic Network

ConfigClarity is one suite in the MetricLogic network of free developer tools. Hub page coming soon.

## Licence

MIT — Copyright (c) 2026 MetricLogic
