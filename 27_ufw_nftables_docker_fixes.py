#!/usr/bin/env python3
"""
Script 27: Build UFW/nftables blog post + 2 Docker fix pages.
1. /blog/ufw-nftables-backend-ubuntu/ — targets big query cluster
2. /fix/docker/network-host/ — docker network_mode: host
3. /fix/docker/nvidia-gpu/ — NVIDIA GPU docker config
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

# ── BLOG POST: UFW nftables backend ──────────────────────────────────────────

BLOG_BODY = """
<p>Ubuntu 22.04 changed UFW's default firewall backend from iptables to nftables. For most people this change is completely invisible — UFW still works the same way from the command line. But if you're running Docker, or if you're mixing UFW with other firewall tools, this change matters and can cause rules to stop working in confusing ways.</p>

<h2>What changed in Ubuntu 22.04</h2>

<p>Ubuntu 22.04 ships with nftables as the default kernel firewall backend. When you install UFW on Ubuntu 22.04, it uses nftables under the hood instead of iptables. The UFW commands you already know (<code>ufw allow</code>, <code>ufw deny</code>, <code>ufw status</code>) all work the same — but the rules they generate are now nftables rules, not iptables rules.</p>

<pre># Check which backend UFW is using:
sudo ufw status verbose
cat /etc/default/ufw | grep "IPTABLES_BACKEND"

# Check nftables rules directly:
sudo nft list ruleset

# Check iptables (will show nftables rules via compatibility layer):
sudo iptables -L</pre>

<h2>Why this breaks Docker</h2>

<p>Docker has been using iptables for network management since the beginning. When Docker starts, it inserts rules into iptables chains — DOCKER, DOCKER-USER, DOCKER-ISOLATION-STAGE-1 — to manage container networking and port forwarding.</p>

<p>On Ubuntu 22.04, Docker still uses iptables even though UFW is now using nftables. This means Docker's rules and UFW's rules are in completely separate systems that don't interact with each other. UFW doesn't know about Docker's containers. Docker doesn't know about UFW's deny rules.</p>

<p>The result is the classic Docker UFW bypass: you add a UFW deny rule for a port, but the Docker container on that port is still accessible from the internet because Docker's iptables rules bypass UFW's nftables rules entirely.</p>

<pre># Verify Docker is still using iptables on Ubuntu 22.04:
sudo iptables -L DOCKER --line-numbers
# You'll see Docker's rules here even though UFW uses nftables</pre>

<h2>Check your current UFW backend</h2>

<pre>cat /etc/default/ufw</pre>

<p>Look for <code>IPT_SYSCTL</code> and <code>IPTABLES_BACKEND</code>. On Ubuntu 22.04 you'll typically see the backend set to <code>nftables</code> or the file may not specify it explicitly (defaulting to nftables).</p>

<pre># Also check the actual active firewall:
sudo nft list tables
# If you see tables like "inet ufw6" — UFW is using nftables

sudo iptables -L INPUT | head -5
# If you see DOCKER chains — Docker is using iptables</pre>

<h2>The fix: bind Docker ports to localhost</h2>

<p>The cleanest fix for the Docker/nftables conflict is to not expose Docker ports publicly in the first place. Bind all container ports to <code>127.0.0.1</code> and use Nginx or Traefik as a reverse proxy for public access.</p>

<pre># In docker-compose.yml — bind to localhost only:
services:
  myapp:
    ports:
      - "127.0.0.1:3000:3000"  # Only accessible locally
    # NOT: "3000:3000" — this binds to 0.0.0.0 and bypasses UFW

  db:
    ports:
      - "127.0.0.1:5432:5432"  # Database never public</pre>

<p>With this setup, the container ports are only accessible via localhost. Nginx on port 80/443 (which UFW allows) proxies traffic to the container. Docker's iptables bypass becomes irrelevant because there's nothing public to bypass to.</p>

<h2>Alternative: force Docker to use iptables compatibility mode</h2>

<p>If you need Docker ports to be directly accessible and want UFW to control them, you can configure Docker to use iptables in a way that interacts better with nftables:</p>

<pre># /etc/docker/daemon.json:
{
  "iptables": true,
  "ip6tables": true
}

sudo systemctl restart docker</pre>

