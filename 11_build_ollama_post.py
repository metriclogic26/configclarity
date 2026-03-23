#!/usr/bin/env python3
"""
Script 11: Build /blog/ollama-server-security/ from Medium article.
Run from: ~/Projects/CronSight/
"""

import os, json

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
      blockquote { border-left:3px solid var(--purple); padding:0.75rem 1.25rem; margin:1.5rem 0; background:var(--bg2); border-radius:0 6px 6px 0; }
      blockquote p { color:var(--text); font-style:italic; margin-bottom:0; }
      .callout { background:var(--bg2); border-left:3px solid var(--orange); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.5rem 0; }
      .callout.danger { border-color:var(--red); }
      .callout.good { border-color:var(--green); }
      .callout p { margin-bottom:0; color:var(--text); font-size:0.875rem; }
      .cta { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.5rem; margin:2.5rem 0; text-align:center; }
      .cta p { color:var(--text); font-size:0.875rem; margin-bottom:0.75rem; }
      .cta-row { display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap; }
      .cta a { display:inline-block; background:var(--purple); color:#fff; padding:0.5rem 1.25rem; border-radius:6px; font-size:0.82rem; font-weight:700; text-decoration:none; }
      .cta a.secondary { background:transparent; border:1px solid var(--purple); color:var(--purple); }
      footer { text-align:center; padding:2rem; font-size:0.75rem; color:var(--muted); border-top:1px solid #2a2d3d; }
      @media (max-width:600px) { h1 { font-size:1.4rem; } .hero, .content { padding-left:1.25rem; padding-right:1.25rem; } }
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

OLLAMA_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ollama Exposes Your Server by Default. Here's the Proof. — ConfigClarity</title>
  <meta name="description" content="Ollama binds to 0.0.0.0 by default. UFW won't protect you because Docker bypasses the INPUT chain. How to lock down your Ollama server in 10 minutes.">
  <meta name="keywords" content="ollama server security, ollama ufw bypass, ollama docker exposed, ollama 11434 public, secure ollama server linux">
  <link rel="canonical" href="https://configclarity.dev/blog/ollama-server-security/">
  <meta property="og:title" content="Ollama Exposes Your Server by Default. Here's the Proof.">
  <meta property="og:description" content="UFW is active. Port 11434 shows blocked. Your Ollama is still open to the internet. Here's why — and how to fix it.">
  <meta property="og:url" content="https://configclarity.dev/blog/ollama-server-security/">
  <meta property="og:type" content="article">
  """ + FONT + """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Ollama Exposes Your Server by Default. Here's the Proof.",
    "description": "Ollama binds to 0.0.0.0 by default. UFW won't protect you because Docker bypasses the INPUT chain. How to lock down your Ollama server in 10 minutes.",
    "url": "https://configclarity.dev/blog/ollama-server-security/",
    "datePublished": "2026-03-23",
    "dateModified": "2026-03-23",
    "author": {"@type": "Organization", "name": "MetricLogic", "url": "https://metriclogic.dev"},
    "publisher": {"@type": "Organization", "name": "ConfigClarity", "url": "https://configclarity.dev"},
    "isPartOf": {"@type": "Blog", "name": "ConfigClarity Blog", "url": "https://configclarity.dev/blog/"}
  }
  </script>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"},
    {"@type":"ListItem","position":2,"name":"Blog","item":"https://configclarity.dev/blog/"},
    {"@type":"ListItem","position":3,"name":"Ollama Server Security","item":"https://configclarity.dev/blog/ollama-server-security/"}
  ]}
  </script>
