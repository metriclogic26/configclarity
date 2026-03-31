#!/usr/bin/env python3
"""
Script 22: Build certbot timer systemd blog post.
Targets: "ubuntu 22.04 certbot.timer systemd" and related queries.
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
<p>On Ubuntu 22.04, certbot uses a systemd timer instead of a cron job for automatic certificate renewal. This is the right way to do it — systemd timers are more reliable than cron for this use case. But if you're used to seeing a cron entry for certbot and it's not there, you might wonder whether renewal is actually working.</p>

<p>Here's how to verify it, fix it if it's broken, and understand what's happening.</p>

<h2>Check if the certbot timer is active</h2>

<pre>sudo systemctl status certbot.timer</pre>

<p>You want to see <code>Active: active (waiting)</code>. If you see <code>inactive (dead)</code> or <code>failed</code> — your certificates are not auto-renewing.</p>

<p>The full output should look something like this:</p>

<pre>● certbot.timer - Run certbot twice daily
     Loaded: loaded (/lib/systemd/system/certbot.timer; enabled; vendor preset: enabled)
     Active: active (waiting) since Mon 2026-03-23 09:00:00 UTC; 6 days ago
    Trigger: Thu 2026-03-30 09:52:00 UTC; 3h 41min left
   Triggers: ● certbot.service</pre>

<p>The <code>Trigger:</code> line shows when it will next run. If this is missing or shows a date in the past — the timer has stopped.</p>

<h2>Check when certbot last ran</h2>

<pre>sudo systemctl status certbot.service</pre>

<p>This shows the last execution of the renewal service itself. Look for <code>ExecStart</code> timestamp and whether it exited successfully.</p>

<pre># Also check the certbot log directly:
sudo journalctl -u certbot.service --since "30 days ago" | tail -30</pre>

<p>You want to see renewal attempts and either <code>no renewal was necessary</code> (cert not expiring soon) or <code>Congratulations, all renewals succeeded</code>.</p>

<h2>Fix: timer exists but is not enabled</h2>

<pre>sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
sudo systemctl status certbot.timer</pre>

<h2>Fix: timer is missing entirely</h2>

<p>If <code>systemctl status certbot.timer</code> returns <code>Unit certbot.timer could not be found</code> — certbot was installed without the systemd timer, or it was installed via pip instead of apt.</p>

<pre># Check how certbot is installed:
which certbot
certbot --version

# If installed via snap (recommended on Ubuntu 22.04):
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# The snap version includes the timer automatically:
sudo systemctl status snap.certbot.renew.timer</pre>

<div class="callout">
  <p><strong>Ubuntu 22.04 note:</strong> The recommended certbot installation method is via snap, not apt. The snap version uses <code>snap.certbot.renew.timer</code> instead of <code>certbot.timer</code>. Check both if you are unsure which you have installed.</p>
</div>

<h2>Test renewal without actually renewing</h2>

<pre>sudo certbot renew --dry-run</pre>

<p>This simulates the renewal process without touching your certificates. It will catch the most common failure modes — port 80 blocked, DNS not pointing to the server, nginx ACME challenge misconfiguration. Run this monthly as a sanity check.</p>

<div class="callout danger">
  <p><strong>If dry-run fails:</strong> your certificates are not auto-renewing even if the timer shows as active. Fix the underlying issue before your next expiry date.</p>
</div>

<h2>Common failure: port 80 blocked</h2>

<p>Let's Encrypt HTTP-01 challenges require port 80 to be accessible. If your Nginx config redirects all port 80 traffic to HTTPS before the ACME challenge location, renewal fails silently.</p>

<pre># Your Nginx port 80 block must have this BEFORE the redirect:
server {
    listen 80;
    server_name yourdomain.com;

    # ACME challenge — must come before the HTTPS redirect
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}</pre>

<h2>Common failure: certbot timer active but cert still expires</h2>

<p>The timer runs twice daily but only renews certificates within 30 days of expiry. If you want to confirm the full renewal pipeline works, force a renewal:</p>

<pre># Force renewal regardless of expiry date:
sudo certbot renew --force-renewal

# Or renew a specific domain:
sudo certbot renew --cert-name yourdomain.com --force-renewal</pre>

<p>Use this only to test. Forcing renewal unnecessarily counts against Let's Encrypt rate limits (5 renewals per domain per week).</p>

<h2>Set up a monitoring check</h2>

<p>The timer being active does not mean renewal will succeed. Add a weekly dry-run to cron as a belt-and-suspenders check:</p>

<pre># Add to crontab (crontab -e):
0 9 * * 1 certbot renew --dry-run 2>&1 | grep -E "error|failed|FAILED" | mail -s "Certbot dry-run check" you@yourdomain.com</pre>

<p>This emails you only if the dry-run finds errors — silent on success.</p>

<div class="cta">
  <p>Check SSL certificate expiry across all your domains at once — 200-day warnings, CDN detection, and chain validation.</p>
  <a href="/ssl/">Open SSL Checker →</a>
</div>

<h2>Quick reference</h2>

<pre># Check timer status:
sudo systemctl status certbot.timer
sudo systemctl status snap.certbot.renew.timer  # if using snap

# Check last renewal:
sudo systemctl status certbot.service
sudo journalctl -u certbot.service --since "7 days ago"

# Test without renewing:
sudo certbot renew --dry-run

# Enable if disabled:
sudo systemctl enable --now certbot.timer

# List all certificates and expiry:
sudo certbot certificates</pre>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/ssl/nginx-renewal/">Nginx + Certbot renewal failure fix</a></li>
  <li><a href="/fix/ssl/expiry-monitoring/">SSL expiry monitoring setup</a></li>
  <li><a href="/fix/ssl/200-day-warning/">Why monitor SSL at 200 days</a></li>
  <li><a href="/glossary/ssl-certificate-expiry/">SSL certificate expiry explained</a></li>
  <li><a href="/blog/ssl-certificate-monitoring-guide/">SSL certificate monitoring guide</a></li>
</ul>
"""