<div class="callout">
  <p><strong>Note:</strong> Even with this setting, Docker's iptables rules and UFW's nftables rules operate in separate subsystems. The most reliable approach remains binding containers to 127.0.0.1 rather than relying on firewall rules to block container ports.</p>
</div>

<h2>What about Ubuntu 20.04?</h2>

<p>Ubuntu 20.04 uses iptables as the default backend. UFW and Docker both use iptables, so there's a different interaction — Docker's rules can actually interfere with UFW's rules in iptables. The Docker UFW bypass problem exists on both versions, just through different mechanisms.</p>

<pre># On Ubuntu 20.04 — check iptables backend:
sudo update-alternatives --display iptables
# Should show iptables-legacy or iptables-nft</pre>

<h2>Quick summary</h2>

<ul style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.4;">
  <li>Ubuntu 22.04: UFW uses nftables, Docker uses iptables — they don't interact</li>
  <li>Ubuntu 20.04: UFW uses iptables, Docker uses iptables — they interact but Docker bypasses UFW</li>
  <li>On both versions: bind container ports to 127.0.0.1 to avoid the problem entirely</li>
  <li>UFW commands work the same on both versions — the backend change is invisible to daily use</li>
</ul>

<div class="cta">
  <p>Audit your UFW rules for Docker bypass risk, nftables conflicts, and missing default-deny on Ubuntu 22.04.</p>
  <a href="/firewall/">Open Firewall Auditor →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/ufw/docker-bypass/">Docker UFW bypass fix guide</a></li>
  <li><a href="/fix/nftables/ubuntu-22/">nftables setup on Ubuntu 22.04</a></li>
  <li><a href="/fix/nftables/docker-conflict/">nftables and Docker conflict</a></li>
  <li><a href="/glossary/docker-ufw-bypass/">Docker UFW bypass explained</a></li>
  <li><a href="/blog/docker-ufw-bypass-explained/">Docker bypasses UFW — the full story</a></li>
</ul>
"""

BLOG = {
    "type": "blog",
    "slug": "ufw-nftables-backend-ubuntu",
    "title": "UFW and nftables on Ubuntu 22.04: What Changed and Why It Breaks Docker",
    "meta_desc": "Ubuntu 22.04 switched UFW's backend to nftables while Docker still uses iptables. Why this matters, how it affects your firewall rules, and the fix for Docker port exposure.",
    "keywords": "ufw nftables ubuntu 22.04, ufw backend nftables, ubuntu 22.04 firewall nftables, docker ufw nftables conflict, ufw iptables nftables ubuntu",
    "date": "2026-04-01",
    "tags": ["UFW", "Ubuntu", "Docker", "Linux", "Firewall"],
    "lede": "Ubuntu 22.04 quietly switched UFW to use nftables as its firewall backend. UFW commands still work exactly the same. But Docker still uses iptables — and now the two systems don't talk to each other at all, which makes the Docker UFW bypass problem worse, not better.",
    "body": BLOG_BODY,
    "faq": [
        ("What firewall backend does UFW use on Ubuntu 22.04?",
         "Ubuntu 22.04 uses nftables as the default firewall backend for UFW. UFW commands (ufw allow, ufw deny, ufw status) work identically, but the rules are now implemented as nftables rules instead of iptables rules."),
        ("Does the nftables backend change affect Docker on Ubuntu 22.04?",
         "Yes. Docker still uses iptables for container networking on Ubuntu 22.04, while UFW uses nftables. The two systems operate independently — UFW's deny rules do not block Docker container ports. This makes the Docker UFW bypass problem persist. The fix is to bind container ports to 127.0.0.1 in docker-compose.yml."),
        ("How do I check which firewall backend UFW is using?",
         "Run: sudo nft list tables — if you see tables starting with 'inet ufw' then UFW is using nftables. Also check: cat /etc/default/ufw for IPTABLES_BACKEND setting. Run: sudo iptables -L DOCKER to see Docker's iptables rules, which exist separately from UFW's nftables rules."),
    ],
}

# ── FIX PAGE: network_mode: host ─────────────────────────────────────────────

NETHOST_BODY = """
<p><code>network_mode: host</code> makes Docker containers share the host machine's network stack directly. Instead of the container getting its own network namespace with its own IP address, it uses the host's IP and all the host's network interfaces. Any port the container listens on is immediately accessible on the host's public IP.</p>

<p>This removes Docker's network isolation entirely. It's the most aggressive network setting in Docker and is almost never the right choice for a web service.</p>

