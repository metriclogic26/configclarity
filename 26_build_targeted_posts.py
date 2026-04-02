#!/usr/bin/env python3
"""
Script 26: Build 3 targeted blog posts in human language.
1. Why Google ignores crawl-delay
2. Hardcoded secrets in Docker: how they get exposed
3. SSH hardening on a fresh Linux server
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


POST1 = {
    "slug": "google-ignores-crawl-delay",
    "title": "Why Google Ignores Crawl-Delay in robots.txt (And What to Use Instead)",
    "meta_desc": "Google officially ignores the Crawl-delay directive in robots.txt. Why it was never adopted, what Googlebot actually uses to manage crawl rate, and how to slow it down if needed.",
    "keywords": "google robots.txt crawl-delay not supported, google ignores crawl-delay, crawl-delay robots.txt google, how to slow down googlebot, google search console crawl rate",
    "date": "2026-03-31",
    "tags": ["robots.txt", "SEO", "Google", "Crawling"],
    "lede": "You added Crawl-delay: 10 to your robots.txt. Googlebot is still hammering your server. This is not a bug — Google has never supported Crawl-delay and has no plans to. Here's what actually works.",
    "body": """
<p>The Crawl-delay directive has been in the robots.txt specification for decades. Bing respects it. Yandex respects it. DuckDuckGo respects it. Google does not, and has been public about this since at least 2008.</p>

<p>The reason is philosophical as much as technical. Google's position is that Crawl-delay is a blunt instrument — it applies the same delay to every resource on your site regardless of how expensive each one is to serve. A 10-second delay on a lightweight HTML page is wasteful. The same delay on a page that triggers a heavy database query might not be enough. Google prefers to manage crawl rate based on actual server response times rather than a static hint.</p>

<h2>What Google uses instead</h2>

<p>Googlebot manages its crawl rate through two mechanisms:</p>

<p><strong>Automatic throttling based on response times.</strong> Googlebot watches how long your server takes to respond. If responses are slow, it backs off. If they're fast, it crawls more aggressively. This is dynamic and continuous — it adjusts throughout a crawl session, not just at the start.</p>

<p><strong>Google Search Console crawl rate setting.</strong> This is the only way to explicitly tell Google to crawl your site more slowly. It's a manual control in GSC that limits the maximum rate Googlebot uses.</p>

<pre># How to access it:
# Google Search Console → Settings → Crawl rate
# Set to "Limit Google's maximum crawl rate"
# Adjust the slider</pre>

<div class="callout">
  <p><strong>Note:</strong> The GSC crawl rate setting is only available for root domains, not subdomains or specific paths. And it's advisory — Google may still crawl at a higher rate if it thinks your site can handle it.</p>
</div>

<h2>When does crawl-delay actually matter</h2>

<p>If Googlebot is causing server load issues, the crawl rate control in GSC is your lever. But before you reach for it, check whether Googlebot is actually the problem.</p>

<pre># Check your access logs for Googlebot activity:
grep -i googlebot /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head

# Check the rate — requests per minute:
grep -i googlebot /var/log/nginx/access.log | awk '{print $4}' | cut -d: -f2 | sort | uniq -c</pre>

<p>Googlebot is usually not the cause of server load issues. More commonly it's your own cron jobs, a slow database query, or a traffic spike from actual users. Check the logs before blaming the crawler.</p>

<h2>What crawl-delay is still useful for</h2>

<p>Even though Google ignores it, Crawl-delay is worth keeping if you have other crawlers visiting your site. Bing, DuckDuckGo, and many smaller crawlers do respect it. If you're running a low-resource server and want to limit any crawler that's not Googlebot, a reasonable Crawl-delay value helps.</p>

<pre># A robots.txt that limits non-Google crawlers:
User-agent: *
Crawl-delay: 2

# Googlebot ignores the above, but you can address it directly:
User-agent: Googlebot
# No crawl-delay here — use GSC instead
Allow: /

User-agent: Bingbot
Crawl-delay: 3</pre>

