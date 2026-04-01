#!/usr/bin/env python3
"""
Script 24: Build Ingress NGINX retirement post + Hetzner production checklist.
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
      .header-logo { font-size:1.1rem; font-weight:700; }
      .header-logo span { color:var(--purple); }
      .header-nav { margin-left:auto; display:flex; gap:1rem; font-size:0.8rem; }
      .header-nav a { color:var(--muted); }
      .breadcrumb { padding:1rem 2rem 0; max-width:720px; margin:0 auto; font-size:0.78rem; color:var(--muted); }
      .breadcrumb a { color:var(--muted); }
      .hero { max-width:720px; margin:0 auto; padding:3rem 2rem 1.5rem; }
      .hero-meta { font-size:0.75rem; color:var(--muted); margin-bottom:1rem; display:flex; gap:1rem; flex-wrap:wrap; align-items:center; }
      .hero-tag { background:rgba(108,99,255,.15); color:var(--purple); padding:0.15rem 0.6rem; border-radius:4px; font-size:0.72rem; }
      .hero-tag.red { background:rgba(239,68,68,.15); color:var(--red); }
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
      .checklist { list-style:none; padding:0; margin:1rem 0 1.5rem; }
      .checklist li { font-size:0.875rem; color:var(--muted); padding:0.6rem 0; border-bottom:1px solid #1a1c26; display:flex; gap:0.75rem; align-items:flex-start; line-height:1.6; }
      .checklist li:last-child { border-bottom:none; }
      .checklist li::before { content:"☐"; color:var(--purple); flex-shrink:0; font-size:1rem; }
      .cta { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.5rem; margin:2.5rem 0; text-align:center; }
      .cta p { color:var(--text); font-size:0.875rem; margin-bottom:0.75rem; }
      .cta-row { display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap; }
      .cta a { display:inline-block; background:var(--purple); color:#fff; padding:0.5rem 1.25rem; border-radius:6px; font-size:0.82rem; font-weight:700; text-decoration:none; }
      .cta a.sec { background:transparent; border:1px solid var(--purple); color:var(--purple); }
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

# ── POST 1: Ingress NGINX Retirement ─────────────────────────────────────────

POST1_BODY = """
<p>Ingress NGINX — the most widely deployed Kubernetes ingress controller — was officially retired in March 2026. The Kubernetes project is no longer maintaining it. If your cluster is running Ingress NGINX, you are now running unsupported software.</p>

<p>This doesn't mean it stops working tomorrow. But it does mean no more security patches, no more bug fixes, and a hard migration deadline before it becomes a liability.</p>

<h2>What exactly was retired</h2>

<p>The <code>kubernetes/ingress-nginx</code> project — the community-maintained ingress controller based on Nginx — reached end of life. This is distinct from:</p>

<ul style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.2;">
  <li><strong>Nginx Inc's commercial Nginx Ingress Controller</strong> — still maintained, different project</li>
  <li><strong>Nginx itself</strong> — still maintained, not affected</li>
  <li><strong>Other ingress controllers</strong> (Traefik, HAProxy, Contour) — not affected</li>
</ul>

<p>If your cluster has <code>kubectl get ingressclass</code> showing <code>nginx</code> and your ingress controller pod is from <code>registry.k8s.io/ingress-nginx</code> — that's the retired one.</p>

<h2>Check if you're affected</h2>

<pre># Check your ingress controller:
kubectl get pods -n ingress-nginx
kubectl get ingressclass

# Check which image version you're running:
kubectl get pods -n ingress-nginx -o jsonpath='{.items[*].spec.containers[*].image}'</pre>

<p>If you see <code>registry.k8s.io/ingress-nginx/controller</code> — you're running the retired project.</p>

<h2>Your migration options</h2>

<h3>Option 1 — Gateway API (recommended path)</h3>

<p>The Kubernetes project's official successor to the Ingress resource is the Gateway API. It's more expressive, supports more traffic routing patterns, and is actively maintained.</p>

<pre># Install Gateway API CRDs:
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/latest/download/standard-install.yaml

# Install a Gateway API implementation (e.g., Nginx Gateway Fabric):
kubectl apply -f https://raw.githubusercontent.com/nginxinc/nginx-gateway-fabric/main/deploy/default/deploy.yaml</pre>

<p>The migration from Ingress resources to Gateway API HTTPRoute resources is not automatic. You'll need to rewrite your ingress manifests.</p>