<h2>What it looks like</h2>

<pre># docker-compose.yml with network_mode: host:
services:
  myapp:
    image: myapp:latest
    network_mode: host
    # No ports: section needed — container shares host network directly
    environment:
      PORT: 3000</pre>

<p>With this config, your application listening on port 3000 inside the container is immediately listening on port 3000 on the host's public IP. No port mapping. No Docker NAT. No UFW protection. Anyone who can reach your server can reach port 3000.</p>

<h2>Why it breaks security</h2>

<p><strong>Bypasses all Docker network isolation.</strong> Docker's default bridge network gives each container its own IP in a private subnet (172.17.0.0/16). Containers can't directly access each other or the host without explicit port mappings. <code>network_mode: host</code> eliminates this completely.</p>

<p><strong>UFW rules don't protect host-mode containers.</strong> UFW manages the host's INPUT chain. When a container uses host networking, its traffic flows through the host network stack directly. A UFW <code>deny 3000</code> rule may or may not apply depending on how the traffic arrives — the behavior is inconsistent and unreliable for host-mode containers.</p>

<p><strong>Container can see all host network traffic.</strong> A container in host mode can bind to any port on the host, including ports already in use by other services. It can also sniff traffic on the host's network interfaces if given sufficient privileges.</p>

<h2>The fix: use bridge networking with explicit port mapping</h2>

<pre># Remove network_mode: host entirely.
# Use explicit port mapping instead:
services:
  myapp:
    image: myapp:latest
    # network_mode: host  <-- remove this line
    ports:
      - "127.0.0.1:3000:3000"  # Bind to localhost only
    networks:
      - app-net

networks:
  app-net:
    driver: bridge</pre>

<p>Binding to <code>127.0.0.1:3000:3000</code> means the container's port 3000 is only accessible on the host's loopback interface. Nginx or Traefik running on the host can proxy to it. Nothing external can reach it directly.</p>

<h2>When network_mode: host is legitimate</h2>

<p>There are genuine use cases, though they're rare:</p>

<ul style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.4;">
  <li><strong>Network monitoring tools</strong> — tools that need to see all host network traffic (like a packet analyzer) legitimately need host networking</li>
  <li><strong>High-frequency trading / ultra-low latency</strong> — Docker's NAT layer adds microseconds of latency that matters in HFT contexts</li>
  <li><strong>Host network diagnostics</strong> — short-lived debug containers that need to see the full host network state</li>
</ul>

<p>For a web app, API server, database, cache, or message queue — none of these apply. Use bridge networking.</p>

<h2>Multi-container setups: use Docker networks instead</h2>

<p>The most common reason developers reach for <code>network_mode: host</code> is that they can't get two containers to talk to each other. The correct solution is a shared Docker network, not host networking:</p>

<pre>services:
  app:
    image: myapp:latest
    networks:
      - app-net
    ports:
      - "127.0.0.1:3000:3000"

  db:
    image: postgres:15
    networks:
      - app-net
    # No ports exposed — only accessible within app-net

networks:
  app-net:
    driver: bridge</pre>

<p>Containers on the same Docker network can reach each other by service name. <code>app</code> can connect to the database at <code>db:5432</code> without any port exposure.</p>

<div class="cta">
  <p>Paste your docker-compose.yml to detect network_mode: host, exposed ports, and other security issues automatically.</p>
  <a href="/docker/">Open Docker Auditor →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/ufw/docker-bypass/">Docker UFW bypass fix</a></li>
  <li><a href="/fix/docker/hardcoded-secrets/">Hardcoded secrets in Docker</a></li>
  <li><a href="/blog/docker-compose-security-checklist/">Docker Compose security checklist</a></li>
  <li><a href="/glossary/port-binding/">Port binding explained</a></li>
  <li><a href="/glossary/docker-ufw-bypass/">Docker UFW bypass explained</a></li>
</ul>
"""

# ── FIX PAGE: NVIDIA GPU docker ───────────────────────────────────────────────

NVIDIA_BODY = """
<p>Getting NVIDIA GPU access inside Docker containers is more finicky than it should be. The configuration has changed across Docker versions, NVIDIA driver versions, and Compose file formats — and the old ways of doing it still show up in tutorials that are now wrong. Here's the current correct approach.</p>

