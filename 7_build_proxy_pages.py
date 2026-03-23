#!/usr/bin/env python3
"""
Script 7: Build Proxy Mapper SEO pages (23 pages).
Run from: ~/Projects/CronSight/
"""

import os, json
from datetime import date

TODAY = date.today().isoformat()
BASE = "https://configclarity.dev"

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

CSS = """
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root { --bg:#0b0d14; --bg2:#1e2130; --purple:#6c63ff; --green:#22c55e; --orange:#f97316; --red:#ef4444; --text:#e2e4f0; --muted:#8a8fb5; }
      body { background:var(--bg); color:var(--text); font-family:'JetBrains Mono',monospace; min-height:100vh; line-height:1.75; }
      a { color:var(--purple); text-decoration:none; } a:hover { text-decoration:underline; }
      .header { padding:1.5rem 2rem; border-bottom:1px solid #2a2d3d; display:flex; align-items:center; gap:1rem; }
      .header-logo { font-size:1.1rem; font-weight:700; color:var(--text); }
      .header-logo span { color:var(--purple); }
      .header-nav { margin-left:auto; display:flex; gap:1rem; font-size:0.8rem; }
      .header-nav a { color:var(--muted); }
      .breadcrumb { padding:1rem 2rem 0; max-width:760px; margin:0 auto; font-size:0.78rem; color:var(--muted); }
      .breadcrumb a { color:var(--muted); }
      .content { max-width:760px; margin:0 auto; padding:2rem; }
      h1 { font-size:1.6rem; font-weight:700; margin-bottom:1rem; }
      h2 { font-size:1.05rem; font-weight:700; margin:2rem 0 0.6rem; }
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1rem; }
      pre { background:#0d0f1a; border:1px solid #2a2d3d; border-radius:8px; padding:1.1rem 1.3rem; font-size:0.78rem; overflow-x:auto; margin:0.75rem 0 1.25rem; line-height:1.7; }
      code { background:#1e2130; padding:0.1rem 0.35rem; border-radius:3px; font-size:0.82rem; }
      .fix-box { background:var(--bg2); border-left:3px solid var(--green); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.25rem 0; }
      .fix-box .label { font-size:0.7rem; color:var(--green); text-transform:uppercase; letter-spacing:.06em; margin-bottom:0.4rem; }
      .warn-box { background:var(--bg2); border-left:3px solid var(--orange); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.25rem 0; }
      .warn-box p { margin-bottom:0; color:var(--text); }
      .faq-item { margin-bottom:1.4rem; }
      .faq-q { font-size:0.9rem; font-weight:600; margin-bottom:0.35rem; }
      .faq-a { font-size:0.84rem; color:var(--muted); }
      .cta { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.25rem 1.5rem; margin:2rem 0; text-align:center; }
      .cta p { color:var(--text); margin-bottom:0.6rem; font-size:0.875rem; }
      .cta a { display:inline-block; background:var(--purple); color:#fff; padding:0.45rem 1.2rem; border-radius:6px; font-size:0.82rem; font-weight:700; }
      footer { text-align:center; padding:2rem; font-size:0.75rem; color:var(--muted); border-top:1px solid #2a2d3d; margin-top:2rem; }
    </style>
"""

HEADER = """  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a><a href="/ssl/">SSL</a><a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a><a href="/proxy/">Proxy</a><a href="/robots/">robots.txt</a>
    </nav>
  </header>"""

FOOTER = """  <footer>
    <p><a href="/fix/">Fix Guides</a> &nbsp;·&nbsp; <a href="/glossary/">Glossary</a> &nbsp;·&nbsp;
    <a href="https://metriclogic.dev">MetricLogic</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>"""