<pre># Old Ingress resource:
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80</pre>

<pre># Equivalent Gateway API HTTPRoute:
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: myapp
spec:
  parentRefs:
  - name: my-gateway
  hostnames:
  - app.example.com
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: myapp
      port: 80</pre>

<h3>Option 2 — Switch to Traefik</h3>

<p>Traefik is actively maintained, has excellent Docker and Kubernetes support, and handles certificate management automatically via Let's Encrypt. If you're running a small cluster (1-10 nodes), Traefik is the lowest-friction migration.</p>

<pre># Install Traefik via Helm:
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik -n traefik --create-namespace</pre>

<p>Traefik supports standard Kubernetes Ingress resources — you don't need to rewrite your manifests immediately. Change <code>ingressClassName: nginx</code> to <code>ingressClassName: traefik</code>.</p>

<h3>Option 3 — Stay on Ingress NGINX (short term)</h3>

<p>The retired version doesn't stop working. If you're not on a tight security compliance deadline, you have a window to migrate carefully. Pin your version, don't upgrade, and set a migration deadline for yourself within 6 months.</p>

<div class="callout danger">
  <p><strong>Don't stay indefinitely.</strong> The longer you wait, the further behind you fall on Kubernetes API compatibility as your cluster upgrades but the ingress controller doesn't.</p>
</div>

<h2>If you're on managed Kubernetes</h2>

<p>Hetzner Cloud, DigitalOcean, Vultr, and most managed Kubernetes providers have their own load balancer integrations. These are separate from the in-cluster ingress controller and are not affected by the retirement.</p>

<ul style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.2;">
  <li><strong>Hetzner K3s/MKS</strong> — use Hetzner Cloud Load Balancers with the hcloud controller, not Ingress NGINX</li>
  <li><strong>DigitalOcean Kubernetes</strong> — use DO Load Balancers with the DO cloud controller</li>
  <li><strong>Vultr Kubernetes Engine</strong> — use Vultr Load Balancers</li>
</ul>

<p>If you self-deployed Ingress NGINX on top of a managed cluster — you are affected and need to migrate.</p>

<h2>Migration checklist</h2>