<h2>Prerequisites — check these first</h2>

<pre># Verify NVIDIA drivers are installed on the host:
nvidia-smi

# Verify the NVIDIA Container Toolkit is installed:
nvidia-ctk --version

# If nvidia-ctk is not installed:
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker</pre>

<p>If <code>nvidia-smi</code> fails — the problem is your host drivers, not Docker. Fix the host drivers first before debugging Docker GPU config.</p>

<h2>The current correct config (Docker Compose v3+)</h2>

<pre># docker-compose.yml — correct approach for 2024+:
services:
  inference:
    image: ollama/ollama:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "127.0.0.1:11434:11434"

volumes:
  ollama_data:</pre>

<p>The <code>deploy.resources.reservations.devices</code> block is the current correct way to request GPU access. Use <code>count: all</code> to use all available GPUs, or <code>count: 1</code} for a specific number, or <code>device_ids: ["0"]</code> for a specific GPU by index.</p>

<h2>The old way — deprecated but still everywhere in tutorials</h2>

<pre># OLD — do not use this:
services:
  inference:
    image: ollama/ollama:latest
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility</pre>

<p>The <code>runtime: nvidia</code> approach worked in older Docker versions but is deprecated. The <code>NVIDIA_VISIBLE_DEVICES</code> environment variable approach still works but is the legacy method. If you're seeing tutorials using these — they're probably written before 2022.</p>

<div class="callout danger">
  <p><strong>Conflict warning:</strong> Do not combine <code>runtime: nvidia</code> with <code>deploy.resources.reservations.devices</code> — they conflict. Pick one approach and use it consistently. The deploy.resources approach is preferred.</p>
</div>

<h2>Verify GPU access inside the container</h2>

<pre># Test GPU access:
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# If using Compose, exec into the running container:
docker compose exec inference nvidia-smi</pre>

<p>If <code>nvidia-smi</code> works inside the container — GPU access is configured correctly. If it fails with "no devices found" — check the Container Toolkit installation. If it fails with "command not found" — the container image doesn't have NVIDIA tools installed (that's fine for inference images that use CUDA without the CLI tools).</p>

<h2>Common errors and fixes</h2>

<h3>Error: could not select device driver with capabilities: [[gpu]]</h3>

<pre># The NVIDIA Container Toolkit is not configured for Docker:
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify the runtime is registered:
docker info | grep -i runtime</pre>

<h3>Error: unknown flag: --gpus</h3>

<pre># Docker version is too old — update Docker:
docker --version  # Need 19.03+
# Install latest Docker:
curl -fsSL https://get.docker.com | sh</pre>

<h3>Error: NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver</h3>

<pre># Host driver issue — check driver status:
sudo dkms status
sudo nvidia-smi
# If host nvidia-smi fails — reinstall host drivers first</pre>

<h2>Specific GPU selection</h2>

<pre># Use all GPUs:
devices:
  - driver: nvidia
    count: all
    capabilities: [gpu]

# Use exactly 1 GPU:
devices:
  - driver: nvidia
    count: 1
    capabilities: [gpu]

# Use specific GPU by ID:
devices:
  - driver: nvidia
    device_ids: ["0"]
    capabilities: [gpu]

# Use specific GPU by UUID:
devices:
  - driver: nvidia
    device_ids: ["GPU-abc123"]
    capabilities: [gpu]</pre>

<pre># Find your GPU IDs:
nvidia-smi -L</pre>

<h2>Ollama-specific config</h2>

<pre>services:
  ollama:
    image: ollama/ollama:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "127.0.0.1:11434:11434"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  ollama_data:</pre>

<div class="cta">
  <p>Paste your docker-compose.yml to detect deprecated GPU runtime config, missing healthchecks, and exposed ports.</p>
  <a href="/docker/">Open Docker Auditor →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/docker/hardcoded-secrets/">Hardcoded secrets in Docker</a></li>
  <li><a href="/fix/docker/missing-healthcheck/">Missing healthcheck fix</a></li>
  <li><a href="/blog/docker-compose-security-checklist/">Docker Compose security checklist</a></li>
  <li><a href="/blog/ollama-server-security/">Securing an Ollama server</a></li>