<p>A Crawl-delay of 1-3 seconds is a reasonable default for non-Googlebot crawlers. Values over 10 can negatively affect indexing speed for crawlers that do respect it.</p>

<h2>The GSC crawl rate control — step by step</h2>

<p>If you genuinely need to slow Googlebot down:</p>

<ol style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.4;">
  <li>Open Google Search Console for your property</li>
  <li>Go to Settings (gear icon, bottom left)</li>
  <li>Find "Crawl rate" under the Google index section</li>
  <li>Select "Limit Google's maximum crawl rate"</li>
  <li>Drag the slider to your desired limit</li>
  <li>Save — takes effect within a day or two</li>
</ol>

<p>The effect is gradual. Google won't immediately drop to your specified rate but will trend toward it over the following days. Monitor your server load and adjust.</p>

<h2>Your robots.txt crawl-delay isn't broken</h2>

<p>If your robots.txt has <code>Crawl-delay: 10</code> and Googlebot is still crawling at full speed — nothing is wrong with your file. Google is reading your robots.txt correctly. It's just choosing to ignore that specific directive, as it always has.</p>

<div class="cta">
  <p>Validate your robots.txt and check crawl-delay settings, AI bot coverage, and sitemap references.</p>
  <a href="/robots/">Open robots.txt Validator →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/robots/crawl-delay-too-high/">Crawl-delay too high fix guide</a></li>
  <li><a href="/blog/ai-crawler-opt-out-robots-txt/">AI crawler opt-out: what robots.txt can and cannot do</a></li>
  <li><a href="/fix/robots/missing-sitemap-reference/">Missing sitemap reference fix</a></li>
  <li><a href="/fix/robots/noindex-vs-disallow/">noindex vs Disallow</a></li>
</ul>
""",
    "faq": [
        ("Does Google support Crawl-delay in robots.txt?",
         "No. Google has officially stated it does not support the Crawl-delay directive and has no plans to. Googlebot manages crawl rate based on server response times and the crawl rate setting in Google Search Console."),
        ("How do I slow down Googlebot?",
         "Use Google Search Console: Settings → Crawl rate → Limit Google's maximum crawl rate. This is the only mechanism Google officially supports for controlling Googlebot's crawl speed. The Crawl-delay directive in robots.txt is ignored by Google."),
        ("Should I remove Crawl-delay from my robots.txt?",
         "Not necessarily. While Google ignores it, other crawlers like Bing, DuckDuckGo, and Yandex do respect it. Keeping a Crawl-delay of 1-3 seconds is a reasonable setting that limits non-Google crawlers without significantly impacting their indexing speed."),
    ],
}


POST2 = {
    "slug": "hardcoded-secrets-docker-exposed",
    "title": "Hardcoded Secrets in Docker: How They Get Exposed and How to Find Them",
    "meta_desc": "Hardcoded secrets in docker-compose.yml are one of the most common causes of data breaches on self-hosted servers. How they end up in your config, where they leak, and how to find them.",
    "keywords": "hardcoded secrets docker, docker compose secrets exposed, docker secrets detection, hardcoded passwords docker-compose, secrets in docker environment variables",
    "date": "2026-03-31",
    "tags": ["Docker", "Security", "DevOps"],
    "lede": "A developer sets up a new service, puts the database password directly in docker-compose.yml to get it working quickly, commits the file to Git, and moves on. Six months later the repo goes public. This is not a hypothetical — it happens constantly and the consequences range from annoying to catastrophic.",
    "body": """
<p>Hardcoded secrets are credentials, API keys, passwords, and tokens written directly into configuration files. In the Docker world, they usually show up in <code>docker-compose.yml</code> environment blocks, in <code>.env</code> files that get committed to version control, or in <code>Dockerfile</code> ARG and ENV instructions.</p>

<p>The problem isn't that the value is in the file — it's that the file goes places the secret was never meant to go.</p>

<h2>How they leak</h2>

<p><strong>Git history.</strong> This is the most common leak vector. A developer adds a password to docker-compose.yml, commits it, then replaces it with an environment variable reference in a later commit. The password is gone from the current file but it's permanently preserved in the git history. Anyone who clones the repo — even years later — can see it with <code>git log -p</code>.</p>

