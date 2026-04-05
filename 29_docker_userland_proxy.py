#!/usr/bin/env python3
"""
Script 29: Build /fix/docker/userland-proxy/ fix page.
Targets: "docker userland-proxy", "docker ufw published ports bypass"
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
      h2 { font-size:1.15rem; font-weight:700; margin:2.5rem 0 0.75rem; color:var(--text); }
      h3 { font-size:0.95rem; font-weight:700; margin:1.75rem 0 0.5rem; color:var(--text); }
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1.1rem; line-height:1.8; }
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
      .cta a.sec { background:transparent; border:1px solid var(--purple); color:var(--purple); margin-left:0.5rem; }
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
<p>Docker's userland proxy is a Go process that Docker starts for each published port on your server. When you run <code>ports: "8080:80"</code> in docker-compose.yml, Docker starts a <code>docker-proxy</code> process listening on host port 8080 that forwards traffic to the container's port 80.</p>

<p>This proxy is part of why UFW rules don't protect Docker container ports — and disabling it changes how Docker handles port forwarding in ways that matter for security.</p>

<h2>What the userland proxy actually does</h2>

<p>Without the userland proxy, Docker uses kernel-level NAT rules (iptables DNAT) to forward traffic from published ports to container ports. The userland proxy is a fallback for cases where kernel NAT isn't available or working correctly.</p>

<pre># See the userland proxy processes running:
ps aux | grep docker-proxy

# You'll see something like:
# /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 8080 -container-ip 172.17.0.2 -container-port 80</pre>

<p>One <code>docker-proxy</code> process per published port. On a busy server with many containers, this adds up to significant memory overhead — each proxy process uses ~5-10MB of RAM.</p>

<h2>How it relates to the UFW bypass</h2>

<p>The UFW bypass happens whether or not the userland proxy is enabled. The root cause is that Docker inserts iptables rules into the FORWARD chain, which UFW doesn't manage. Disabling the userland proxy doesn't fix the UFW bypass — it just changes which kernel mechanism Docker uses to forward traffic.</p>

<div class="callout">
  <p><strong>Common misconception:</strong> disabling <code>userland-proxy</code> does not make Docker respect UFW rules. The iptables FORWARD chain bypass happens at the kernel level regardless of whether the userland proxy is running.</p>
</div>

<h2>Disabling the userland proxy</h2>

<p>Some sysadmins disable the userland proxy to reduce memory usage and rely purely on kernel NAT. This is safe if your kernel supports the required iptables rules:</p>

<pre># /etc/docker/daemon.json:
{
  "userland-proxy": false
}

sudo systemctl restart docker</pre>

<div class="callout danger">
  <p><strong>Before disabling:</strong> test that your containers still receive traffic after the restart. Some network configurations (IPv6, certain VPN setups) require the userland proxy. If containers stop receiving traffic after disabling, re-enable it.</p>
</div>

<h2>Verifying the change</h2>

<pre># After restarting Docker with userland-proxy disabled:
ps aux | grep docker-proxy
# Should show no docker-proxy processes

# Verify containers still receive traffic:
curl http://localhost:YOUR_PORT/

# Check Docker is using iptables DNAT instead:
sudo iptables -t nat -L DOCKER --line-numbers</pre>

<h2>The actual fix for Docker UFW bypass</h2>

<p>Disabling the userland proxy doesn't solve the UFW bypass. The correct fix is to bind container ports to <code>127.0.0.1</code> so they're only accessible locally:</p>

<pre># In docker-compose.yml — bind to localhost only:
services:
  myapp:
    ports:
      - "127.0.0.1:8080:80"  # Not accessible from internet
      # NOT: "8080:80"        # This binds to 0.0.0.0 — bypasses UFW</pre>

<p>With <code>127.0.0.1</code> binding, Docker's iptables rules only create DNAT entries for loopback traffic. External traffic from the internet can't reach the container port at all — not through UFW, not through iptables, not through the userland proxy.</p>

<h2>Quick reference</h2>

<pre># Check if userland proxy is enabled:
docker info | grep "Userland Proxy"

# See running proxy processes:
ps aux | grep docker-proxy

# Disable in daemon.json:
# { "userland-proxy": false }

# The real UFW fix — bind to localhost:
# ports: "127.0.0.1:HOST_PORT:CONTAINER_PORT"</pre>

<div class="cta">
  <p>Audit your UFW rules and Docker port bindings for bypass risk and missing default-deny.</p>
  <a href="/firewall/">Open Firewall Auditor →</a>
  <a href="/docker/" class="sec">Docker Auditor →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/ufw/docker-bypass/">Docker UFW bypass fix guide</a></li>
  <li><a href="/blog/ufw-nftables-backend-ubuntu/">UFW and nftables on Ubuntu 22.04</a></li>
  <li><a href="/fix/nftables/docker-conflict/">nftables and Docker conflict</a></li>
  <li><a href="/glossary/docker-ufw-bypass/">Docker UFW bypass explained</a></li>
  <li><a href="/blog/docker-ufw-bypass-explained/">Docker bypasses UFW — the full story</a></li>
</ul>
"""