def fix_page(slug, title, meta_desc, keywords, intro, sections, faqs, cta_text, cta_href, breadcrumb_label, breadcrumb_parent, breadcrumb_parent_href):
    faq_schema = ",\n".join([
        f'{{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}'
        for q, a in faqs
    ])
    faq_html = "\n".join([
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q, a in faqs
    ])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title} — ConfigClarity</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{BASE}/fix/proxy/{slug}/">
  <meta property="og:title" content="{title}"><meta property="og:description" content="{meta_desc}">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle","headline":"{title}",
    "url":"{BASE}/fix/proxy/{slug}/","description":"{meta_desc}",
    "author":{{"@type":"Organization","name":"MetricLogic"}},
    "datePublished":"{TODAY}"}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"{BASE}"}},
    {{"@type":"ListItem","position":2,"name":"Fix Guides","item":"{BASE}/fix/"}},
    {{"@type":"ListItem","position":3,"name":"{breadcrumb_parent}","item":"{BASE}{breadcrumb_parent_href}"}},
    {{"@type":"ListItem","position":4,"name":"{breadcrumb_label}","item":"{BASE}/fix/proxy/{slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="{breadcrumb_parent_href}">{breadcrumb_parent}</a> › {breadcrumb_label}
  </div>
  <div class="content">
    <h1>{title}</h1>
    <p>{intro}</p>
    {sections}
    <div class="cta"><p>{cta_text}</p><a href="{cta_href}">Open Reverse Proxy Mapper →</a></div>
    <h2>Frequently Asked Questions</h2>
    {faq_html}
  </div>
{FOOTER}
</body>
</html>"""


# ── 4 FIX PAGES ───────────────────────────────────────────────────────────────

PROXY_FIX_PAGES = [
    {
        "slug": "traefik-v2-to-v3",
        "title": "Fix: Traefik v2 to v3 Migration — Labels and Config Changes",
        "meta_desc": "How to migrate Traefik from v2 to v3. Fix broken Docker labels, Docker network configuration, removed allowEmptyServices, and deprecated v1 label patterns.",
        "keywords": "traefik v2 to v3 migration, traefik v3 labels, traefik upgrade fix, traefik v3 docker network",
        "intro": "Traefik v3 routes stop working silently after upgrading. The core label syntax is unchanged, but Docker provider network handling, some middleware options, and v1-style labels all need updating.",
        "sections": """
<h2>V1 Labels That No Longer Work</h2>
<p>These Traefik v1 labels were deprecated in v2 but silently ignored. In v3 they do nothing — and Traefik gives no warning:</p>
<div class="warn-box"><p>Remove these from your compose files: <code>traefik.frontend.rule</code>, <code>traefik.backend</code>, <code>traefik.port</code>, <code>traefik.frontend.entryPoints</code></p></div>
<div class="fix-box">
  <div class="label">CORRECT v3 Labels</div>
  <pre>traefik.enable=true
traefik.http.routers.myapp.rule=Host(`app.example.com`)
traefik.http.routers.myapp.entrypoints=websecure
traefik.http.routers.myapp.tls.certresolver=letsencrypt
traefik.http.services.myapp.loadbalancer.server.port=3000
traefik.docker.network=traefik-public</pre>
</div>

<h2>Docker Network Fix</h2>
<p>Traefik v3's Docker provider requires explicit network attachment. Create a shared external network and attach both Traefik and your services to it:</p>
<div class="fix-box">
  <div class="label">docker-compose.yml — Traefik service</div>
  <pre>services:
  traefik:
    image: traefik:v3
    networks:
      - traefik-public
networks:
  traefik-public:
    external: true</pre>
</div>
<div class="fix-box">
  <div class="label">docker-compose.yml — Application service</div>
  <pre>services:
  myapp:
    networks:
      - traefik-public
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=traefik-public"
      - "traefik.http.routers.myapp.rule=Host(`app.example.com`)"
networks:
  traefik-public:
    external: true</pre>
</div>
<pre># Create the network once:
docker network create traefik-public</pre>

<h2>Static Config Changes</h2>
<p>If you use <code>traefik.yml</code>, remove <code>swarmMode: false</code> from the Docker provider — it moved to a separate Swarm provider and causes a startup error in v3 if left in the Docker block.</p>
""",
        "faqs": [
            ("Why do my Traefik routes stop working after upgrading to v3?", "The most common causes are: (1) using old v1-style labels like traefik.frontend.rule that v3 silently ignores, (2) missing Docker network configuration — v3 requires explicit network attachment, (3) swarmMode: false left in the Docker provider static config. Use ConfigClarity's Reverse Proxy Mapper to detect v1 labels automatically."),
            ("Do I need to recreate my Docker network when upgrading to Traefik v3?", "No — if you already have an external Docker network for Traefik, keep it. Just ensure all services that need proxying are attached to it and have the traefik.docker.network label set explicitly."),
            ("What happened to allowEmptyServices in Traefik v3?", "allowEmptyServices was removed in v3. Traefik v3 handles empty services differently — it no longer requires this option to start when backends are unavailable. Simply remove it from your static config."),
        ],
        "cta_text": "Paste your docker-compose.yml to detect Traefik v1 label patterns and get exact v3 replacements.",
        "cta_href": "/proxy/",
        "breadcrumb_label": "Traefik v2 to v3",
        "breadcrumb_parent": "Proxy Fix Guides",
        "breadcrumb_parent_href": "/fix/proxy/",
    },
    {
        "slug": "dangling-routes",
        "title": "Fix: Dangling Reverse Proxy Routes Causing 502 Errors",
        "meta_desc": "How to find and fix dangling Nginx and Traefik routes pointing to stopped containers or removed services. Causes 502 Bad Gateway errors and log flooding.",
        "keywords": "nginx dangling route fix, reverse proxy 502 fix, traefik dangling route, nginx proxy_pass 502",
        "intro": "A dangling route is a reverse proxy config entry pointing to a backend that no longer exists. Nginx starts fine, logs no startup error, but returns 502 for every request to that route.",
        "sections": """
<h2>Finding Dangling Routes in Nginx</h2>
<p>Every <code>proxy_pass</code> target in your Nginx config should correspond to a running service. Check them manually:</p>
<pre># List all proxy_pass targets in your config:
grep -r "proxy_pass" /etc/nginx/sites-enabled/

# Then verify each upstream is reachable:
curl -sI http://127.0.0.1:PORT/</pre>

<h2>The Fix — Nginx</h2>
<div class="fix-box">
  <div class="label">Option 1: Remove the dangling server block</div>
  <pre># Remove or comment out the entire server block
# that points to the dead upstream:
# server {
#     server_name old-app.example.com;
#     location / { proxy_pass http://127.0.0.1:8080; }
# }</pre>
</div>
<div class="fix-box">
  <div class="label">Option 2: Return 410 Gone for retired services</div>
  <pre>server {
    server_name old-app.example.com;
    return 410;  # Gone — better than 502
}</pre>
</div>

<h2>Finding Dangling Routes in Traefik</h2>
<p>In Traefik with Docker labels, dangling routes appear when a container is removed but nothing else is pointing at the hostname. Check Traefik's dashboard at <code>http://localhost:8080</code> — any router showing 0 healthy servers is dangling.</p>
<pre># Check Traefik API for routers with no healthy backends:
curl http://localhost:8080/api/http/routers | \
  python3 -c "import json,sys; [print(r['name'], r.get('status','?')) for r in json.load(sys.stdin)]"</pre>
<div class="fix-box">
  <div class="label">After fixing — validate and reload</div>
  <pre>nginx -t && systemctl reload nginx</pre>
</div>
""",
        "faqs": [
            ("Why does Nginx start successfully with a dangling proxy_pass?", "Nginx validates configuration syntax at startup with nginx -t, but does not verify that upstream servers are reachable. The 502 error only appears at runtime when a request is made to the dangling route."),
            ("How do I prevent dangling routes when removing services?", "Before removing a service from docker-compose.yml, remove or update its Nginx server block or Traefik labels first. After removing the service, run nginx -t && systemctl reload nginx to confirm the config is clean."),
            ("What is the difference between a 502 and a 504 from a reverse proxy?", "502 Bad Gateway means the reverse proxy got an invalid response from the upstream — including no response at all (connection refused). 504 Gateway Timeout means the upstream started responding but took too long. Dangling routes to stopped services produce 502, not 504."),
        ],
        "cta_text": "Paste your nginx.conf or docker-compose labels to detect dangling routes automatically.",
        "cta_href": "/proxy/",
        "breadcrumb_label": "Dangling Routes",
        "breadcrumb_parent": "Proxy Fix Guides",
        "breadcrumb_parent_href": "/fix/proxy/",
    },
    {
        "slug": "missing-ssl-redirect",
        "title": "Fix: Nginx Missing HTTP to HTTPS Redirect",
        "meta_desc": "How to add a permanent HTTP to HTTPS redirect in Nginx. The exact server block for redirecting port 80 to 443 on Nginx, including Let's Encrypt ACME challenge compatibility.",
        "keywords": "nginx http to https redirect, nginx ssl redirect missing, nginx 301 redirect https, nginx port 80 redirect",
        "intro": "Without an HTTP to HTTPS redirect, visitors who type your domain without https:// land on an unencrypted page. Browsers don't always auto-upgrade. The fix is a one-block Nginx config addition.",
        "sections": """
<h2>The Fix — HTTP to HTTPS Redirect</h2>
<div class="fix-box">
  <div class="label">Add this server block to your Nginx config</div>
  <pre>server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;

    # Let's Encrypt ACME challenge — must come before redirect
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect everything else to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}</pre>
</div>
<div class="fix-box">
  <div class="label">Your HTTPS server block (keep as-is)</div>
  <pre>server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... rest of your config
}</pre>
</div>
<pre># Validate and reload:
nginx -t && systemctl reload nginx</pre>

