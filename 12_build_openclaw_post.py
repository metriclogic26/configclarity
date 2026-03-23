#!/usr/bin/env python3
"""
Script 12: Build /blog/openclaw-server-audit/ post.
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
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1.1rem; }
      strong { color:var(--text); }
      pre { background:#0d0f1a; border:1px solid #2a2d3d; border-radius:8px; padding:1.25rem 1.5rem; font-size:0.78rem; overflow-x:auto; margin:1rem 0 1.5rem; line-height:1.7; color:var(--text); }
      code { background:#1e2130; padding:0.1rem 0.4rem; border-radius:3px; font-size:0.82rem; color:var(--text); }
      .callout { background:var(--bg2); border-left:3px solid var(--orange); border-radius:0 8px 8px 0; padding:1.1rem 1.4rem; margin:1.5rem 0; }
      .callout.danger { border-color:var(--red); }
      .callout p { margin-bottom:0; color:var(--text); font-size:0.875rem; }
      .checklist { list-style:none; padding:0; margin:1rem 0 1.5rem; }
      .checklist li { font-size:0.875rem; color:var(--muted); padding:0.5rem 0; border-bottom:1px solid #1a1c26; display:flex; gap:0.75rem; align-items:flex-start; }
      .checklist li:last-child { border-bottom:none; }
      .checklist li::before { content:"→"; color:var(--purple); flex-shrink:0; }
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

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Running NemoClaw or OpenClaw Locally? Audit Your Server First. — ConfigClarity</title>
  <meta name="description" content="An always-on AI agent with access to your files and network is only as secure as the infrastructure it runs on. 5 things to check before you give NemoClaw or OpenClaw the keys.">
  <meta name="keywords" content="openclaw server security, nemoclaw local setup, ai agent docker security, openclaw server audit, nemoclaw server hardening">
  <link rel="canonical" href="https://configclarity.dev/blog/openclaw-server-audit/">
  <meta property="og:title" content="Running NemoClaw or OpenClaw Locally? Audit Your Server First.">
  <meta property="og:description" content="An always-on AI agent is only as secure as the infrastructure it runs on. 5 checks before you go live.">
  <meta property="og:url" content="https://configclarity.dev/blog/openclaw-server-audit/">
  <meta property="og:type" content="article">
  """ + FONT + """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Running NemoClaw or OpenClaw Locally? Audit Your Server First.",
    "description": "An always-on AI agent with access to your files and network is only as secure as the infrastructure it runs on. 5 things to check before you give NemoClaw or OpenClaw the keys.",
    "url": "https://configclarity.dev/blog/openclaw-server-audit/",
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
    {"@type":"ListItem","position":3,"name":"OpenClaw Server Audit","item":"https://configclarity.dev/blog/openclaw-server-audit/"}
  ]}
  </script>
""" + CSS + """
</head>
<body>
""" + HEADER + """
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › OpenClaw Server Audit</div>
  <div class="hero">
    <div class="hero-meta">
      <span>2026-03-23</span> ·
      <span class="hero-tag">AI</span>
      <span class="hero-tag">Security</span>
      <span class="hero-tag">DevOps</span>
      <span class="hero-tag">Self-hosted</span>
    </div>
    <h1>Running NemoClaw or OpenClaw Locally? Audit Your Server Before You Give an AI Agent the Keys.</h1>
    <p class="lede">An always-on AI agent with access to your files, tools, and network is only as secure as the infrastructure it runs on. Here's what to check before you go live.</p>
  </div>
  <div class="content">

    <p>NVIDIA just announced NemoClaw at GTC 2026. If you're in the OpenClaw community, you're probably already thinking about running it locally on a dedicated machine.</p>

    <p>Before you do — your server needs to be clean first. An always-on agent with access to your files, tools, and network is only as secure as the infrastructure underneath it. A misconfigured server with an AI agent on top is worse than a misconfigured server on its own.</p>

    <p>Five things to check before NemoClaw or OpenClaw goes live.</p>

    <h2>1. Your Docker ports might be publicly exposed</h2>

    <p>NemoClaw and OpenClaw both run in Docker. The most common misconfiguration in any Docker setup:</p>

    <pre>ports: "11434:11434"</pre>

    <p>That binds to <code>0.0.0.0</code> — meaning your AI agent's inference port is accessible from the public internet, not just localhost. UFW won't catch it. Docker bypasses UFW entirely by inserting rules directly into iptables FORWARD chain before UFW's INPUT rules fire.</p>

    <div class="callout danger">
      <p>Check right now from mobile data: <code>curl http://YOUR_SERVER_IP:11434</code> — if you get a response, your inference port is public.</p>
    </div>

    <pre># Before — publicly accessible:
ports:
  - "11434:11434"

# After — localhost only:
ports:
  - "127.0.0.1:11434:11434"</pre>

    <p>Check every port mapping in your compose file before NemoClaw goes live. Every service the agent can reach should be bound to <code>127.0.0.1</code> unless there's a specific reason it needs external access.</p>

    <h2>2. Your firewall has IPv4/IPv6 mismatches</h2>

    <p>You locked down IPv4. IPv6 is wide open. Same result — your agent's ports are reachable from outside.</p>

    <p>UFW manages both <code>iptables</code> (IPv4) and <code>ip6tables</code> (IPv6), but only applies rules to both when <code>IPV6=yes</code> is set in <code>/etc/default/ufw</code>. Most guides skip this step.</p>

    <pre>grep IPV6 /etc/default/ufw
# Should return: IPV6=yes

# If not set, fix it:
sudo sed -i 's/IPV6=no/IPV6=yes/' /etc/default/ufw
sudo ufw disable && sudo ufw enable</pre>

    <div class="cta">
      <p>Paste your <code>ufw status verbose</code> output to detect IPv6 mismatches, Docker bypass risk, and high-risk open ports.</p>
      <div class="cta-row">
        <a href="/firewall/">Firewall Auditor →</a>
        <a href="/docker/" class="secondary">Docker Auditor →</a>
      </div>
    </div>

    <h2>3. Your cron jobs will collide with agent tasks</h2>

    <p>Always-on agents schedule their own tasks. If you already have cron jobs running backups, updates, or maintenance — you need to know exactly when they fire.</p>

    <p>Three jobs hitting the same minute means a server load spike. Your agent task hangs. No error. No alert. You just come back to a failed inference job and a confused agent that retried four times.</p>

    <p>Visualise your full cron timeline before adding agent workloads on top of it. Stagger everything by at least 5 minutes. Wrap agent-triggered scripts with <code>flock</code> to prevent concurrent runs.</p>

    <pre># Agent task — flock to prevent concurrent runs:
*/10 * * * * flock -n /tmp/agent-task.lock /usr/local/bin/agent-task.sh</pre>

    <h2>4. Your SSL certificates need monitoring</h2>

    <p>NemoClaw and OpenClaw both run web interfaces. If you're proxying either through Nginx or Traefik with SSL — that cert will expire. Let's Encrypt certs expire every 90 days and auto-renew only if your renewal pipeline is working correctly.</p>

    <p>Set up certificate monitoring across all your domains now. The standard 30-day alert is too late — if auto-renewal broke on issuance day, you have 89 days of silent failure before a 30-day alert fires.</p>

    <h2>5. Your dependencies have CVEs you don't know about</h2>

    <p>Building on top of NemoClaw? Extending OpenClaw with custom skills? Your <code>package.json</code> or <code>requirements.txt</code> has vulnerabilities that AI assistants can't tell you about accurately — because the OSV database updates daily and AI training data is always stale.</p>

    <p>A CVE published last Tuesday against a package you pinned six months ago doesn't exist in any model's training set. Scan against live data, not cached data.</p>

    <h2>The full pre-launch checklist</h2>

    <ul class="checklist">
      <li>All Docker ports bound to <code>127.0.0.1</code>, not <code>0.0.0.0</code></li>
      <li>UFW IPv6 rules enabled — <code>IPV6=yes</code> in <code>/etc/default/ufw</code></li>
      <li>No hardcoded API keys in compose files — all in <code>.env</code> with <code>.gitignore</code></li>
      <li>Resource limits set on agent containers — CPU and memory caps</li>
      <li>Log rotation configured — <code>max-size: 10m, max-file: 3</code></li>
      <li>Cron schedule visualised — no overlaps with agent tasks</li>
      <li>SSL certs monitored — across all domains the agent's interfaces use</li>
      <li>Dependencies scanned against live CVE database</li>
    </ul>

    <div class="cta">
      <p>ConfigClarity audits Docker, firewall, cron, SSL, and reverse proxy configs. Paste your config and get exact copy-paste fixes. No signup. Nothing leaves your browser.</p>
      <div class="cta-row">
        <a href="/docker/">Docker Auditor →</a>
        <a href="/firewall/" class="secondary">Firewall Auditor →</a>
      </div>
    </div>

    <p style="margin-top:2rem;font-size:0.82rem;color:var(--muted);">Building something with NemoClaw or OpenClaw? The agent layer gets all the attention. The infrastructure layer underneath is where things quietly go wrong.</p>

  </div>
""" + FOOTER + """
</body>
</html>"""