SLUG = "userland-proxy"
PATH = "fix/docker/userland-proxy"
URL = "/fix/docker/userland-proxy/"
TITLE = "Fix: Docker userland-proxy — What It Is and How It Affects UFW"
META_DESC = "Docker's userland-proxy starts a docker-proxy process for each published port. How it works, how it relates to the UFW bypass problem, and whether disabling it helps."
KEYWORDS = "docker userland-proxy, docker-proxy process, docker ufw bypass userland proxy, disable docker userland proxy, docker published ports bypass ufw"
DATE = "2026-04-02"
TAGS = ["Docker", "UFW", "Networking", "Linux"]
LEDE = "Every Docker published port spawns a docker-proxy process on your server. Most people never notice it. But when you're trying to understand why UFW rules don't protect your containers, the userland proxy is part of the story."

FAQS = [
    ("What is Docker's userland proxy?",
     "The userland proxy is a Go process (docker-proxy) that Docker starts for each published container port. It listens on the host port and forwards traffic to the container. It's a fallback for cases where kernel-level NAT (iptables DNAT) isn't available."),
    ("Does disabling the userland proxy fix the Docker UFW bypass?",
     "No. The Docker UFW bypass happens because Docker inserts rules into the iptables FORWARD chain, which UFW doesn't manage. This bypass occurs whether or not the userland proxy is enabled. The correct fix is to bind container ports to 127.0.0.1 in docker-compose.yml."),
    ("How do I disable the Docker userland proxy?",
     "Add to /etc/docker/daemon.json: { \"userland-proxy\": false } then restart Docker with sudo systemctl restart docker. Test that containers still receive traffic before relying on this in production — some network configurations require the userland proxy."),
]


def make_faq_schema(faqs):
    items = ",\n".join([
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faqs
    ])
    return f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}'


if __name__ == "__main__":
    tag_html = "".join([f'<span class="hero-tag">{t}</span>' for t in TAGS])
    faq_schema = make_faq_schema(FAQS)
    canonical = f"https://configclarity.dev{URL}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{TITLE} — ConfigClarity</title>
  <meta name="description" content="{META_DESC}">
  <meta name="keywords" content="{KEYWORDS}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{META_DESC}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="article">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle","headline":"{TITLE}","description":"{META_DESC}","url":"{canonical}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"MetricLogic"}}}}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Fix Guides","item":"https://configclarity.dev/fix/"}},
    {{"@type":"ListItem","position":3,"name":"Docker","item":"https://configclarity.dev/fix/docker/"}},
    {{"@type":"ListItem","position":4,"name":"userland-proxy","item":"{canonical}"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/docker/">Docker</a> › userland-proxy</div>
  <div class="hero">
    <div class="hero-meta"><span>{DATE}</span> · {tag_html}</div>
    <h1>{TITLE}</h1>
    <p class="lede">{LEDE}</p>
  </div>
  <div class="content">{BODY}</div>
{FOOTER}
</body>
</html>"""

    # Validate JSON-LD
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    all_ok = True
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
            print(f"  JSON block {i}: OK")
        except Exception as e:
            print(f"  JSON block {i}: ERROR — {e}")
            all_ok = False

    if not all_ok:
        print("Fix JSON errors before proceeding.")
        exit(1)

    # Write file
    os.makedirs(PATH, exist_ok=True)
    with open(f"{PATH}/index.html", "w") as f:
        f.write(html)
    print(f"  OK  {PATH}/index.html ({len(html):,} bytes)")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)
    added = 0
    for rule in [
        {"source": URL, "destination": f"{PATH}/index.html"},
        {"source": URL.rstrip("/"), "destination": f"{PATH}/index.html"},
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
    if URL not in sitemap:
        entry = f"  <url><loc>https://www.configclarity.dev{URL}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>"
        sitemap = sitemap.replace("</urlset>", entry + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
        print(f"  OK  sitemap-seo.xml — URL added")

    print(f"\nDone.")
    print("\nRun:")
    print(f"  git add -A && git commit -m 'feat: docker userland-proxy fix page' && git push origin main && npx vercel --prod --force")
    print(f"\nGSC submit: https://configclarity.dev{URL}")