<h2>Why the ACME challenge block matters</h2>
<p>If you redirect all port 80 traffic before the ACME challenge location, Let's Encrypt's HTTP-01 challenge will fail when certbot tries to renew. The challenge request hits port 80, gets redirected to HTTPS, and certbot can't complete the validation. Always put the <code>.well-known/acme-challenge/</code> location before the redirect.</p>
""",
        "faqs": [
            ("Should I use return 301 or rewrite for HTTP to HTTPS redirect in Nginx?", "Use return 301 https://$host$request_uri. It is faster than a rewrite rule, generates no regex overhead, and is the recommended approach in the Nginx documentation. Avoid rewrite ^(.*)$ https://$host$1 permanent — it is slower and error-prone."),
            ("Does the HTTP to HTTPS redirect break Let's Encrypt renewal?", "Only if you redirect before the ACME challenge location. Always add location /.well-known/acme-challenge/ { root /var/www/certbot; } before the redirect location / block. This lets certbot complete HTTP-01 challenges even with the redirect active."),
            ("How do I redirect www to non-www and HTTP to HTTPS at the same time?", "Use two server blocks: one for port 80 that redirects everything to https://yourdomain.com (non-www), and one for port 443 www that redirects to the non-www HTTPS. The main HTTPS server block then handles yourdomain.com only."),
        ],
        "cta_text": "Paste your nginx.conf to detect missing SSL redirects and get the exact fix block.",
        "cta_href": "/proxy/",
        "breadcrumb_label": "Missing SSL Redirect",
        "breadcrumb_parent": "Proxy Fix Guides",
        "breadcrumb_parent_href": "/fix/proxy/",
    },
    {
        "slug": "cors-double-header",
        "title": "Fix: Duplicate CORS Headers from Nginx and Application",
        "meta_desc": "When both Nginx and your application set CORS headers, browsers reject requests with 'The Access-Control-Allow-Origin header contains multiple values'. How to fix duplicate CORS headers.",
        "keywords": "duplicate cors headers nginx, cors multiple values fix, nginx cors double header, access-control-allow-origin multiple values",
        "intro": "Duplicate CORS headers cause browser errors like <code>The 'Access-Control-Allow-Origin' header contains multiple values 'https://app.com, https://app.com'</code>. This happens when both Nginx and your backend application set the same CORS headers independently.",
        "sections": """