if __name__ == "__main__":
    print("=== Building OpenClaw Blog Post ===\n")

    # Write page
    os.makedirs("blog/openclaw-server-audit", exist_ok=True)
    with open("blog/openclaw-server-audit/index.html", "w") as f:
        f.write(PAGE)
    print(f"  ✅ blog/openclaw-server-audit/index.html ({len(PAGE):,} bytes)")

    # Update blog index
    blog_index = "blog/index.html"
    if os.path.exists(blog_index):
        with open(blog_index, "r") as f:
            content = f.read()
        if "openclaw-server-audit" not in content:
            new_card = '''    <a href="/blog/openclaw-server-audit/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">2026-03-23 &nbsp;·&nbsp; <span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">AI</span>&nbsp;<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">Security</span>&nbsp;<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">Self-hosted</span></div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">Running NemoClaw or OpenClaw Locally? Audit Your Server First.</div>
      <div style="font-size:0.82rem;color:var(--muted);">An always-on AI agent is only as secure as the infrastructure it runs on. 5 checks before you go live.</div>
    </a>'''
            marker = '<h1 style="font-size:1.6rem'
            content = content.replace(marker, new_card + "\n    " + marker, 1)
            with open(blog_index, "w") as f:
                f.write(content)
            print(f"  ✅ blog/index.html — OpenClaw post added")
        else:
            print(f"  SKIP blog/index.html — already present")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)
    new_rules = [
        {"source": "/blog/openclaw-server-audit/", "destination": "/blog/openclaw-server-audit/index.html"},
        {"source": "/blog/openclaw-server-audit", "destination": "/blog/openclaw-server-audit/index.html"},
    ]
    added = sum(1 for r in new_rules if r not in config["rewrites"])
    for r in new_rules:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  ✅ vercel.json — {added} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    if "/blog/openclaw-server-audit/" not in sitemap:
        entry = "  <url><loc>https://configclarity.dev/blog/openclaw-server-audit/</loc><lastmod>2026-03-23</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        sitemap = sitemap.replace("</urlset>", entry + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
        print(f"  ✅ sitemap-seo.xml updated")

    print(f"\nDone. Blog is now 8 posts.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: openclaw server audit blog post' && git push origin main && npx vercel --prod --force")
    print("\nGSC submit:")
    print("  https://configclarity.dev/blog/openclaw-server-audit/")