SLUG = "certbot-timer-systemd-ubuntu"
TITLE = "certbot.timer on Ubuntu 22.04: How to Check, Fix, and Verify Auto-Renewal"
META_DESC = "How to check if certbot.timer is active on Ubuntu 22.04, fix a broken systemd timer, run a dry-run test, and verify Let's Encrypt auto-renewal is working."
KEYWORDS = "certbot.timer ubuntu 22.04, certbot systemd timer, certbot auto renewal ubuntu, certbot renew dry-run, certbot timer not running"
DATE = "2026-03-30"
TAGS = ["SSL", "Let's Encrypt", "Ubuntu", "systemd"]

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
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"https://configclarity.dev/blog/"}},
    {{"@type":"ListItem","position":3,"name":"{TITLE}","item":"https://configclarity.dev/blog/{SLUG}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › certbot.timer Ubuntu 22.04</div>
  <div class="hero">
    <div class="hero-meta">
      <span>{DATE}</span> ·
      {"".join([f'<span class="hero-tag">{t}</span>' for t in TAGS])}
    </div>
    <h1>{TITLE}</h1>
    <p class="lede">The certbot.timer is active. The service shows enabled. Your certificate expired anyway. Here is how to verify the full renewal pipeline is actually working — not just that the timer exists.</p>
  </div>
  <div class="content">{BODY}</div>
{FOOTER}
</body>
</html>"""

if __name__ == "__main__":
    print("=== Building certbot timer blog post ===\n")

    # Validate JSON-LD
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', PAGE, re.DOTALL)
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
            print(f"  JSON block {i}: OK")
        except Exception as e:
            print(f"  JSON block {i}: ERROR — {e}")

    # Write page
    os.makedirs(f"blog/{SLUG}", exist_ok=True)
    with open(f"blog/{SLUG}/index.html", "w") as f:
        f.write(PAGE)
    print(f"  OK  blog/{SLUG}/index.html ({len(PAGE):,} bytes)")

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

    print(f"\nDone. Blog is now 10 posts.")
    print("\nRun:")
    print(f"  git add -A && git commit -m 'feat: certbot timer systemd ubuntu blog post' && git push origin main && npx vercel --prod --force")
    print(f"\nGSC — submit URL:")
    print(f"  https://configclarity.dev/blog/{SLUG}/")
