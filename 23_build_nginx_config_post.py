#!/usr/bin/env python3
"""
Script 23: Build nginx config tester blog post.
Targets: "nginx config tester", "nginx -t", "test nginx config", "nginx config check"
Run from: ~/Projects/CronSight/
"""

import os, json, re

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

CSS = """
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root { --bg:#0b0d14; --bg2:#1e2130; --purple:#6c63ff; --green:#22c55e; --orange:#f97316; --red:#ef4444; --text:#e2e4f0; --muted:#8a8fb5; }
      body { background:var(--bg); color:var(--text); font-family:'JetBrains Mono',monospace; min-height:100vh; line-height:1.8; }
      a { color:var(--purple); text-decoration:none; } a:hover { text-decoration:underline; }
      .header { padding:1.5rem 2rem; border-bottom:1px solid #2a2d3d; display:flex; align-items:center; gap:1rem; }
      .header-logo { font-size:1.1rem; font-weight:700; color:var(--text); }
      .header-logo span { color:var(--purple); }
      .header-nav { margin-left:auto; display:flex; gap:1rem; font-size:0.8rem; }
      .header-nav a { color:var(--muted); }
      .breadcrumb { padding:1rem 2rem 0; max-width:720px; margin:0 auto; font-size:0.78rem; color:var(--muted); }
      .breadcrumb a { color:var(--muted); }
      .hero { max-width:720px; margin:0 auto; padding:3rem 2rem 1.5rem; }
      .hero-meta { font-size:0.75rem; color:var(--muted); margin-bottom:1rem; display:flex; gap:1rem; flex-wrap:wrap; align-items:center; }
      .hero-tag { background:rgba(108,99,255,.15); color:var(--purple); padding:0.15rem 0.6rem; border-radius:4px; font-size:0.72rem; }
      h1 { font-size:1.75rem; font-weight:700; line-height:1.35; margin-bottom:1rem; }
      .lede { font-size:1rem; color:var(--muted); margin-bottom:2rem; line-height:1.75; }
      .content { max-width:720px; margin:0 auto; padding:0 2rem 4rem; }
      h2 { font-size:1.15rem; font-weight:700; margin:2.5rem 0 0.75rem; }
      h3 { font-size:0.95rem; font-weight:700; margin:1.75rem 0 0.5rem; }
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1.1rem; }
      strong { color:var(--text); }
      pre { background:#0d0f1a; border:1px solid #2a2d3d; border-radius:8px; padding:1.25rem 1.5rem; font-size:0.78rem; overflow-x:auto; margin:1rem 0 1.5rem; line-height:1.7; color:var(--text); }
      code { background:#1e2130; padding:0.1rem 0.4rem; border-radius:3px; font-size:0.82rem; color:var(--text); }
      .callout { background:var(--bg2); border-left:3px solid var(--orange); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.5rem 0; }
      .callout.good { border-color:var(--green); }
      .callout.danger { border-color:var(--red); }
      .callout p { margin-bottom:0; color:var(--text); font-size:0.875rem; }
      .cta { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.5rem; margin:2.5rem 0; text-align:center; }
      .cta p { color:var(--text); font-size:0.875rem; margin-bottom:0.75rem; }
      .cta a { display:inline-block; background:var(--purple); color:#fff; padding:0.5rem 1.25rem; border-radius:6px; font-size:0.82rem; font-weight:700; text-decoration:none; }
      footer { text-align:center; padding:2rem; font-size:0.75rem; color:var(--muted); border-top:1px solid #2a2d3d; }
    </style>
"""

HEADER = """  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a><a href="/ssl/">SSL</a><a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a><a href="/proxy/">Proxy</a><a href="/robots/">robots.txt</a>
      <a href="/blog/" style="color:var(--purple);">Blog</a>
    </nav>
  </header>"""

FOOTER = """  <footer>
    <p>Part of the <a href="https://metriclogic.dev">MetricLogic</a> network &nbsp;·&nbsp;
    <a href="/blog/">More articles</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>"""