""" + CSS + """
</head>
<body>
""" + HEADER + """
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › Ollama Server Security</div>
  <div class="hero">
    <div class="hero-meta">
      <span>2026-03-23</span> · 
      <span class="hero-tag">Ollama</span>
      <span class="hero-tag">Security</span>
      <span class="hero-tag">Docker</span>
      <span class="hero-tag">Self-hosted</span>
    </div>
    <h1>Ollama Exposes Your Server by Default. Here's the Proof.</h1>
    <p class="lede">Turn off your Wi-Fi. Switch to mobile data. Run <code>curl http://your-server-ip:11434</code>. If you get a response — your Ollama API is publicly reachable right now. Anyone on the internet can run inference on your hardware for free.</p>
  </div>
  <div class="content">

    <p>I've seen this play out more times than I'd like. Someone sets up Ollama on their VPS or home server. They run <code>ufw status</code> and see their firewall is active. They feel good about it. They move on.</p>

    <p>Three weeks later they get an API bill that makes no sense. Or they find out their model endpoint has been running inference for strangers on the internet — burning their hardware cycles, racking up bandwidth, and potentially getting their VPS account flagged for abuse.</p>

    <p>The firewall didn't fail. They just didn't know how Docker actually works.</p>

    <blockquote><p>Infrastructure is the boring part until it's the expensive part.</p></blockquote>

    <h2>Why UFW isn't protecting you</h2>

    <p>This is the one that surprises people the most. You set UFW to deny incoming. You check <code>ufw status</code> and port 11434 shows as blocked. You feel safe.</p>

    <p>But Docker doesn't route traffic through the INPUT chain where UFW lives. It inserts its own rules into the FORWARD chain — before UFW even gets a look at the packet.</p>

    <p>Think of it like this: UFW is a security guard at the front door. Docker built a side entrance that bypasses the lobby entirely.</p>

    <p>So when your compose file has:</p>
    <pre>ports: "11434:11434"</pre>

    <p>You're binding Ollama to <code>0.0.0.0</code>. Every interface. Including your public IP. UFW is sitting there blocking the INPUT chain while Docker has already let the traffic through the FORWARD chain.</p>

    <h2>The fix — one line</h2>

    <pre># Before — exposed to internet:
ports:
  - "11434:11434"

# After — localhost only:
ports:
  - "127.0.0.1:11434:11434"</pre>

    <p>That's it. Binds to localhost only. External traffic never reaches the container.</p>

    <div class="callout">
      <p><strong>Important:</strong> don't confuse this with the <code>OLLAMA_HOST</code> environment variable. Even if you set <code>OLLAMA_HOST=127.0.0.1</code> inside the container, a standard <code>ports: "11434:11434"</code> mapping will still punch a hole through your firewall. The fix must happen in the ports block — not the environment block.</p>
    </div>

    <p>If you actually need Ollama accessible from other machines — don't expose the port directly. Put Nginx or Traefik in front with authentication. That also handles SSL.</p>

    <div class="callout danger">
      <p><strong>Red flag:</strong> if you see <code>network_mode: host</code> in a tutorial — run. It completely eliminates Docker's network sandbox and exposes every port directly on the host interface, bypassing every security layer we just discussed.</p>
    </div>

    <h2>The CORS wildcard that opens a second door</h2>

    <p>To get their web UI working, a lot of people set this in their compose file:</p>
    <pre>environment:
  - OLLAMA_ORIGINS=*</pre>

    <p>That wildcard means any website — including a malicious one — can send requests to your Ollama instance directly through your browser when you visit it. Set specific origins instead:</p>

    <pre>environment:
  - OLLAMA_ORIGINS=https://your-webui-domain.com</pre>

    <h2>Your compose file might be leaking API keys</h2>

    <p>If you're connecting Ollama to any external service — OpenRouter, a custom API, anything — check your compose file for this pattern:</p>
    <pre>environment:
  - OPENROUTER_KEY=sk-abc123</pre>

    <p>That key is in plain text. If your repo is public or if you've ever pushed it anywhere, that key has been exposed. Move it to a .env file:</p>

    <pre>environment:
  - OPENROUTER_KEY=${OPENROUTER_KEY}</pre>

    <pre>echo ".env" >> .gitignore</pre>

    <div class="cta">
      <p>Paste your docker-compose.yml to detect exposed ports, hardcoded secrets, missing healthchecks, and resource limits — with exact copy-paste fixes.</p>
      <div class="cta-row">
        <a href="/docker/">Docker Auditor →</a>
        <a href="/firewall/" class="secondary">Firewall Auditor →</a>
      </div>
    </div>

    <h2>Your cron jobs will collide with model pulls</h2>

    <p>If you have automated model pulls running on a schedule — and you should — they need to coexist with everything else on that server. Backup jobs. Log rotation. System updates. Three jobs firing at the same minute causes a load spike. Your model pull hangs. No error. No alert. You just come back to a half-pulled model and a confused container.</p>

    <p>Visualise your full cron schedule and check for overlaps before you add model management tasks on top of it.</p>

    <h2>That SSL cert on your Ollama frontend will expire</h2>

    <p>If you're running Open WebUI or any other Ollama frontend behind Nginx or Traefik — that TLS certificate has an expiry date. It will expire. Usually at an inconvenient time. Set up certificate monitoring across all your domains now. Not when the browser throws a warning.</p>

    <h2>Set resource limits or Ollama will eat your server</h2>

    <p>A large model pull, a stuck inference job, or a runaway embedding task will pin your CPU at 100% and take everything else on the host down with it.</p>

    <pre>deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G</pre>

    <p>Adjust based on your hardware. The point is to set a ceiling so one stuck job can't take the whole machine down.</p>

    <h2>Set log limits or your disk will disappear</h2>

    <p>Ollama is surprisingly chatty. Running 24/7, the logs accumulate fast. Left unchecked they'll fill your disk over days or weeks until something breaks in a confusing way.</p>

    <pre>logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"</pre>

    <p>And run this occasionally to clean up dangling volumes from crashed containers:</p>
    <pre>docker system prune</pre>

    <p>Safe to run — it removes stopped containers and dangling images but won't touch your <code>~/.ollama</code> directory or Docker volumes. Your 50GB of models are not going anywhere.</p>

    <h2>The full checklist</h2>

    <pre># 1. Bind Ollama to localhost only