<pre># Find secrets in git history:
git log --all -p | grep -i "password|secret|api_key|token" | head -20</pre>

<p><strong>Accidentally public repositories.</strong> A private repo gets made public. A developer creates a public fork. A CI/CD pipeline logs environment variables. The repo gets added to a job board or portfolio. Any of these exposes the secrets to anyone who looks.</p>

<p><strong>Docker image layers.</strong> If you copy a file containing secrets into a Docker image during the build process, that file is baked into the image layer permanently — even if you delete it in a later layer. Anyone who pulls the image can extract the layer and read the file.</p>

<pre># Bad — secret is in the image layer even after deletion:
COPY .env /app/.env
RUN python setup.py
RUN rm /app/.env  # Too late — it's already in layer 2</pre>

<p><strong>Container inspection.</strong> Any user with Docker socket access can read the environment variables of running containers:</p>

<pre>docker inspect container_name | grep -i "env" -A 50</pre>

<p>This means anyone with <code>docker</code> group membership on your server can read every secret in every running container.</p>

<h2>What hardcoded secrets look like in the wild</h2>

<pre># Classic example — everything hardcoded:
services:
  app:
    image: myapp:latest
    environment:
      DATABASE_URL: postgres://admin:SuperSecret123@db:5432/mydb
      API_KEY: sk-abc123def456
      REDIS_PASSWORD: redis_pass_here
      JWT_SECRET: my-super-secret-jwt-key

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: SuperSecret123
      POSTGRES_USER: admin</pre>

<p>This is what the Docker Auditor flags as CRITICAL. Every value in those environment blocks is a literal credential that will be visible to anyone who reads the file.</p>

<h2>The correct pattern</h2>

<pre># docker-compose.yml — no secrets, only references:
services:
  app:
    image: myapp:latest
    environment:
      DATABASE_URL: ${DATABASE_URL}
      API_KEY: ${API_KEY}
      REDIS_PASSWORD: ${REDIS_PASSWORD}
      JWT_SECRET: ${JWT_SECRET}

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_USER: ${POSTGRES_USER}</pre>

<pre># .env — actual values, never committed to git:
DATABASE_URL=postgres://admin:SuperSecret123@db:5432/mydb
API_KEY=sk-abc123def456
REDIS_PASSWORD=redis_pass_here
JWT_SECRET=my-super-secret-jwt-key
POSTGRES_PASSWORD=SuperSecret123
POSTGRES_USER=admin</pre>

<pre># .gitignore — must include .env:
.env
.env.local
.env.production
*.env</pre>

<p>The <code>docker-compose.yml</code> is safe to commit. The <code>.env</code> file is not — it contains the actual values and must never leave your server.</p>

<h2>Finding hardcoded secrets in your current setup</h2>

<p>Check your running docker-compose files:</p>

<pre># Scan for common secret patterns:
grep -rn "password|secret|api_key|token|passwd" \
  --include="docker-compose*.yml" \
  --include=".env*" . | grep -v "^\s*#" | grep "=.\{4\}"</pre>

<p>Check your git history for previously committed secrets:</p>

<pre># Search across all commits:
git log --all -p -- "*.yml" "*.env" | grep -i "password|secret|key" | grep "^+" | grep -v "^\+\+\+"</pre>

<p>If you find secrets in git history — the secret is compromised regardless of whether you've removed it from the current files. Rotate the credential immediately. A removed secret in history is still a leaked secret.</p>

<div class="callout danger">
  <p><strong>If your secrets are already in a public repo's history:</strong> rotate them immediately. Removing the file or the commit doesn't help — GitHub, GitLab, and any forks already have the data. Change the password, revoke the API key, regenerate the JWT secret. Then clean the history with git filter-repo.</p>
</div>

<h2>Docker Compose secrets (production pattern)</h2>

<p>For production setups, Docker has a native secrets mechanism that mounts secrets as files rather than environment variables:</p>

<pre>services:
  app:
    image: myapp:latest
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt</pre>