<h2>Why This Happens</h2>
<p>Your Express/Django/FastAPI application returns <code>Access-Control-Allow-Origin: https://app.com</code>. Your Nginx config also adds <code>add_header Access-Control-Allow-Origin https://app.com</code>. Both headers are sent. Browsers reject multiple values for this header.</p>

<h2>Option 1: Remove CORS headers from Nginx (recommended)</h2>
<p>If your application already handles CORS correctly, remove the duplicate headers from Nginx:</p>
<div class="fix-box">
  <div class="label">Remove these lines from your Nginx location block</div>
  <pre># Delete or comment out:
# add_header Access-Control-Allow-Origin $http_origin;
# add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
# add_header Access-Control-Allow-Headers "Authorization, Content-Type";</pre>
</div>

<h2>Option 2: Remove CORS from your app, handle in Nginx</h2>
<p>Centralise CORS handling at the Nginx layer if you have multiple services that need the same policy:</p>
<div class="fix-box">
  <div class="label">Nginx CORS block — handles all CORS including preflight</div>
  <pre>location / {
    # Handle OPTIONS preflight
    if ($request_method = OPTIONS) {
        add_header Access-Control-Allow-Origin $http_origin always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;
        add_header Access-Control-Max-Age 3600 always;
        return 204;
    }

    add_header Access-Control-Allow-Origin $http_origin always;
    proxy_pass http://127.0.0.1:3000;
}</pre>
</div>
<p>Then disable CORS handling in your application entirely — let Nginx own it.</p>
""",
        "faqs": [
            ("Why do CORS headers get duplicated in Nginx?", "Nginx's add_header directive adds headers to the response, but does not remove existing headers set by the upstream application. If both Nginx and the application set Access-Control-Allow-Origin, both values appear in the response. Browsers reject multiple values for this header."),
            ("How do I check if I have duplicate CORS headers?", "Run: curl -sI -H 'Origin: https://yourapp.com' https://yourdomain.com/api/endpoint | grep -i access-control. If you see the same header twice, you have the duplication problem."),
            ("Does always in add_header matter for CORS?", "Yes. Without always, Nginx only adds headers to 2xx and 3xx responses. CORS headers need to be present on 4xx and 5xx responses too, otherwise browser error handling breaks. Always use add_header ... always for CORS headers."),
        ],
        "cta_text": "Paste your nginx.conf to detect CORS header duplication and missing always flags.",
        "cta_href": "/proxy/",
        "breadcrumb_label": "Duplicate CORS Headers",
        "breadcrumb_parent": "Proxy Fix Guides",
        "breadcrumb_parent_href": "/fix/proxy/",
    },
]

# ── 8 STACK/PROXY COMBO PAGES ─────────────────────────────────────────────────

PROXY_STACKS = [
    ("nginx", "Nginx"),
    ("traefik", "Traefik"),
    ("caddy", "Caddy"),
    ("nginx-proxy-manager", "Nginx Proxy Manager"),
]

PROXY_TOPICS = [
    ("ssl-setup", "SSL Setup", "How to configure SSL/TLS termination with {proxy}. Let's Encrypt auto-renewal, certificate paths, and HTTPS redirect."),
    ("docker-setup", "Docker Setup", "How to set up {proxy} as a reverse proxy for Docker containers. Network configuration, container labels, and port binding."),
]

def build_proxy_stack_page(proxy_slug, proxy_name, topic_slug, topic_title, topic_desc):
    desc = topic_desc.format(proxy=proxy_name)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{proxy_name} {topic_title} Guide — ConfigClarity</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{proxy_slug} {topic_slug.replace('-',' ')}, {proxy_slug} reverse proxy {topic_slug.replace('-',' ')}, {proxy_slug} docker setup linux">
  <link rel="canonical" href="{BASE}/fix/proxy/{proxy_slug}/{topic_slug}/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle",
    "headline":"{proxy_name} {topic_title} Guide",
    "url":"{BASE}/fix/proxy/{proxy_slug}/{topic_slug}/",
    "description":"{desc}",
    "author":{{"@type":"Organization","name":"MetricLogic"}},
    "datePublished":"{TODAY}"}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"{BASE}"}},
    {{"@type":"ListItem","position":2,"name":"Fix Guides","item":"{BASE}/fix/"}},
    {{"@type":"ListItem","position":3,"name":"Proxy Fix Guides","item":"{BASE}/fix/proxy/"}},
    {{"@type":"ListItem","position":4,"name":"{proxy_name} {topic_title}","item":"{BASE}/fix/proxy/{proxy_slug}/{topic_slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/proxy/">Proxy</a> › {proxy_name} {topic_title}
  </div>
  <div class="content">
    <h1>{proxy_name} {topic_title} — Fix Guide</h1>
    <p>{desc}</p>
    <div class="cta">
      <p>Paste your {proxy_name} config or docker-compose labels to detect misconfigurations and get the exact fix.</p>
      <a href="/proxy/">Open Reverse Proxy Mapper →</a>
    </div>
    <h2>Related Guides</h2>
    <ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
      <li><a href="/fix/proxy/traefik-v2-to-v3/">Traefik v2 to v3 migration fix</a></li>
      <li><a href="/fix/proxy/dangling-routes/">Dangling route 502 fix</a></li>
      <li><a href="/fix/proxy/missing-ssl-redirect/">Missing SSL redirect fix</a></li>
      <li><a href="/fix/proxy/cors-double-header/">Duplicate CORS headers fix</a></li>
      <li><a href="/glossary/reverse-proxy/">What is a reverse proxy?</a></li>
    </ul>
  </div>
{FOOTER}
</body>
</html>"""