<ul class="checklist">
  <li>Confirm you are running <code>registry.k8s.io/ingress-nginx/controller</code></li>
  <li>Inventory all Ingress resources: <code>kubectl get ingress --all-namespaces</code></li>
  <li>Choose replacement: Gateway API, Traefik, or HAProxy</li>
  <li>Set up new ingress controller in parallel (don't remove the old one yet)</li>
  <li>Migrate one service at a time, verify before continuing</li>
  <li>Update DNS or load balancer to point to new controller</li>
  <li>Remove old Ingress NGINX once all traffic is migrated</li>
  <li>Update SSL certificate management if using cert-manager with Ingress NGINX annotations</li>
</ul>

<div class="cta">
  <p>Running Nginx on self-hosted infra? Audit your reverse proxy config for dangling routes, missing SSL redirects, and Traefik migration issues.</p>
  <div class="cta-row">
    <a href="/proxy/">Reverse Proxy Mapper →</a>
    <a href="/ssl/" class="sec">SSL Checker →</a>
  </div>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/proxy/traefik-v2-to-v3/">Traefik v2 to v3 migration fix</a></li>
  <li><a href="/blog/traefik-v3-what-broke-in-the-wild/">Traefik v3 what broke in the wild</a></li>
  <li><a href="/fix/proxy/dangling-routes/">Dangling routes fix guide</a></li>
  <li><a href="/fix/nginx/502-bad-gateway/">Nginx 502 Bad Gateway fix</a></li>
</ul>
"""

# ── PAGE 2: Hetzner Production Checklist ─────────────────────────────────────

PAGE2_BODY = """
<p>Hetzner Cloud is one of the best-value Linux VPS providers in 2026. The hardware is good, the network is fast, and the pricing is a fraction of AWS or GCP for comparable specs. The default setup is not production-ready. Here's what to do before you put real traffic on it.</p>

<h2>1. Firewall — default is wide open</h2>

<p>A fresh Hetzner server has no firewall rules. Every port is accessible from the internet. The first thing to do after SSH access is confirmed:</p>

<pre>sudo apt update && sudo apt install ufw -y

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

sudo ufw status verbose</pre>

<div class="callout">
  <p><strong>Docker users:</strong> UFW does not protect Docker container ports. Bind containers to 127.0.0.1 — use <code>127.0.0.1:PORT:PORT</code> in docker-compose.yml. See the <a href="/fix/ufw/docker-bypass/">Docker UFW bypass fix</a>.</p>
</div>

<h2>2. SSH hardening</h2>

<pre># Disable password authentication (key-only):
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Disable root login:
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

sudo systemctl restart sshd</pre>

<div class="callout danger">
  <p><strong>Before disabling password auth:</strong> confirm your SSH key works in a second terminal session. Locking yourself out of a Hetzner server requires a rescue boot.</p>
</div>

<h2>3. fail2ban</h2>

<pre>sudo apt install fail2ban -y

# Create local config (never edit jail.conf directly):
sudo tee /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime  = 1h
findtime = 10m
maxretry = 3
backend  = systemd

[sshd]
enabled  = true
port     = ssh
maxretry = 3
bantime  = 24h

[recidive]
enabled  = true
logpath  = /var/log/fail2ban.log
banaction = %(banaction_allports)s
bantime  = 1w
findtime = 1d
maxretry = 5
EOF

sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd</pre>

<h2>4. SSL certificate</h2>

<pre># Install certbot (snap method — recommended on Ubuntu 22.04):
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Obtain certificate (Nginx):
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Verify auto-renewal timer:
sudo systemctl status snap.certbot.renew.timer

# Test renewal:
sudo certbot renew --dry-run</pre>

<h2>5. Docker setup (if using containers)</h2>

<pre># Install Docker:
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Critical: bind all container ports to localhost:
# In docker-compose.yml use:
# ports:
#   - "127.0.0.1:PORT:PORT"
# NOT:
#   - "PORT:PORT"

# Set default log rotation in /etc/docker/daemon.json:
sudo tee /etc/docker/daemon.json << 'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

sudo systemctl restart docker</pre>

<h2>6. Unattended security updates</h2>

<pre>sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -pmedium unattended-upgrades

# Verify it's enabled:
cat /etc/apt/apt.conf.d/20auto-upgrades</pre>

<p>Should show <code>APT::Periodic::Unattended-Upgrade "1";</code>.</p>

<h2>7. Swap (for low-RAM servers)</h2>

<p>Hetzner's CX11 (2GB RAM) and CX21 (4GB RAM) servers can run out of memory under load. Add swap as a safety net:</p>

<pre>sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab</pre>

<h2>8. Basic monitoring</h2>

<pre># Check current resource usage:
htop
df -h
free -h

# Watch Nginx error log:
sudo tail -f /var/log/nginx/error.log

# Watch fail2ban:
sudo fail2ban-client status
sudo journalctl -u fail2ban --since "1 hour ago"</pre>

<h2>Production-ready checklist</h2>

<ul class="checklist">
  <li>UFW enabled with default-deny incoming</li>
  <li>SSH key-only authentication (password auth disabled)</li>
  <li>Root login disabled</li>
  <li>fail2ban active with sshd jail and recidive jail</li>
  <li>SSL certificate installed and auto-renewal verified</li>
  <li>Docker containers bound to 127.0.0.1 (not 0.0.0.0)</li>
  <li>Docker log rotation configured</li>
  <li>Unattended security updates enabled</li>
  <li>Swap configured (for servers under 4GB RAM)</li>
</ul>

<div class="cta">
  <p>Audit your Hetzner server config — firewall rules, Docker port exposure, SSL expiry, and reverse proxy setup.</p>
  <div class="cta-row">
    <a href="/firewall/">Firewall Auditor →</a>
    <a href="/docker/" class="sec">Docker Auditor →</a>
  </div>
</div>

<h2>Related Hetzner guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/providers/hetzner/ssl-setup/">Hetzner SSL setup guide</a></li>
  <li><a href="/providers/hetzner/docker-firewall/">Hetzner Docker firewall setup</a></li>
  <li><a href="/providers/hetzner/ssh-hardening/">Hetzner SSH hardening</a></li>
  <li><a href="/providers/hetzner/ufw-docker/">Hetzner UFW + Docker</a></li>
  <li><a href="/fix/ufw/docker-bypass/">Docker UFW bypass fix</a></li>
  <li><a href="/blog/fail2ban-misconfigured/">fail2ban misconfiguration guide</a></li>
</ul>
"""

PAGES = [
    {
        "type": "blog",
        "slug": "ingress-nginx-retirement-2026",
        "title": "Ingress NGINX Retired in 2026: Migration Guide and Alternatives",
        "meta_desc": "Ingress NGINX (kubernetes/ingress-nginx) was officially retired in March 2026. What this means, how to check if you are affected, and migration paths to Gateway API and Traefik.",
        "keywords": "ingress nginx retired, ingress nginx deprecated 2026, kubernetes ingress nginx replacement, gateway api migration, ingress nginx end of life",
        "date": "2026-03-30",
        "tags": ["Kubernetes", "Nginx", "Migration", "DevOps"],
        "lede": "The kubernetes/ingress-nginx project was officially retired in March 2026. No more security patches. No more bug fixes. If your cluster is running it, here is what to do.",
        "body": POST1_BODY,
        "faq": [
            ("Is Ingress NGINX completely broken after retirement?",
             "No. The software continues to work after retirement — it just receives no more updates, security patches, or bug fixes. Your existing deployments will keep running but you should plan migration within 6 months before Kubernetes API compatibility issues arise."),
            ("What is the recommended replacement for Ingress NGINX?",
             "The Kubernetes project recommends migrating to the Gateway API, which is the official successor to the Ingress resource type. For simpler setups, Traefik is a popular alternative that supports standard Kubernetes Ingress resources without manifest rewrites."),
            ("Does this affect Nginx itself?",
             "No. Nginx the web server and reverse proxy is not affected. Only the kubernetes/ingress-nginx community ingress controller project was retired. Nginx Inc's commercial Nginx Ingress Controller is also not affected."),
        ],
        "path": "blog",
    },
    {
        "type": "provider",
        "slug": "production-checklist",
        "provider": "hetzner",
        "provider_name": "Hetzner",
        "title": "Hetzner Production-Ready Server Checklist (Ubuntu 22.04)",
        "meta_desc": "Complete production checklist for Hetzner Cloud servers: UFW firewall, SSH hardening, fail2ban, SSL certificates, Docker security, and unattended updates. Ubuntu 22.04.",
        "keywords": "hetzner production setup, hetzner server hardening, hetzner ubuntu 22.04 checklist, hetzner vps security setup",
        "date": "2026-03-30",
        "tags": ["Hetzner", "Linux", "Security", "DevOps"],
        "lede": "A fresh Hetzner server has no firewall, password SSH enabled, no fail2ban, and no log rotation. Here is everything to do before you put real traffic on it.",
        "body": PAGE2_BODY,
        "faq": [
            ("What is the first thing to do on a new Hetzner server?",
             "Install and configure UFW firewall with default-deny incoming before doing anything else. A fresh Hetzner server has every port open to the internet. Run: sudo ufw default deny incoming && sudo ufw allow ssh && sudo ufw enable."),
            ("Does UFW protect Docker containers on Hetzner?",
             "No. Docker bypasses UFW by inserting rules directly into iptables FORWARD chain. On Hetzner, bind all container ports to 127.0.0.1 in docker-compose.yml — use 127.0.0.1:PORT:PORT instead of PORT:PORT."),
            ("Which certbot installation method is recommended on Hetzner Ubuntu 22.04?",
             "Install certbot via snap: sudo snap install --classic certbot. The snap version includes automatic renewal via a systemd timer and is the recommended method on Ubuntu 22.04. Avoid installing certbot via apt on Ubuntu 22.04 as the apt version may be outdated."),
        ],
        "path": "providers/hetzner",
    },
]


def make_faq_schema(faqs):
    items = ",\n".join([
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faqs
    ])
    return f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}'


def build_page(p):
    tag_html = "".join([f'<span class="hero-tag{"" if t not in ["RETIRED","URGENT"] else " red"}">{t}</span>' for t in p["tags"]])
    faq_schema = make_faq_schema(p["faq"])

    if p["type"] == "blog":
        canonical = f"https://configclarity.dev/blog/{p['slug']}/"
        bc_items = f'''[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"https://configclarity.dev/blog/"}},
    {{"@type":"ListItem","position":3,"name":"{p['title']}","item":"{canonical}"}}
  ]'''
    else:
        canonical = f"https://configclarity.dev/providers/{p['provider']}/{p['slug']}/"
        bc_items = f'''[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Provider Guides","item":"https://configclarity.dev/providers/"}},
    {{"@type":"ListItem","position":3,"name":"{p['provider_name']}","item":"https://configclarity.dev/providers/{p['provider']}/"}},
    {{"@type":"ListItem","position":4,"name":"{p['title']}","item":"{canonical}"}}
  ]'''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{p['title']} — ConfigClarity</title>
  <meta name="description" content="{p['meta_desc']}">
  <meta name="keywords" content="{p['keywords']}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{p['meta_desc']}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="article">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article",
    "headline":"{p['title']}",
    "description":"{p['meta_desc']}",
    "url":"{canonical}",
    "datePublished":"{p['date']}",
    "dateModified":"{p['date']}",
    "author":{{"@type":"Organization","name":"MetricLogic","url":"https://metriclogic.dev"}},
    "publisher":{{"@type":"Organization","name":"ConfigClarity","url":"https://configclarity.dev"}}
  }}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":{bc_items}}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">{"<a href='/'>ConfigClarity</a> › <a href='/blog/'>Blog</a> › " + p['title'] if p['type'] == 'blog' else f"<a href='/'>ConfigClarity</a> › <a href='/providers/'>Providers</a> › <a href='/providers/{p['provider']}/'>{p['provider_name']}</a> › {p['title']}"}</div>
  <div class="hero">
    <div class="hero-meta"><span>{p['date']}</span> · {tag_html}</div>
    <h1>{p['title']}</h1>
    <p class="lede">{p['lede']}</p>
  </div>
  <div class="content">{p['body']}</div>
{FOOTER}
</body>
</html>"""


if __name__ == "__main__":
    print("=== Building 2 new pages ===\n")

    new_rewrites = []
    new_sitemap_urls = []

    for p in PAGES:
        # Build HTML
        html = build_page(p)

        # Validate JSON-LD
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        schema_ok = True
        for i, b in enumerate(blocks):
            try:
                json.loads(b)
            except Exception as e:
                print(f"  JSON ERROR block {i}: {e}")
                schema_ok = False

        # Write file
        if p["type"] == "blog":
            path = f"blog/{p['slug']}"
            url = f"/blog/{p['slug']}/"
        else:
            path = f"providers/{p['provider']}/{p['slug']}"
            url = f"/providers/{p['provider']}/{p['slug']}/"

        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.html", "w") as f:
            f.write(html)

        schema_status = "OK" if schema_ok else "SCHEMA_ERROR"
        print(f"  {schema_status}  {path}/index.html ({len(html):,} bytes)")

        new_rewrites.append({"source": url, "destination": f"{path}/index.html"})
        new_rewrites.append({"source": url.rstrip("/"), "destination": f"{path}/index.html"})
        new_sitemap_urls.append(url)

    # Update blog index for blog post
    with open("blog/index.html", "r") as f:
        content = f.read()
    blog_p = PAGES[0]
    if blog_p["slug"] not in content:
        tag_html = "&nbsp;".join([
            f'<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">{t}</span>'
            for t in blog_p["tags"]
        ])
        new_card = f"""    <a href="/blog/{blog_p['slug']}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">{blog_p['date']} &nbsp;·&nbsp; {tag_html}</div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">{blog_p['title']}</div>
      <div style="font-size:0.82rem;color:var(--muted);">{blog_p['meta_desc'][:120]}...</div>
    </a>\n"""
        marker = '<h1 style="font-size:1.6rem'
        content = content.replace(marker, new_card + "    " + marker, 1)
        with open("blog/index.html", "w") as f:
            f.write(content)
        print(f"  OK  blog/index.html — ingress-nginx post added")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)
    added = sum(1 for r in new_rewrites if r not in config["rewrites"])
    for r in new_rewrites:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  OK  vercel.json — {added} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    entries = []
    for url in new_sitemap_urls:
        if url not in sitemap:
            entries.append(f"  <url><loc>https://www.configclarity.dev{url}</loc><lastmod>2026-03-30</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>")
    if entries:
        sitemap = sitemap.replace("</urlset>", "\n".join(entries) + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
    print(f"  OK  sitemap-seo.xml — {len(entries)} URLs added")

    print(f"\nDone.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: ingress nginx retirement post + hetzner production checklist' && git push origin main && npx vercel --prod --force")
    print("\nGSC submit tomorrow:")
    print("  https://configclarity.dev/blog/ingress-nginx-retirement-2026/")
    print("  https://configclarity.dev/providers/hetzner/production-checklist/")