BODY = """
<p>Every Nginx change carries the same risk: you edit the config, reload, and find out you broke something only after traffic starts hitting errors. <code>nginx -t</code> exists to catch this before it happens — but most people don't know everything it does and doesn't catch.</p>

<h2>The basics: nginx -t</h2>

<pre>sudo nginx -t</pre>

<p>This validates your entire Nginx configuration — all included files, all server blocks, all upstream definitions. If the syntax is clean you see:</p>

<pre>nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful</pre>

<p>If there's an error:</p>

<pre>nginx: [emerg] unknown directive "servr_name" in /etc/nginx/sites-enabled/mysite:3
nginx: configuration file /etc/nginx/nginx.conf test failed</pre>

<p>The error tells you the exact file and line number. Fix it there, run <code>nginx -t</code> again before reloading.</p>

<h2>Always pair nginx -t with the reload</h2>

<pre># The safe pattern — test then reload:
sudo nginx -t && sudo systemctl reload nginx

# The unsafe pattern — skip the test:
sudo systemctl reload nginx</pre>

<p>The <code>&&</code> means the reload only runs if the test passes. If <code>nginx -t</code> fails, the reload never executes and your running Nginx stays untouched. Make this muscle memory.</p>

<div class="callout good">
  <p><strong>reload vs restart:</strong> Use <code>systemctl reload nginx</code> not <code>restart</code>. Reload applies the new config without dropping existing connections. Restart kills Nginx and starts it fresh — briefly interrupts active connections.</p>
</div>

<h2>What nginx -t catches</h2>

<p>Syntax errors — missing semicolons, typos in directive names, unclosed blocks. It catches these reliably.</p>

<p>Include file errors — if a file referenced with <code>include</code> doesn't exist or has a syntax error, <code>nginx -t</code> catches it.</p>

<p>Invalid directive values — wrong argument types, out-of-range values, incompatible directive combinations.</p>

<h2>What nginx -t does NOT catch</h2>

<p>This is the part people get burned by:</p>

<p><strong>Upstream availability</strong> — <code>nginx -t</code> does not check whether upstream servers are reachable. A <code>proxy_pass http://127.0.0.1:3000</code> pointing to a stopped container passes the test fine. You only find out it's broken when requests start returning 502.</p>

<p><strong>SSL certificate validity</strong> — it checks that the certificate file exists and is readable, but not whether the certificate is expired, matches the domain, or has a valid chain.</p>

<p><strong>DNS resolution</strong> — upstream hostnames in <code>proxy_pass</code> are not resolved at test time.</p>

<p><strong>Logic errors</strong> — a valid but wrong configuration passes the test. Wrong <code>proxy_pass</code> port, missing security headers, incorrect redirect chains — all pass <code>nginx -t</code> perfectly.</p>

<h2>Test a specific config file</h2>

<pre># Test a specific config file instead of the default:
sudo nginx -t -c /path/to/nginx.conf

# Useful when testing a new config before moving it into place:
sudo nginx -t -c /tmp/new-nginx.conf</pre>

<h2>Check which config files are loaded</h2>

<pre># See the full config with all includes expanded:
sudo nginx -T

# Pipe to grep to find specific settings:
sudo nginx -T | grep -i "server_name|listen|proxy_pass"

# Check what's included:
sudo nginx -T | grep "# configuration file"</pre>

<p><code>nginx -T</code> (capital T) dumps the entire effective configuration — every include file expanded inline. Useful for auditing what Nginx is actually running versus what you think it's running.</p>

<h2>Debug mode for more detail</h2>

<pre># Run nginx in debug mode to see config parsing:
sudo nginx -t -e /dev/stderr 2>&1 | head -50</pre>

<h2>Validate before and after every change</h2>

<p>The workflow that prevents every "I just broke prod" incident:</p>

<pre># 1. Make your change
nano /etc/nginx/sites-available/mysite

# 2. Test before touching anything live
sudo nginx -t

# 3. Only reload if test passes
sudo nginx -t && sudo systemctl reload nginx

# 4. Verify the change took effect
curl -sI https://yourdomain.com | grep -E "Server|X-Frame|Strict"</pre>

<h2>Reload vs restart — when to use each</h2>

<pre># Use reload for config changes (zero downtime):
sudo systemctl reload nginx

# Use restart only when:
# - Adding new modules
# - Changing worker_processes
# - SSL certificate replacement (some versions)
sudo systemctl restart nginx</pre>

<h2>Check Nginx error logs after reload</h2>

<p>Even after a successful reload, check the error log for runtime issues that the config test couldn't catch:</p>

<pre># Watch the error log in real time after reload:
sudo tail -f /var/log/nginx/error.log

# Check for upstream errors in the last 100 lines:
sudo tail -100 /var/log/nginx/error.log | grep -E "upstream|connect|refused"</pre>

<h2>Audit your full config for common issues</h2>

<p>Beyond syntax validation, there are configuration issues <code>nginx -t</code> will never catch — dangling proxy_pass targets, missing SSL redirects, duplicate CORS headers, deprecated Traefik labels. These require a semantic audit, not just a syntax check.</p>

<div class="cta">
  <p>Paste your nginx.conf to detect dangling routes, missing SSL redirects, and CORS header issues — the things nginx -t can't catch.</p>
  <a href="/proxy/">Open Reverse Proxy Mapper →</a>
</div>

<h2>Quick reference</h2>

<pre># Test config syntax:
sudo nginx -t

# Test then reload (safe pattern):
sudo nginx -t && sudo systemctl reload nginx

# Dump full effective config:
sudo nginx -T

# Test specific config file:
sudo nginx -t -c /path/to/nginx.conf

# Check error log after reload:
sudo tail -50 /var/log/nginx/error.log</pre>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/nginx/502-bad-gateway/">Nginx 502 Bad Gateway fix</a></li>
  <li><a href="/fix/nginx/upstream-timeout/">Nginx 504 upstream timeout fix</a></li>
  <li><a href="/fix/nginx/ssl-redirect-missing/">Nginx missing SSL redirect fix</a></li>
  <li><a href="/fix/proxy/dangling-routes/">Dangling routes fix</a></li>
  <li><a href="/glossary/reverse-proxy/">What is a reverse proxy?</a></li>
</ul>
"""