</ul>
"""

FIX_PAGES = [
    {
        "type": "fix",
        "path": "fix/docker/network-host",
        "url": "/fix/docker/network-host/",
        "title": "Fix: Docker network_mode: host — Risks and Safe Alternative",
        "meta_desc": "network_mode: host removes Docker network isolation entirely. How it works, why it breaks security and UFW rules, and the correct bridge networking alternative.",
        "keywords": "docker network_mode host, docker host network security, network_mode host risks, docker network isolation, docker host networking alternative",
        "date": "2026-04-01",
        "tags": ["Docker", "Networking", "Security"],
        "lede": "network_mode: host makes your Docker container share the host's network stack directly. Every port the container opens is immediately accessible on the host's public IP, bypassing all Docker network isolation and making UFW rules unreliable.",
        "body": NETHOST_BODY,
        "breadcrumb": '<a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/docker/">Docker</a> › network_mode: host',
        "faq": [
            ("What does network_mode: host do in Docker?",
             "network_mode: host makes the container share the host machine's network stack directly instead of getting its own isolated network namespace. Any port the container listens on is immediately accessible on the host's public IP address without any port mapping."),
            ("Does UFW protect Docker containers using network_mode: host?",
             "Unreliably. UFW manages the host INPUT chain. Containers using host networking bypass Docker's NAT layer, which changes how traffic is classified by the kernel firewall. The behavior is inconsistent and should not be relied upon. Use bridge networking with 127.0.0.1 port binding instead."),
            ("When is network_mode: host actually needed?",
             "Legitimate uses include: network monitoring tools that need raw access to host interfaces, ultra-low-latency applications where Docker NAT overhead is unacceptable, and short-lived diagnostic containers. For web apps, APIs, databases, and caches, bridge networking is always the right choice."),
        ],
    },
    {
        "type": "fix",
        "path": "fix/docker/nvidia-gpu",
        "url": "/fix/docker/nvidia-gpu/",
        "title": "Fix: NVIDIA GPU in Docker Compose — Current Correct Config (2026)",
        "meta_desc": "The correct way to configure NVIDIA GPU access in Docker Compose using deploy.resources.reservations.devices. Fixes for deprecated runtime: nvidia config and common errors.",
        "keywords": "nvidia gpu docker compose, docker compose gpu, ollama docker gpu, nvidia docker deprecated runtime, deploy resources reservations devices nvidia",
        "date": "2026-04-01",
        "tags": ["Docker", "NVIDIA", "GPU", "Ollama"],
        "lede": "NVIDIA GPU configuration in Docker has changed across versions and old tutorials still show deprecated approaches. The runtime: nvidia method is gone. Here is the current correct config and fixes for the most common errors.",
        "body": NVIDIA_BODY,
        "breadcrumb": '<a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/docker/">Docker</a> › NVIDIA GPU config',
        "faq": [
            ("What is the correct way to add GPU access in Docker Compose?",
             "Use the deploy.resources.reservations.devices block: specify driver: nvidia, count: all (or a number), and capabilities: [gpu]. This is the current correct approach for Docker Compose v3+. The older runtime: nvidia and NVIDIA_VISIBLE_DEVICES environment variable approaches are deprecated."),
            ("Why does Docker say could not select device driver with capabilities gpu?",
             "The NVIDIA Container Toolkit is not configured for Docker. Run: sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker. Then verify with: docker info | grep -i runtime."),
            ("Can I mix runtime: nvidia with deploy.resources.reservations.devices?",
             "No. These two approaches conflict with each other. Use deploy.resources.reservations.devices exclusively — it is the current supported method. Remove any runtime: nvidia lines from your compose file when using the deploy.resources approach."),
        ],
    },
]


def make_faq_schema(faqs):
    items = ",\n".join([
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faqs
    ])
    return f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}'


def build_blog_html(p):
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
  {{"@context":"https://schema.org","@type":"Article","headline":"{p['title']}","description":"{p['meta_desc']}","url":"{canonical}","datePublished":"{p['date']}","dateModified":"{p['date']}","author":{{"@type":"Organization","name":"MetricLogic","url":"https://metriclogic.dev"}},"publisher":{{"@type":"Organization","name":"ConfigClarity","url":"https://configclarity.dev"}}}}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"https://configclarity.dev/blog/"}},{{"@type":"ListItem","position":3,"name":"{p['title'][:55]}","item":"{canonical}"}}]}}
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


def build_fix_html(p):
    tag_html = "".join([f'<span class="hero-tag">{t}</span>' for t in p["tags"]])
    faq_schema = make_faq_schema(p["faq"])
    canonical = f"https://configclarity.dev{p['url']}"
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
  {{"@context":"https://schema.org","@type":"TechArticle","headline":"{p['title']}","description":"{p['meta_desc']}","url":"{canonical}","datePublished":"{p['date']}","dateModified":"{p['date']}","author":{{"@type":"Organization","name":"MetricLogic"}}}}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},{{"@type":"ListItem","position":2,"name":"Fix Guides","item":"https://configclarity.dev/fix/"}},{{"@type":"ListItem","position":3,"name":"Docker","item":"https://configclarity.dev/fix/docker/"}},{{"@type":"ListItem","position":4,"name":"{p['title'][:50]}","item":"{canonical}"}}]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">{p['breadcrumb']}</div>
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
    print("=== Building 3 pages ===\n")

    new_rewrites = []
    new_sitemap_urls = []

    # Build blog post
    html = build_blog_html(BLOG)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    ok = all(json.loads(b) is not None for b in blocks if json.loads(b) is not None)
    path = f"blog/{BLOG['slug']}"
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/index.html", "w") as f:
        f.write(html)
    print(f"  OK  {path}/index.html ({len(html):,} bytes)")
    new_rewrites += [
        {"source": f"/blog/{BLOG['slug']}/", "destination": f"blog/{BLOG['slug']}/index.html"},
        {"source": f"/blog/{BLOG['slug']}", "destination": f"blog/{BLOG['slug']}/index.html"},
    ]
    new_sitemap_urls.append(f"/blog/{BLOG['slug']}/")

    # Build fix pages
    for p in FIX_PAGES:
        html = build_fix_html(p)
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        schema_ok = True
        for b in blocks:
            try:
                json.loads(b)
            except Exception as e:
                print(f"  JSON ERROR {p['path']}: {e}")
                schema_ok = False
        os.makedirs(p["path"], exist_ok=True)
        with open(f"{p['path']}/index.html", "w") as f:
            f.write(html)
        print(f"  {'OK' if schema_ok else 'ERR'}  {p['path']}/index.html ({len(html):,} bytes)")
        new_rewrites += [
            {"source": p["url"], "destination": f"{p['path']}/index.html"},
            {"source": p["url"].rstrip("/"), "destination": f"{p['path']}/index.html"},
        ]
        new_sitemap_urls.append(p["url"])

    # Update blog index
    with open("blog/index.html", "r") as f:
        content = f.read()
    if BLOG["slug"] not in content:
        tag_html = "&nbsp;".join([f'<span style="background:rgba(108,99,255,.15);color:var(--purple);padding:.1rem .4rem;border-radius:3px;font-size:.68rem;">{t}</span>' for t in BLOG["tags"]])
        card = f"""    <a href="/blog/{BLOG['slug']}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1.5rem;margin-bottom:1rem;text-decoration:none;">
      <div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.5rem;">{BLOG['date']} &nbsp;·&nbsp; {tag_html}</div>
      <div style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.4rem;line-height:1.4;">{BLOG['title']}</div>
      <div style="font-size:0.82rem;color:var(--muted);">{BLOG['meta_desc'][:120]}...</div>
    </a>\n"""
        marker = '<h1 style="font-size:1.6rem'
        content = content.replace(marker, card + "    " + marker, 1)
        with open("blog/index.html", "w") as f:
            f.write(content)
        print(f"  OK  blog/index.html — card added")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)
    added = 0
    for r in new_rewrites:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)
            added += 1
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  OK  vercel.json — {added} rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()
    added_urls = 0
    for url in new_sitemap_urls:
        if url not in sitemap:
            entry = f"  <url><loc>https://www.configclarity.dev{url}</loc><lastmod>2026-04-01</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
            sitemap = sitemap.replace("</urlset>", entry + "\n</urlset>")
            added_urls += 1
    with open("sitemap-seo.xml", "w") as f:
        f.write(sitemap)
    print(f"  OK  sitemap-seo.xml — {added_urls} URLs added")

    print(f"\nDone. 3 pages built.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: ufw nftables blog + docker network-host + nvidia gpu fix pages' && git push origin main && npx vercel --prod --force")
    print("\nGSC submit:")
    for url in new_sitemap_urls:
        print(f"  https://configclarity.dev{url}")