ports: "127.0.0.1:11434:11434"

# 2. Set specific CORS origins
OLLAMA_ORIGINS=https://your-webui-domain.com

# 3. Move API keys to .env
OPENROUTER_KEY=${OPENROUTER_KEY}

# 4. Set resource limits
deploy.resources.limits: cpus 2.0, memory 4G

# 5. Set log rotation
logging.driver: json-file, max-size 10m, max-file 3

# 6. Check for port exposure
curl http://YOUR_SERVER_IP:11434  (from mobile data)</pre>

    <div class="cta">
      <p>The Docker Auditor catches all of this automatically. Paste your compose file — exposed ports, hardcoded secrets, missing limits, missing healthchecks — flagged in one pass.</p>
      <div class="cta-row">
        <a href="/docker/">Open Docker Auditor →</a>
        <a href="/firewall/" class="secondary">Firewall Auditor →</a>
      </div>
    </div>

    <p style="margin-top:2rem;font-size:0.82rem;color:var(--muted);">The model layer gets all the attention. The infrastructure layer underneath is where things quietly go wrong. Go run that curl command. Off Wi-Fi. Right now.</p>

  </div>
""" + FOOTER + """
</body>
</html>"""


if __name__ == "__main__":
    print("=== Building Ollama Blog Post ===\n")

    # Write page
    os.makedirs("blog/ollama-server-security", exist_ok=True)
    with open("blog/ollama-server-security/index.html", "w") as f:
        f.write(OLLAMA_PAGE)
    print(f"  ✅ blog/ollama-server-security/index.html ({len(OLLAMA_PAGE):,} bytes)")

    # Update blog index to add this post if not already there
    blog_index = "blog/index.html"
    if os.path.exists(blog_index):
        with open(blog_index, "r") as f:
            content = f.read()
        if "ollama-server-security" not in content:
            # Insert card before the first existing card
            new_card = '''    <a href="/blog/ollama-server-security/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">2026-03-23 &nbsp;·&nbsp; <span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">Ollama</span>&nbsp;<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">Security</span>&nbsp;<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">Docker</span></div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">Ollama Exposes Your Server by Default. Here&#39;s the Proof.</div>
      <div style="font-size:0.82rem;color:var(--muted);">UFW is active. Port 11434 shows blocked. Your Ollama is still open. Here&#39;s why — and the one-line fix.</div>
    </a>'''
            # Insert after the <div style="max-width... opening
            marker = '<h1 style="font-size:1.6rem'
            content = content.replace(marker, new_card + "\n    " + marker, 1)
            with open(blog_index, "w") as f:
                f.write(content)
            print(f"  ✅ blog/index.html — Ollama post added to index")
        else:
            print(f"  SKIP blog/index.html — already contains ollama post")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)
    new_rules = [
        {"source": "/blog/ollama-server-security/", "destination": "/blog/ollama-server-security/index.html"},
        {"source": "/blog/ollama-server-security", "destination": "/blog/ollama-server-security/index.html"},
    ]
    added = 0
    for r in new_rules:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)
            added += 1
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  ✅ vercel.json — {added} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    if "/blog/ollama-server-security/" not in sitemap:
        entry = "  <url><loc>https://configclarity.dev/blog/ollama-server-security/</loc><lastmod>2026-03-23</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        sitemap = sitemap.replace("</urlset>", entry + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
        print(f"  ✅ sitemap-seo.xml — ollama post added")

    print(f"\nDone.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: ollama server security blog post' && git push origin main && npx vercel --prod --force")
    print("\nGSC submit:")
    print("  https://configclarity.dev/blog/ollama-server-security/")