<p>The secret is mounted at <code>/run/secrets/db_password</code> inside the container. Your application reads it from the file. It never appears in <code>docker inspect</code> output or environment variable listings.</p>

<div class="cta">
  <p>Paste your docker-compose.yml to scan for hardcoded secrets, missing healthchecks, and exposed ports automatically.</p>
  <a href="/docker/">Open Docker Auditor →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/docker/hardcoded-secrets/">Hardcoded secrets fix guide</a></li>
  <li><a href="/glossary/hardcoded-secrets/">What are hardcoded secrets?</a></li>
  <li><a href="/incidents/docker-secrets-exposed/">Incident: hardcoded secrets in docker-compose files</a></li>
  <li><a href="/blog/docker-compose-security-checklist/">Docker Compose security checklist</a></li>
</ul>
""",
    "faq": [
        ("What is a hardcoded secret in Docker Compose?",
         "A hardcoded secret is when you write a literal credential value directly in docker-compose.yml — like POSTGRES_PASSWORD: mysecret — instead of referencing an environment variable like POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}. The problem is that the compose file gets committed to version control while the secret should only exist on the server."),
        ("How do I find hardcoded secrets in my Docker Compose files?",
         "Paste your docker-compose.yml into ConfigClarity's Docker Auditor — it scans all environment blocks for literal credential values. You can also search manually: grep -rn 'password|secret|api_key' --include='docker-compose*.yml' ."),
        ("If I remove a secret from git history, is it safe?",
         "No. If the secret was ever pushed to a remote repository, assume it is compromised. Forks, clones, and CI/CD systems may have cached the history. The correct response is to rotate the credential immediately — change the password or revoke and regenerate the API key — then clean the git history with git filter-repo."),
    ],
}


POST3 = {
    "slug": "ssh-hardening-linux-server",
    "title": "SSH Hardening on a Fresh Linux Server: The Practical Guide",
    "meta_desc": "How to harden SSH on a new Linux server — disable password auth, disable root login, change the port, set up fail2ban, and verify everything is working without locking yourself out.",
    "keywords": "ssh hardening linux, ssh server hardening ubuntu, disable ssh password authentication, harden sshd config, ssh security linux vps",
    "date": "2026-03-31",
    "tags": ["SSH", "Linux", "Security", "DevOps"],
    "lede": "Every new VPS comes with SSH wide open. Password authentication enabled. Root login allowed. Port 22 listening on all interfaces. Within minutes of the server coming online, bots are already trying passwords. Here's how to close those gaps in order — without accidentally locking yourself out.",
    "body": """
<p>SSH hardening is one of those tasks that feels straightforward until you lock yourself out of your own server. The order of operations matters a lot here. Do the steps wrong and you're looking at a rescue console or a full server rebuild.</p>

<p>This guide does everything in the right order. Read it once before running any commands.</p>

<h2>Before you start: open a second SSH session</h2>

<p>This is not optional. Before making any changes to SSH configuration, open a second terminal and connect to your server. Keep it open. If your primary session disconnects, you have a working backup. If your backup also disconnects — you've locked yourself out and need the provider's console.</p>

<pre># Terminal 1: your working session where you make changes
# Terminal 2: keep this connected as a backup the entire time

# Verify you can connect before starting:
ssh user@your-server-ip "echo connected"</pre>

<h2>Step 1: Set up SSH key authentication</h2>

<p>Do this first, before disabling password authentication. If you disable passwords before setting up keys, you lock yourself out.</p>

<pre># On your LOCAL machine — generate a key if you don't have one:
ssh-keygen -t ed25519 -C "your-server-name"

# Copy your public key to the server:
ssh-copy-id user@your-server-ip

# Verify key auth works — open a NEW terminal and connect:
ssh user@your-server-ip
# If this connects without asking for a password, keys are working</pre>

<p>Only proceed to the next step after confirming key authentication works in a fresh terminal.</p>

<h2>Step 2: Disable password authentication</h2>

<pre>sudo nano /etc/ssh/sshd_config

# Find and change these lines:
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys</pre>