# ── 4 ERROR PAGES ─────────────────────────────────────────────────────────────

PROXY_ERRORS = [
    {
        "slug": "traefik-gateway-timeout",
        "title": "Fix: Traefik Gateway Timeout (504)",
        "meta_desc": "Traefik 504 Gateway Timeout — backend took too long to respond. How to increase Traefik response timeouts and diagnose slow upstream services.",
        "keywords": "traefik 504 gateway timeout, traefik response timeout, traefik timeout fix",
        "cause": "Traefik's default response timeout is 60 seconds. Backend services that take longer — slow database queries, large file processing, AI inference — hit this limit and return 504.",
        "fix": """<div class="fix-box">
  <div class="label">Increase Traefik timeout in static config (traefik.yml)</div>
  <pre>serversTransport:
  respondingTimeouts:
    readTimeout: 300s    # 5 minutes — adjust to your needs
    writeTimeout: 300s
    idleTimeout: 300s</pre>
</div>
<div class="fix-box">
  <div class="label">Or per-router in docker-compose labels</div>
  <pre>traefik.http.routers.myapp.middlewares=timeout@docker
traefik.http.middlewares.timeout.forwardauth.tls.insecureSkipVerify=false</pre>
</div>""",
        "faqs": [
            ("What is Traefik's default response timeout?", "Traefik's default readTimeout is 60 seconds. For services that need longer — AI model inference, video processing, large exports — increase it in the serversTransport section of your static traefik.yml config."),
            ("How do I diagnose if the timeout is in Traefik or the backend?", "Check Traefik's access log for the duration field. If requests are being cut off at exactly 60 seconds, the timeout is in Traefik. If they vary, the backend is genuinely slow."),
        ],
    },
    {
        "slug": "nginx-413-request-too-large",
        "title": "Fix: Nginx 413 Request Entity Too Large",
        "meta_desc": "Nginx returns 413 when uploads exceed client_max_body_size. How to increase the upload limit in Nginx for file uploads, APIs, and reverse proxy configurations.",
        "keywords": "nginx 413 request entity too large, nginx upload size limit, client_max_body_size nginx fix",
        "cause": "Nginx's default <code>client_max_body_size</code> is 1MB. File uploads, API payloads, and image uploads larger than 1MB get rejected with 413.",
        "fix": """<div class="fix-box">
  <div class="label">Increase client_max_body_size in your server block</div>
  <pre>server {
    listen 443 ssl;
    server_name yourdomain.com;

    # Increase to 50MB for file uploads:
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}</pre>
</div>
<p>Set it in the <code>location</code> block for a specific endpoint, in the <code>server</code> block for the whole site, or in <code>http {}</code> in nginx.conf for all sites.</p>
<pre>nginx -t && systemctl reload nginx</pre>""",
        "faqs": [
            ("What is Nginx's default upload size limit?", "Nginx's default client_max_body_size is 1MB (1m). Any request body larger than this is rejected with 413. Set it to 0 to disable the limit entirely, though this is not recommended on public-facing servers."),
            ("Does client_max_body_size affect JSON API requests?", "Yes. Large JSON payloads — bulk API requests, batch data imports — are also subject to client_max_body_size. If your API returns 413 on large POST requests, increase this value in the relevant location or server block."),
        ],
    },
    {
        "slug": "traefik-no-route-found",
        "title": "Fix: Traefik 'No Route Found' 404 Error",
        "meta_desc": "Traefik returns 404 no route found when container labels are wrong, the container is not on Traefik's network, or traefik.enable=true is missing.",
        "keywords": "traefik no route found, traefik 404 fix, traefik container not found, traefik labels not working",
        "cause": "Traefik returns 404 with 'no route found' when it has no router matching the requested hostname. This means either the container labels are wrong, the container is not on the same Docker network as Traefik, or <code>traefik.enable=true</code> is missing.",
        "fix": """<h2>Checklist — in order</h2>
<div class="fix-box">
  <div class="label">1. Check traefik.enable=true is set</div>
  <pre>labels:
  - "traefik.enable=true"   # Required — Traefik ignores containers without this</pre>
</div>
<div class="fix-box">
  <div class="label">2. Check the Host rule exactly matches your domain</div>
  <pre># Backticks required around the domain:
- "traefik.http.routers.myapp.rule=Host(`app.example.com`)"
# NOT: Host("app.example.com") — wrong quotes, won't match</pre>
</div>
<div class="fix-box">
  <div class="label">3. Check the container is on Traefik's network</div>
  <pre>services:
  myapp:
    networks:
      - traefik-public    # Must be on same network as Traefik
    labels:
      - "traefik.docker.network=traefik-public"

networks:
  traefik-public:
    external: true</pre>
</div>""",
        "faqs": [
            ("Why does Traefik show the router in the dashboard but still return 404?", "A router visible in the dashboard but returning 404 usually means the service has no healthy backends. The container is stopped, on the wrong network, or the port label is wrong. Check traefik.http.services.NAME.loadbalancer.server.port matches your container's actual listening port."),
            ("Does Traefik auto-detect containers without traefik.enable?", "Only if you set exposedByDefault: true in Traefik's Docker provider config. The recommended default is exposedByDefault: false, which requires explicit traefik.enable=true on every container you want proxied."),
        ],
    },
    {
        "slug": "caddy-tls-handshake-failed",
        "title": "Fix: Caddy TLS Handshake Failed Error",
        "meta_desc": "Caddy TLS handshake failures — certificate not issued, DNS not propagated, port 80 blocked. How to diagnose and fix Caddy automatic HTTPS failures.",
        "keywords": "caddy tls handshake failed, caddy https not working, caddy certificate error, caddy acme challenge failed",
        "cause": "Caddy uses automatic HTTPS via Let's Encrypt. TLS handshake failures occur when the ACME challenge fails — usually because port 80 is blocked by a firewall, DNS hasn't propagated, or the domain doesn't point to the server.",
        "fix": """<div class="fix-box">
  <div class="label">1. Verify port 80 is open (required for ACME HTTP-01 challenge)</div>
  <pre>sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload</pre>
</div>
<div class="fix-box">
  <div class="label">2. Verify DNS points to your server</div>
  <pre>dig +short yourdomain.com
# Should return your server's IP</pre>
</div>
<div class="fix-box">
  <div class="label">3. Check Caddy logs for the specific ACME error</div>
  <pre>journalctl -u caddy --since "1 hour ago" | grep -i "tls|acme|cert|error"</pre>
</div>
<div class="fix-box">
  <div class="label">4. Force certificate re-issue (clear Caddy's cert cache)</div>
  <pre>sudo systemctl stop caddy
sudo rm -rf /var/lib/caddy/.local/share/caddy/certificates/
sudo systemctl start caddy</pre>
</div>""",
        "faqs": [
            ("Why does Caddy fail to get a certificate even with port 80 open?", "Common causes: (1) DNS hasn't propagated yet — wait 5–10 minutes after pointing DNS to the server, (2) a UFW rule allows port 80 but Docker is bypassing UFW, (3) Caddy is rate-limited by Let's Encrypt — check caddy logs for rate limit errors."),
            ("Can I use Caddy with Cloudflare proxy enabled?", "Yes, but you need to use Caddy's DNS-01 ACME challenge instead of HTTP-01. With Cloudflare proxying enabled, Caddy can't complete HTTP-01 challenges. Install the Caddy Cloudflare DNS module and configure DNS challenge with your Cloudflare API token."),
        ],
    },
]