SLUG = "nginx-config-test"
TITLE = "How to Test Your Nginx Config Before Reloading (nginx -t and Beyond)"
META_DESC = "nginx -t validates syntax but misses upstream errors, expired certs, and logic issues. How to test Nginx config safely, what nginx -t catches and misses, and the reload workflow that prevents outages."
KEYWORDS = "nginx config tester, nginx -t, test nginx config, nginx config check, nginx config validator, nginx -t command"
DATE = "2026-03-30"
TAGS = ["Nginx", "DevOps", "Linux", "Reverse Proxy"]

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{TITLE} — ConfigClarity</title>
  <meta name="description" content="{META_DESC}">
  <meta name="keywords" content="{KEYWORDS}">
  <link rel="canonical" href="https://configclarity.dev/blog/{SLUG}/">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{META_DESC}">
  <meta property="og:url" content="https://configclarity.dev/blog/{SLUG}/">
  <meta property="og:type" content="article">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article",
    "headline":"{TITLE}",
    "description":"{META_DESC}",
    "url":"https://configclarity.dev/blog/{SLUG}/",
    "datePublished":"{DATE}",
    "dateModified":"{DATE}",
    "author":{{"@type":"Organization","name":"MetricLogic","url":"https://metriclogic.dev"}},
    "publisher":{{"@type":"Organization","name":"ConfigClarity","url":"https://configclarity.dev"}},
    "isPartOf":{{"@type":"Blog","name":"ConfigClarity Blog","url":"https://configclarity.dev/blog/"}}
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {{"@type":"Question","name":"What does nginx -t do?","acceptedAnswer":{{"@type":"Answer","text":"nginx -t validates the syntax of your entire Nginx configuration including all included files. It catches syntax errors, unknown directives, and invalid values but does not check whether upstream servers are reachable or SSL certificates are valid."}}}},
    {{"@type":"Question","name":"What is the safe way to reload Nginx after a config change?","acceptedAnswer":{{"@type":"Answer","text":"Always test before reloading: sudo nginx -t && sudo systemctl reload nginx. The && means reload only runs if the test passes. This prevents accidentally reloading a broken config."}}}},
    {{"@type":"Question","name":"What does nginx -t not catch?","acceptedAnswer":{{"@type":"Answer","text":"nginx -t does not check upstream server availability, SSL certificate validity or expiry, DNS resolution of upstream hostnames, or logic errors like wrong proxy_pass ports. A config can pass nginx -t and still cause 502 errors at runtime."}}}}
  ]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"https://configclarity.dev/blog/"}},
    {{"@type":"ListItem","position":3,"name":"How to Test Nginx Config","item":"https://configclarity.dev/blog/{SLUG}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › Nginx Config Testing</div>
  <div class="hero">
    <div class="hero-meta">
      <span>{DATE}</span> ·
      {"".join([f'<span class="hero-tag">{t}</span>' for t in TAGS])}
    </div>
    <h1>{TITLE}</h1>
    <p class="lede">nginx -t checks syntax. It does not check whether your upstreams are alive, your SSL certs are valid, or your config actually does what you intended. Here is the full testing workflow — and what to do after the test passes.</p>
  </div>
  <div class="content">{BODY}</div>
{FOOTER}
</body>
</html>"""

if __name__ == "__main__":
    print("=== Building nginx config tester blog post ===\n")

    # Validate JSON-LD
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', PAGE, re.DOTALL)
    all_ok = True
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
            print(f"  JSON block {i}: OK")
        except Exception as e:
            print(f"  JSON block {i}: ERROR — {e}")
            all_ok = False

    if not all_ok:
        print("\nFix JSON errors before proceeding.")
        exit(1)

    # Write page
    os.makedirs(f"blog/{SLUG}", exist_ok=True)
    with open(f"blog/{SLUG}/index.html", "w") as f:
        f.write(PAGE)
    print(f"\n  OK  blog/{SLUG}/index.html ({len(PAGE):,} bytes)")

    # Update blog index
    with open("blog/index.html", "r") as f:
        content = f.read()
    if SLUG not in content:
        tag_html = "&nbsp;".join([
            f'<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">{t}</span>'
            for t in TAGS
        ])
        new_card = f"""    <a href="/blog/{SLUG}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">{DATE} &nbsp;·&nbsp; {tag_html}</div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">{TITLE}</div>
      <div style="font-size:0.82rem;color:var(--muted);">{META_DESC[:120]}...</div>
    </a>\n"""
        marker = '<h1 style="font-size:1.6rem'
        content = content.replace(marker, new_card + "    " + marker, 1)
        with open("blog/index.html", "w") as f:
            f.write(content)
        print(f"  OK  blog/index.html — post added")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)
    added = 0
    for rule in [
        {"source": f"/blog/{SLUG}/", "destination": f"/blog/{SLUG}/index.html"},
        {"source": f"/blog/{SLUG}", "destination": f"/blog/{SLUG}/index.html"},
    ]:
        if rule not in config["rewrites"]:
            config["rewrites"].append(rule)
            added += 1
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  OK  vercel.json — {added} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    url = f"/blog/{SLUG}/"
    if url not in sitemap:
        entry = f"  <url><loc>https://www.configclarity.dev{url}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        sitemap = sitemap.replace("</urlset>", entry + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
        print(f"  OK  sitemap-seo.xml — URL added")

    print(f"\nDone. Blog is now 11 posts.")
    print("\nRun:")
    print(f"  git add -A && git commit -m 'feat: nginx config test blog post' && git push origin main && npx vercel --prod --force")
    print(f"\nGSC — submit tomorrow (quota reset):")
    print(f"  https://configclarity.dev/blog/{SLUG}/")