<p>Don't restart SSH yet. Make all your config changes first, then restart once.</p>

<h2>Step 3: Disable root login</h2>

<pre># In /etc/ssh/sshd_config:
PermitRootLogin no</pre>

<p>If you need to run commands as root, use <code>sudo</code> from your regular user account. Direct root SSH login is unnecessary and increases your attack surface.</p>

<h2>Step 4: Limit login attempts</h2>

<pre># In /etc/ssh/sshd_config:
MaxAuthTries 3
MaxSessions 5
LoginGraceTime 30</pre>

<p><code>MaxAuthTries 3</code> limits how many password attempts before the connection is dropped. <code>LoginGraceTime 30</code> gives users 30 seconds to authenticate before the connection times out.</p>

<h2>Step 5: Disable unused authentication methods</h2>

<pre># In /etc/ssh/sshd_config:
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
PrintMotd no</pre>

<p>Unless you specifically need X11 forwarding or TCP tunneling, disable them. These features increase attack surface without benefit for most setups.</p>

<h2>Step 6: Apply the config</h2>

<pre># Test the config before restarting:
sudo sshd -t

# If no errors, restart SSH:
sudo systemctl restart sshd

# Verify SSH is running:
sudo systemctl status sshd</pre>

<div class="callout danger">
  <p><strong>Critical:</strong> After restarting SSH, test that your key authentication still works from your backup terminal before closing your primary session. If the backup terminal can connect — you're done. If it can't connect — something went wrong and you still have your primary session to fix it.</p>
</div>

<h2>Step 7: Set up fail2ban</h2>

<pre>sudo apt install fail2ban -y

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
EOF

sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd</pre>

<h2>Optional: change the SSH port</h2>

<p>Changing from port 22 to a high-numbered port (e.g., 2222 or 22022) eliminates the vast majority of automated scanning. It's security through obscurity — not a substitute for proper hardening — but it drastically reduces log noise.</p>

<pre># In /etc/ssh/sshd_config:
Port 2222

# Update UFW to allow the new port:
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp  # Only after confirming the new port works

# Restart SSH:
sudo systemctl restart sshd

# Connect on the new port to verify:
ssh -p 2222 user@your-server-ip</pre>

<div class="callout">
  <p><strong>Important:</strong> update your firewall rules before restarting SSH on the new port. If you close port 22 in UFW before opening the new port, you lock yourself out.</p>
</div>

<h2>Verify your hardening</h2>

<pre># Check current SSH config:
sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin|pubkeyauthentication|maxauthtries'

# Check fail2ban is active:
sudo fail2ban-client status sshd

# Check who's been blocked:
sudo fail2ban-client status sshd | grep "Banned IP"

# Check for recent login attempts in the log:
sudo journalctl -u sshd --since "1 hour ago" | grep -i "failed|invalid"</pre>

<h2>The complete sshd_config changes summary</h2>

<pre># Changes to make in /etc/ssh/sshd_config:
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
MaxAuthTries 3
MaxSessions 5
LoginGraceTime 30
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
PrintMotd no</pre>

<div class="cta">
  <p>Audit your UFW firewall rules alongside SSH hardening — check for Docker bypass risk, missing default-deny, and open ports that shouldn't be public.</p>
  <a href="/firewall/">Open Firewall Auditor →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/providers/hetzner/ssh-hardening/">Hetzner SSH hardening guide</a></li>
  <li><a href="/providers/hetzner/production-checklist/">Hetzner production-ready server checklist</a></li>
  <li><a href="/blog/fail2ban-misconfigured/">fail2ban is misconfigured on most servers</a></li>
  <li><a href="/fix/ufw/default-deny-missing/">UFW default deny missing fix</a></li>
  <li><a href="/glossary/port-binding/">Port binding explained</a></li>