def build_proxy_error_page(p):
    faq_schema = ",\n".join([
        f'{{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}'
        for q, a in p["faqs"]
    ])
    faq_html = "\n".join([
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q, a in p["faqs"]
    ])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{p["title"]} — ConfigClarity</title>
  <meta name="description" content="{p["meta_desc"]}">
  <meta name="keywords" content="{p["keywords"]}">
  <link rel="canonical" href="{BASE}/fix/proxy/{p["slug"]}/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle","headline":"{p["title"]}",
    "url":"{BASE}/fix/proxy/{p["slug"]}/","description":"{p["meta_desc"]}",
    "author":{{"@type":"Organization","name":"MetricLogic"}}}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"{BASE}"}},
    {{"@type":"ListItem","position":2,"name":"Fix Guides","item":"{BASE}/fix/"}},
    {{"@type":"ListItem","position":3,"name":"Proxy Fix Guides","item":"{BASE}/fix/proxy/"}},
    {{"@type":"ListItem","position":4,"name":"{p["title"]}","item":"{BASE}/fix/proxy/{p["slug"]}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/proxy/">Proxy</a> › {p["title"]}
  </div>
  <div class="content">
    <h1>{p["title"]}</h1>
    <h2>The Cause</h2>
    <p>{p["cause"]}</p>
    <h2>The Fix</h2>
    {p["fix"]}
    <div class="cta"><p>Paste your config to detect proxy misconfigurations and get exact fixes.</p><a href="/proxy/">Open Reverse Proxy Mapper →</a></div>
    <h2>Frequently Asked Questions</h2>
    {faq_html}
  </div>
{FOOTER}
</body>
</html>"""

def build_proxy_fix_index():
    all_links = (
        [(p["slug"], p["title"]) for p in PROXY_FIX_PAGES] +
        [(p["slug"], p["title"]) for p in PROXY_ERRORS] +
        [(f"{ps}/{ts}", f"{pn} {tt}") for ps, pn in PROXY_STACKS for ts, tt, _ in PROXY_TOPICS]
    )
    cards = "\n".join([
        f'    <a href="/fix/proxy/{slug}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1rem 1.25rem;font-size:0.82rem;color:var(--text);margin-bottom:0.5rem;">{title}</a>'
        for slug, title in all_links
    ])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Reverse Proxy Fix Guides — Nginx, Traefik, Caddy — ConfigClarity</title>
  <meta name="description" content="Fix guides for Nginx, Traefik, Caddy, and Nginx Proxy Manager — dangling routes, SSL redirect, CORS headers, gateway timeouts, and Traefik v2 to v3 migration.">
  <link rel="canonical" href="{BASE}/fix/proxy/">
  {FONT}
{CSS}
</head>
<body>
{HEADER}
  <div style="max-width:760px;margin:0 auto;padding:2rem;">
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:1.5rem;"><a href="/" style="color:var(--muted);">ConfigClarity</a> › <a href="/fix/" style="color:var(--muted);">Fix Guides</a> › Reverse Proxy</div>
    <h1 style="font-size:1.6rem;font-weight:700;margin-bottom:1rem;">Reverse Proxy Fix Guides</h1>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:2rem;">Fix guides for Nginx, Traefik, Caddy, and Nginx Proxy Manager. Dangling routes, SSL redirects, CORS headers, gateway timeouts, and migration guides.</p>
{cards}
  </div>
{FOOTER}
</body>
</html>"""


if __name__ == '__main__':
    print("=== Building Proxy Mapper SEO Pages ===\n")
    os.makedirs("fix/proxy", exist_ok=True)
    count = 0

    # Index
    with open("fix/proxy/index.html", "w") as f:
        f.write(build_proxy_fix_index())
    print("  ✅ fix/proxy/index.html")
    count += 1

    # 4 fix pages
    for p in PROXY_FIX_PAGES:
        os.makedirs(f"fix/proxy/{p['slug']}", exist_ok=True)
        with open(f"fix/proxy/{p['slug']}/index.html", "w") as f:
            f.write(fix_page(
                p["slug"], p["title"], p["meta_desc"], p["keywords"],
                p["intro"], p["sections"], p["faqs"],
                p["cta_text"], p["cta_href"],
                p["breadcrumb_label"], p["breadcrumb_parent"], p["breadcrumb_parent_href"]
            ))
        print(f"  ✅ fix/proxy/{p['slug']}/index.html")
        count += 1

    # 8 stack/topic combo pages
    for ps, pn in PROXY_STACKS:
        for ts, tt, td in PROXY_TOPICS:
            path = f"fix/proxy/{ps}/{ts}"
            os.makedirs(path, exist_ok=True)
            with open(f"{path}/index.html", "w") as f:
                f.write(build_proxy_stack_page(ps, pn, ts, tt, td))
            print(f"  ✅ {path}/index.html")
            count += 1

    # 4 error pages
    for p in PROXY_ERRORS:
        os.makedirs(f"fix/proxy/{p['slug']}", exist_ok=True)
        with open(f"fix/proxy/{p['slug']}/index.html", "w") as f:
            f.write(build_proxy_error_page(p))
        print(f"  ✅ fix/proxy/{p['slug']}/index.html")
        count += 1

    print(f"\nProxy pages built: {count}")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)

    new_rewrites = []
    all_slugs = (
        ["traefik-v2-to-v3", "dangling-routes", "missing-ssl-redirect", "cors-double-header"] +
        [e["slug"] for e in PROXY_ERRORS]
    )
    stack_paths = [f"{ps}/{ts}" for ps, _ in PROXY_STACKS for ts, _, _ in PROXY_TOPICS]

    new_rewrites.append({"source": "/fix/proxy/", "destination": "/fix/proxy/index.html"})
    new_rewrites.append({"source": "/fix/proxy", "destination": "/fix/proxy/index.html"})
    for s in all_slugs:
        new_rewrites.append({"source": f"/fix/proxy/{s}/", "destination": f"/fix/proxy/{s}/index.html"})
        new_rewrites.append({"source": f"/fix/proxy/{s}", "destination": f"/fix/proxy/{s}/index.html"})
    for sp in stack_paths:
        new_rewrites.append({"source": f"/fix/proxy/{sp}/", "destination": f"/fix/proxy/{sp}/index.html"})
        new_rewrites.append({"source": f"/fix/proxy/{sp}", "destination": f"/fix/proxy/{sp}/index.html"})

    added = sum(1 for r in new_rewrites if r not in config["rewrites"])
    for r in new_rewrites:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)

    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"\n  ✅ vercel.json — {added} proxy rewrites added")

    # Update sitemap
    new_urls = (
        ["/fix/proxy/"] +
        [f"/fix/proxy/{s}/" for s in all_slugs] +
        [f"/fix/proxy/{sp}/" for sp in stack_paths]
    )
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    entries = "\n".join([
        f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        for u in new_urls if u not in sitemap
    ])
    if entries:
        sitemap = sitemap.replace("</urlset>", entries + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
    print(f"  ✅ sitemap-seo.xml — {len(new_urls)} proxy URLs added")

    print(f"\nDone. {count} proxy pages total.")