</ul>
""",
    "faq": [
        ("What is the most important SSH hardening step?",
         "Disabling password authentication and switching to SSH key-only authentication. This eliminates brute force attacks entirely since attackers cannot guess a private key. Always set up and verify key authentication before disabling password auth to avoid locking yourself out."),
        ("How do I disable root SSH login on Ubuntu?",
         "Edit /etc/ssh/sshd_config and set PermitRootLogin no. Then restart SSH with sudo systemctl restart sshd. Verify you can still connect as your regular user before closing your session."),
        ("Should I change the SSH port from 22?",
         "It reduces automated scanning noise significantly but is not a security measure on its own. Changing from port 22 to a high port eliminates the majority of bot traffic but determined attackers scan all ports. It works best combined with proper key authentication and fail2ban."),
    ],
}


POSTS = [POST1, POST2, POST3]


def make_faq_schema(faqs):
    items = ",\n".join([
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faqs
    ])
    return f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}'


def build_page(p):
    tag_html = "".join([f'<span class="hero-tag">{t}</span>' for t in p["tags"]])
    faq_schema = make_faq_schema(p["faq"])
    canonical = f"https://configclarity.dev/blog/{p['slug']}/"

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
    "publisher":{{"@type":"Organization","name":"ConfigClarity","url":"https://configclarity.dev"}},
    "isPartOf":{{"@type":"Blog","name":"ConfigClarity Blog","url":"https://configclarity.dev/blog/"}}
  }}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"https://configclarity.dev/blog/"}},
    {{"@type":"ListItem","position":3,"name":"{p['title'][:60]}","item":"{canonical}"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › {p['title'][:55]}...</div>
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
    print("=== Building 3 targeted blog posts ===\n")

    new_rewrites = []
    new_sitemap = []

    for p in POSTS:
        html = build_page(p)

        # Validate JSON-LD
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        ok = True
        for i, b in enumerate(blocks):
            try:
                json.loads(b)
            except Exception as e:
                print(f"  JSON ERROR {p['slug']} block {i}: {e}")
                ok = False

        path = f"blog/{p['slug']}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.html", "w") as f:
            f.write(html)
        print(f"  {'OK' if ok else 'SCHEMA_ERR'}  {path}/index.html ({len(html):,} bytes)")

        new_rewrites.append({"source": f"/blog/{p['slug']}/", "destination": f"blog/{p['slug']}/index.html"})
        new_rewrites.append({"source": f"/blog/{p['slug']}", "destination": f"blog/{p['slug']}/index.html"})
        new_sitemap.append(f"/blog/{p['slug']}/")

    # Update blog index
    with open("blog/index.html", "r") as f:
        content = f.read()
    added_cards = 0
    for p in POSTS:
        if p["slug"] not in content:
            tag_html = "&nbsp;".join([f'<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">{t}</span>' for t in p["tags"]])
            card = f"""    <a href="/blog/{p['slug']}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">{p['date']} &nbsp;·&nbsp; {tag_html}</div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">{p['title']}</div>
      <div style="font-size:0.82rem;color:var(--muted);">{p['meta_desc'][:120]}...</div>
    </a>\n"""
            marker = '<h1 style="font-size:1.6rem'
            content = content.replace(marker, card + "    " + marker, 1)
            added_cards += 1
    with open("blog/index.html", "w") as f:
        f.write(content)
    print(f"\n  OK  blog/index.html — {added_cards} cards added")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)
    added_rewrites = 0
    for r in new_rewrites:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)
            added_rewrites += 1
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  OK  vercel.json — {added_rewrites} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    added_urls = 0
    for url in new_sitemap:
        if url not in sitemap:
            entry = f"  <url><loc>https://www.configclarity.dev{url}</loc><lastmod>2026-03-31</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
            sitemap = sitemap.replace("</urlset>", entry + "\n</urlset>")
            added_urls += 1
    with open("sitemap-seo.xml", "w") as f:
        f.write(sitemap)
    print(f"  OK  sitemap-seo.xml — {added_urls} URLs added")

    print(f"\nDone. Blog is now 19 posts.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: crawl-delay, hardcoded secrets, SSH hardening posts' && git push origin main && npx vercel --prod --force")
    print("\nGSC — submit tomorrow:")
    for url in new_sitemap:
        print(f"  https://configclarity.dev{url}")
