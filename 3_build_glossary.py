#!/usr/bin/env python3
"""
Script 3: Build glossary index + 15 term pages.
Run from: ~/Projects/configclarity-fresh/
"""

import os

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">'

CSS = """
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      :root {
        --bg: #0b0d14; --bg2: #1e2130; --purple: #6c63ff;
        --green: #22c55e; --orange: #f97316; --red: #ef4444;
        --text: #e2e4f0; --muted: #8a8fb5;
      }
      body { background: var(--bg); color: var(--text); font-family: 'JetBrains Mono', monospace; min-height: 100vh; line-height: 1.7; }
      a { color: var(--purple); text-decoration: none; }
      a:hover { text-decoration: underline; }
      .header { padding: 1.5rem 2rem; border-bottom: 1px solid #2a2d3d; display: flex; align-items: center; gap: 1rem; }
      .header-logo { font-size: 1.1rem; font-weight: 700; color: var(--text); }
      .header-logo span { color: var(--purple); }
      .header-nav { margin-left: auto; display: flex; gap: 1rem; font-size: 0.8rem; color: var(--muted); }
      .header-nav a { color: var(--muted); }
      .breadcrumb { padding: 1rem 2rem 0; max-width: 760px; margin: 0 auto; font-size: 0.78rem; color: var(--muted); }
      .breadcrumb a { color: var(--muted); }
      .content { max-width: 760px; margin: 0 auto; padding: 2rem; }
      h1 { font-size: 1.7rem; font-weight: 700; margin-bottom: 1rem; }
      .definition-box { background: var(--bg2); border-left: 3px solid var(--purple); border-radius: 0 8px 8px 0; padding: 1.25rem 1.5rem; margin-bottom: 2rem; font-size: 0.95rem; }
      h2 { font-size: 1.1rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--text); }
      p { font-size: 0.875rem; color: var(--muted); margin-bottom: 1rem; }
      .tag { display: inline-block; font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(108,99,255,.15); color: var(--purple); margin-right: 0.4rem; margin-bottom: 0.4rem; }
      .related-links { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 0.5rem; }
      .related-links a { font-size: 0.8rem; padding: 0.3rem 0.75rem; background: var(--bg2); border: 1px solid #2a2d3d; border-radius: 6px; color: var(--text); }
      .related-links a:hover { border-color: var(--purple); text-decoration: none; }
      .faq-item { margin-bottom: 1.5rem; }
      .faq-q { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; }
      .faq-a { font-size: 0.85rem; color: var(--muted); }
      .tool-cta { background: var(--bg2); border: 1px solid #2a2d3d; border-radius: 8px; padding: 1.25rem 1.5rem; margin: 2rem 0; }
      .tool-cta p { color: var(--text); font-size: 0.85rem; margin-bottom: 0.75rem; }
      .tool-cta a { display: inline-block; background: var(--purple); color: #fff; padding: 0.4rem 1rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; text-decoration: none; }
      footer { text-align: center; padding: 2rem; font-size: 0.75rem; color: var(--muted); border-top: 1px solid #2a2d3d; margin-top: 2rem; }
      .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
      .card { background: var(--bg2); border: 1px solid #2a2d3d; border-radius: 8px; padding: 1.25rem 1.5rem; }
      .card:hover { border-color: var(--purple); }
      .card-title { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.35rem; }
      .card-desc { font-size: 0.78rem; color: var(--muted); }
    </style>
"""

HEADER = """
  <header class="header">
    <div class="header-logo"><a href="/" style="color:var(--text);text-decoration:none;">Config<span>Clarity</span></a></div>
    <nav class="header-nav">
      <a href="/">Cron</a><a href="/ssl/">SSL</a><a href="/docker/">Docker</a>
      <a href="/firewall/">Firewall</a><a href="/proxy/">Proxy</a><a href="/robots/">robots.txt</a>
    </nav>
  </header>
"""

FOOTER = """
  <footer>
    <p>Part of the <a href="https://metriclogic.dev">MetricLogic</a> network &nbsp;·&nbsp;
    <a href="https://configclarity.dev">ConfigClarity</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>
"""

# ─── GLOSSARY TERMS ────────────────────────────────────────────────────────────

TERMS = [
    {
        "slug": "docker-ufw-bypass",
        "title": "Docker UFW Bypass",
        "short": "Docker UFW bypass is a known misconfiguration where Docker's iptables rules expose container ports to the internet, ignoring UFW's deny rules.",
        "body": """<p>Docker UFW bypass occurs because Docker inserts its own iptables rules directly into the DOCKER chain, which is evaluated before UFW's INPUT chain rules. When you run a container with <code>-p 8080:80</code> or set <code>ports:</code> in docker-compose.yml, Docker adds an iptables ACCEPT rule that allows external traffic to reach the container regardless of your <code>ufw deny</code> rules.</p>

<p>This is not a bug — it's Docker's intended behavior for container networking. The problem is that most system administrators assume UFW protects all ports on the server. For standalone services this is true. For Dockerized services it is not, unless you explicitly configure Docker to respect UFW.</p>

<h2>Why This Happens</h2>
<p>Linux packet flow for incoming traffic evaluates iptables chains in order: PREROUTING → DOCKER → FORWARD → INPUT. UFW manages the INPUT chain. Docker manages the DOCKER and FORWARD chains. A packet destined for a Docker container never reaches the INPUT chain — it's routed through FORWARD before UFW can block it.</p>

<h2>How to Fix It</h2>
<p>The standard fix is to add <code>DOCKER-USER</code> chain rules or to bind container ports only to <code>127.0.0.1</code> (e.g., <code>127.0.0.1:8080:80</code>) so Docker does not expose the port on the public interface. For server-wide protection, the <code>/etc/docker/daemon.json</code> approach with <code>"iptables": false</code> is an option but breaks Docker's networking for external container access.</p>""",
        "faqs": [
            ("Does UFW protect Docker containers?", "No. UFW manages the Linux INPUT chain. Docker containers use the FORWARD chain, which UFW does not control by default. Docker ports are accessible from the internet even if UFW has no allow rule for them."),
            ("How do I check if Docker is bypassing UFW?", "Run: <code>sudo iptables -L DOCKER --line-numbers</code>. Any ACCEPT rules in that chain bypass UFW. You can also use the ConfigClarity Firewall Auditor — paste your <code>ufw status verbose</code> output and it will flag Docker bypass risk."),
            ("What is the safest Docker port binding?", "Bind to <code>127.0.0.1</code>: use <code>127.0.0.1:8080:80</code> in docker-compose.yml. This exposes the port only on the loopback interface, accessible via Nginx reverse proxy but not directly from the internet."),
        ],
        "related_tools": [("Firewall Auditor", "/firewall/"), ("Docker Auditor", "/docker/")],
        "related_fixes": [("/fix/docker/ufw-bypass/", "Docker UFW bypass fix"), ("/fix/ufw/docker-bypass/", "UFW Docker bypass fix")],
        "tags": ["Docker", "UFW", "iptables", "Firewall", "Security"],
    },
    {
        "slug": "port-binding",
        "title": "Port Binding",
        "short": "Port binding is the process of associating a network port on a host interface with a service or container, controlling which IP addresses and protocols can reach the service.",
        "body": """<p>Port binding determines two things: which port number a service listens on, and which network interface (IP address) the service is accessible from. The combination of IP address and port is called a socket.</p>

<p>In Docker, port binding is specified in docker-compose.yml as <code>HOST_IP:HOST_PORT:CONTAINER_PORT</code>. Omitting the HOST_IP (e.g., <code>8080:80</code>) binds to <code>0.0.0.0</code>, which means all interfaces including the public internet-facing interface. This is the most common cause of accidentally exposed services.</p>

<h2>Interface Binding Options</h2>
<p><code>0.0.0.0:8080:80</code> — all interfaces, publicly accessible. <code>127.0.0.1:8080:80</code> — loopback only, localhost access only. <code>192.168.1.x:8080:80</code> — specific private interface, LAN only.</p>

<h2>Why 0.0.0.0 Is Dangerous</h2>
<p>Services bound to 0.0.0.0 are reachable from any network interface including the public internet. Databases (Redis :6379, PostgreSQL :5432, MongoDB :27017) are frequently exposed this way via Docker without the operator realising. Combined with the Docker UFW bypass issue, these services bypass firewall protection entirely.</p>""",
        "faqs": [
            ("What does 0.0.0.0 port binding mean?", "A service bound to 0.0.0.0 listens on all network interfaces — loopback, private LAN, and public internet. Any machine that can reach the server's public IP on that port can connect to the service."),
            ("How do I check what ports are bound to 0.0.0.0?", "Run: <code>ss -tlnp</code> or <code>netstat -tlnp</code>. Look for <code>0.0.0.0:PORT</code> in the Local Address column. For Docker containers, run <code>docker ps --format 'table {{.Ports}}'</code>."),
            ("Should databases ever bind to 0.0.0.0?", "Almost never. Databases like Redis, PostgreSQL, and MongoDB should bind to <code>127.0.0.1</code> or a private network interface. Public exposure of database ports is one of the most common causes of data breaches on VPS servers."),
        ],
        "related_tools": [("Docker Auditor", "/docker/"), ("Firewall Auditor", "/firewall/")],
        "related_fixes": [("/fix/docker/port-exposure/", "Docker port exposure fix")],
        "tags": ["Networking", "Docker", "Security", "0.0.0.0", "Firewall"],
    },
    {
        "slug": "ssl-certificate-expiry",
        "title": "SSL Certificate Expiry",
        "short": "SSL certificate expiry occurs when a TLS certificate passes its validity end date, causing browsers to display security warnings and refuse HTTPS connections to the site.",
        "body": """<p>An SSL/TLS certificate is valid for a defined period — historically 1–2 years, and since September 2020 limited to 398 days maximum by major browsers. When a certificate expires, browsers display a full-page warning ("Your connection is not private") and most users will not proceed. The site becomes effectively inaccessible for non-technical visitors.</p>

<p>Certificate expiry is one of the most preventable causes of site outages. Unlike server failures, expiry is fully predictable — the date is embedded in the certificate itself and visible months in advance.</p>

<h2>Common Causes of Missed Expiry</h2>
<p>Auto-renewal failures are the most common cause. Let's Encrypt certificates expire every 90 days and require a working certbot or ACME renewal cron job. If the renewal job silently fails (wrong path, DNS mismatch, rate limit hit), the certificate expires without warning. CDN-fronted domains (Cloudflare, Fastly) have their own certificate lifecycle separate from the origin cert — many operators monitor only one of the two.</p>

<h2>The 200-Day Warning Standard</h2>
<p>ConfigClarity's SSL Checker flags certificates expiring within 200 days — not the standard 30-day window. This gives enough time to diagnose and fix renewal pipeline failures before the 30-day critical window. Let's Encrypt certificates issued today will expire in ~89 days if auto-renewal breaks immediately.</p>""",
        "faqs": [
            ("How long are SSL certificates valid?", "Since September 2020, browser-trusted TLS certificates are valid for a maximum of 398 days (roughly 13 months). Let's Encrypt certificates are valid for 90 days and are designed to auto-renew every 60 days."),
            ("What happens when an SSL certificate expires?", "Browsers display a full-page 'Your connection is not private' warning (ERR_CERT_DATE_INVALID). HTTPS connections are refused. The site remains accessible via HTTP but search engines will flag it. API clients and webhooks that enforce certificate validation will also fail."),
            ("How do I monitor SSL certificate expiry?", "ConfigClarity's SSL Checker checks multiple domains at once and flags anything expiring within 200 days with exact days remaining. For automated monitoring, set a cron job running <code>openssl s_client -connect domain.com:443</code> and parsing the <code>notAfter</code> field."),
        ],
        "related_tools": [("SSL Checker", "/ssl/")],
        "related_fixes": [("/fix/ssl/expiry-monitoring/", "SSL expiry monitoring fix"), ("/fix/ssl/nginx-renewal/", "Nginx SSL renewal fix"), ("/fix/ssl/traefik-renewal/", "Traefik SSL renewal fix")],
        "tags": ["SSL", "TLS", "HTTPS", "Certificate", "Let's Encrypt", "Security"],
    },
    {
        "slug": "cron-job-collision",
        "title": "Cron Job Collision",
        "short": "A cron job collision occurs when multiple scheduled cron jobs run simultaneously and compete for the same resources — CPU, disk I/O, database connections, or lock files — causing performance degradation or data corruption.",
        "body": """<p>Cron job collisions are silent failures. The individual jobs may complete without errors, but the concurrent execution degrades performance, corrupts data, or causes cascading failures that appear unrelated. A backup job and a database dump running at the same time is a classic example — both appear to succeed but the backup captures a mid-write database state.</p>

<p>The collision problem compounds on low-spec servers where scheduled tasks like log rotation, backup, cache clearing, and report generation are all set to run at midnight or hourly boundaries (0 * * * *).</p>

<h2>Types of Collision</h2>
<p><strong>Resource collision</strong> — two jobs competing for CPU/disk causes both to run slower. Common with backup jobs on I/O-limited VPS instances. <strong>Lock collision</strong> — two jobs trying to acquire the same file lock or database advisory lock. One waits, one times out. <strong>Data collision</strong> — two jobs reading and writing the same dataset. Most dangerous — can cause partial writes and corrupted state.</p>

<h2>flock as the Standard Fix</h2>
<p><code>flock</code> is the standard Linux tool for preventing concurrent cron job execution. Wrapping a cron command with <code>flock -n /tmp/job.lock</code> ensures only one instance runs at a time. If the lock cannot be acquired (a previous instance is still running), the new invocation exits immediately without error.</p>""",
        "faqs": [
            ("How do I detect overlapping cron jobs?", "Paste your <code>crontab -l</code> output into ConfigClarity's Cron Visualiser. It renders a 24-hour timeline showing every job's execution window and flags overlapping windows in red with a collision report."),
            ("What is flock safety for cron jobs?", "flock safety means wrapping your cron command with <code>flock -n /tmp/jobname.lock command</code>. If the previous run is still executing when the next scheduled run starts, the new invocation exits immediately instead of running concurrently."),
            ("Why do all my cron jobs run at midnight?", "It's the most common default. When a task is set up with no specific time in mind, developers often choose <code>0 0 * * *</code>. When multiple tasks pile up at the same minute, the server CPU and I/O spike simultaneously. Spread jobs across off-peak minutes — 0:05, 0:15, 0:30, 0:45."),
        ],
        "related_tools": [("Cron Visualiser", "/")],
        "related_fixes": [("/fix/cron/overlapping-jobs/", "Overlapping cron jobs fix"), ("/fix/cron/flock-safety/", "Cron flock safety fix"), ("/fix/cron/server-load-spike/", "Server load spike fix")],
        "tags": ["Cron", "Scheduling", "flock", "Linux", "DevOps"],
    },
    {
        "slug": "reverse-proxy",
        "title": "Reverse Proxy",
        "short": "A reverse proxy is a server that sits in front of backend applications and forwards client requests to them, handling TLS termination, load balancing, caching, and routing.",
        "body": """<p>A reverse proxy accepts incoming connections from clients and forwards them to one or more backend services. From the client's perspective, they are communicating with a single server. The backend services are hidden behind the proxy.</p>

<p>The most common reverse proxies in self-hosted Linux environments are Nginx, Caddy, Traefik, and HAProxy. In cloud environments, Cloudflare, AWS ALB, and Vercel's edge network serve as reverse proxies.</p>

<h2>What a Reverse Proxy Does</h2>
<p><strong>TLS termination</strong> — the proxy handles HTTPS, so backend services can communicate over plain HTTP internally. <strong>Host-based routing</strong> — route app.domain.com to one backend, api.domain.com to another, all on the same server. <strong>Path-based routing</strong> — route /api/ to one service, / to another. <strong>Load balancing</strong> — distribute traffic across multiple backend instances. <strong>Header manipulation</strong> — add X-Forwarded-For, X-Real-IP, security headers.</p>

<h2>Common Misconfigurations</h2>
<p>Dangling routes pointing to stopped containers are the most frequent issue — Nginx config references a backend that no longer exists, causing 502 errors. Missing SSL redirects (HTTP not redirected to HTTPS) are the second most common. Traefik users frequently encounter label conflicts when migrating from v2 to v3, as label syntax changed significantly.</p>""",
        "faqs": [
            ("What is the difference between a proxy and a reverse proxy?", "A forward proxy sits in front of clients and forwards their requests to servers — used for anonymity, content filtering, or caching outbound traffic. A reverse proxy sits in front of servers and forwards client requests to backend applications — used for TLS termination, routing, and load balancing."),
            ("Why use Nginx as a reverse proxy for Docker?", "Docker containers typically run on high-numbered ports (8080, 3000, 5000). Nginx acts as the public-facing server on ports 80 and 443, handles TLS, and proxies requests to the container's port. This means only Nginx needs to be exposed — container ports are bound to 127.0.0.1 only."),
            ("What is a dangling reverse proxy route?", "A dangling route is a proxy configuration pointing to a backend that no longer exists — a container that was stopped, a service that was moved, or a hostname that no longer resolves. The reverse proxy returns a 502 or 504 error for these routes."),
        ],
        "related_tools": [("Reverse Proxy Mapper", "/proxy/")],
        "related_fixes": [("/fix/nginx/502-bad-gateway/", "Nginx 502 fix"), ("/fix/nginx/ssl-redirect-missing/", "SSL redirect missing fix")],
        "tags": ["Nginx", "Reverse Proxy", "Traefik", "TLS", "Load Balancing", "DevOps"],
    },
    {
        "slug": "traefik-labels",
        "title": "Traefik Labels",
        "short": "Traefik labels are Docker Compose metadata that tell the Traefik reverse proxy how to route traffic to a container — defining hostnames, TLS settings, middleware, and service ports.",
        "body": """<p>Traefik uses Docker labels to auto-configure routing without a static config file. When Traefik discovers a container with routing labels, it automatically creates routes, applies middleware, and manages TLS certificates — all from the Docker Compose file itself.</p>

<p>The label system changed significantly between Traefik v2 and v3. Labels written for v2 will not work in v3, and the failure mode is silent — Traefik starts but the route is simply not created.</p>

<h2>Traefik v2 Label Syntax</h2>
<p><code>traefik.http.routers.app.rule=Host(`app.domain.com`)</code><br>
<code>traefik.http.routers.app.tls.certresolver=letsencrypt</code><br>
<code>traefik.http.services.app.loadbalancer.server.port=3000</code></p>

<h2>Breaking Changes in v3</h2>
<p>Traefik v3 removed the <code>traefik.frontend.*</code> and <code>traefik.backend.*</code> label prefixes used in v1. Several v2 features changed defaults: <code>allowEmptyServices</code> was removed, Docker provider requires explicit network configuration, and some middleware parameters were renamed.</p>""",
        "faqs": [
            ("Why are my Traefik labels not working after upgrading to v3?", "Traefik v3 removed several v2 label patterns and changed defaults. The most common issue is using old <code>traefik.frontend.*</code> labels from v1 (which were already deprecated in v2). Use ConfigClarity's Reverse Proxy Mapper — it detects v2 labels and generates the exact v3 replacements."),
            ("Do I need to restart Traefik when I change labels?", "No. Traefik watches the Docker socket for container events and updates its routing configuration dynamically. Changing labels and redeploying the container (docker compose up -d) is enough — Traefik picks up the new labels within seconds."),
            ("What is the minimum Traefik label set needed to route a container?", "At minimum: <code>traefik.enable=true</code>, <code>traefik.http.routers.NAME.rule=Host(`domain.com`)</code>, and <code>traefik.http.services.NAME.loadbalancer.server.port=PORT</code>. For HTTPS add <code>traefik.http.routers.NAME.tls.certresolver=letsencrypt</code>."),
        ],
        "related_tools": [("Reverse Proxy Mapper", "/proxy/")],
        "related_fixes": [("/fix/proxy/traefik-v2-to-v3/", "Traefik v2 to v3 migration fix")],
        "tags": ["Traefik", "Docker", "Reverse Proxy", "Labels", "Routing", "TLS"],
    },
    {
        "slug": "flock-safety",
        "title": "flock Safety",
        "short": "flock safety is the practice of wrapping cron jobs and scheduled scripts with the Linux flock command to prevent multiple simultaneous instances from running and causing resource conflicts or data corruption.",
        "body": """<p><code>flock</code> is a Linux utility that acquires a file-based advisory lock before executing a command. It ensures that only one instance of a script runs at any given time, even if cron schedules overlapping runs.</p>

<p>Without flock safety, a long-running cron job (backup, report generation, data sync) can be scheduled to run every 5 minutes. If the job takes 7 minutes, by the 5-minute mark a second instance starts running concurrently. Both instances compete for the same resources, write to the same files, and produce corrupted output.</p>

<h2>flock Syntax</h2>
<p>Non-blocking (skip if already running): <code>flock -n /tmp/jobname.lock /path/to/script.sh</code><br>
Blocking (wait up to 10 seconds): <code>flock -w 10 /tmp/jobname.lock /path/to/script.sh</code><br>
In crontab: <code>*/5 * * * * flock -n /tmp/backup.lock /usr/local/bin/backup.sh</code></p>

<h2>Lock File Placement</h2>
<p>Lock files are typically placed in <code>/tmp/</code> or <code>/var/run/</code>. The filename should be unique per job to avoid unrelated jobs blocking each other. <code>/tmp/</code> is cleared on reboot, so stale locks from crashed scripts are automatically removed on next boot.</p>""",
        "faqs": [
            ("What happens if a flock-protected job crashes?", "If the script crashes, the lock file remains but the file descriptor lock is released automatically by the kernel when the process exits. The next cron invocation can acquire the lock normally. Stale lock files in /tmp/ do not prevent re-execution."),
            ("Should I use flock -n or flock -w?", "Use <code>flock -n</code> (non-blocking) for jobs that should skip if already running — backups, report generation, cleanup scripts. Use <code>flock -w TIMEOUT</code> for jobs that should wait — database migrations, deployment scripts where you want the next run to proceed once the current run finishes."),
            ("How do I add flock safety to all my cron jobs?", "ConfigClarity's Cron Visualiser has a flock safety toggle. After analysing your crontab, enable flock safety to generate flock-wrapped versions of all your jobs with unique lock file names."),
        ],
        "related_tools": [("Cron Visualiser", "/")],
        "related_fixes": [("/fix/cron/flock-safety/", "Cron flock safety fix"), ("/fix/cron/overlapping-jobs/", "Overlapping jobs fix")],
        "tags": ["Cron", "flock", "Linux", "Concurrency", "Scheduling", "DevOps"],
    },
    {
        "slug": "hardcoded-secrets",
        "title": "Hardcoded Secrets",
        "short": "Hardcoded secrets are credentials, API keys, database passwords, or private keys embedded directly in source code, configuration files, or container definitions instead of being injected at runtime from a secure secrets store.",
        "body": """<p>Hardcoded secrets are one of the most common causes of security breaches in self-hosted and cloud-hosted applications. When credentials appear in docker-compose.yml, .env files committed to version control, or application config files, they are often accidentally exposed through public repositories, log files, or build artifacts.</p>

<p>The Docker Compose pattern is particularly dangerous because <code>environment:</code> blocks with literal values are frequently committed to public GitHub repositories. GitHub's secret scanning catches some patterns, but custom API keys and database passwords are not always detected.</p>

<h2>What Counts as a Hardcoded Secret</h2>
<p>Direct credential values in <code>environment:</code> blocks (<code>DB_PASSWORD=mypassword</code>). API keys embedded in config files. Private keys committed to repositories. Connection strings with embedded credentials (<code>postgresql://user:password@host/db</code>). Any credential that doesn't use an environment variable reference or secrets manager.</p>

<h2>The Safe Pattern: Variable References</h2>
<p>Use <code>${{DB_PASSWORD}}</code> in docker-compose.yml and define the actual value only in <code>.env</code> files that are listed in <code>.gitignore</code>. For production, use Docker Secrets, HashiCorp Vault, AWS Secrets Manager, or equivalent.</p>""",
        "faqs": [
            ("How do I find hardcoded secrets in my Docker Compose files?", "Paste your docker-compose.yml and .env files into ConfigClarity's Docker Auditor. It scans all environment blocks for literal credential values and flags any that should be environment variable references."),
            ("Is a .env file safe for secrets?", "A .env file is safe if and only if it is listed in .gitignore and never committed to version control. For production, .env files are a transitional solution — proper secrets management uses Docker Secrets, Vault, or a cloud-native secrets store."),
            ("What do I do if I accidentally committed a secret to GitHub?", "Treat the secret as compromised immediately — rotate it before doing anything else. Then remove it from history using git-filter-repo or BFG Repo Cleaner. GitHub's advisory on removing sensitive data covers the exact steps. Removing from history does not protect forks or cached views."),
        ],
        "related_tools": [("Docker Auditor", "/docker/")],
        "related_fixes": [("/fix/docker/hardcoded-secrets/", "Docker hardcoded secrets fix")],
        "tags": ["Security", "Docker", "Secrets Management", "Credentials", "DevOps"],
    },
    {
        "slug": "healthcheck",
        "title": "Docker Healthcheck",
        "short": "A Docker healthcheck is a command defined in a container's configuration that Docker runs periodically to determine if the container is functioning correctly — allowing orchestrators to restart failed containers and delay dependent services.",
        "body": """<p>A Docker healthcheck defines a test command that Docker runs inside the container at a regular interval. If the command exits with a non-zero status code, Docker marks the container as unhealthy. Container orchestrators (Docker Compose, Swarm, Kubernetes) can then take action — restarting the container, stopping dependent services from starting, or routing traffic away from unhealthy instances.</p>

<p>Without a healthcheck, Docker considers a container healthy as soon as it starts. The container may be running but the application inside may not be ready to serve traffic — the web server may still be starting up, the database may be running its initial migration, or a connection pool may not yet be established.</p>

<h2>Healthcheck in docker-compose.yml</h2>
<pre style="background:#0b0d14;padding:1rem;border-radius:6px;font-size:0.78rem;overflow-x:auto;margin:0.75rem 0;">healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s</pre>

<p><code>start_period</code> is the grace period before health failures count against the retry limit — essential for services with slow startup like Java applications or services running database migrations on boot.</p>""",
        "faqs": [
            ("What happens if a container has no healthcheck?", "Docker reports the container status as 'running' regardless of whether the application is functioning. Dependent services start immediately without waiting for the container to be ready. Orchestrators cannot detect application failures — only process crashes."),
            ("What is a good healthcheck command for a web service?", "For HTTP services: <code>[\"CMD\", \"curl\", \"-f\", \"http://localhost:PORT/health\"]</code>. For services without curl: <code>[\"CMD-SHELL\", \"wget -q --spider http://localhost:PORT/health || exit 1\"]</code>. For databases: use the database's own health tool — <code>[\"CMD\", \"pg_isready\", \"-U\", \"postgres\"]</code> for PostgreSQL."),
            ("How do I check if my containers have healthchecks configured?", "Paste your docker-compose.yml into ConfigClarity's Docker Auditor. It flags every service missing a healthcheck definition and generates a suggested healthcheck command based on the detected service type."),
        ],
        "related_tools": [("Docker Auditor", "/docker/")],
        "related_fixes": [("/fix/docker/missing-healthcheck/", "Docker missing healthcheck fix")],
        "tags": ["Docker", "Healthcheck", "Orchestration", "Container", "DevOps"],
    },
    {
        "slug": "nftables",
        "title": "nftables",
        "short": "nftables is the modern Linux firewall framework that replaced iptables as the default in Debian 10+, Ubuntu 20.10+, and RHEL 8+. It provides a unified interface for IPv4, IPv6, and ARP filtering with improved performance and syntax.",
        "body": """<p>nftables is the successor to iptables, ip6tables, arptables, and ebtables — replacing four separate tools with a single framework. It was merged into the Linux kernel in 3.13 (2014) and became the default firewall backend in Debian 10 (Buster, 2019) and Ubuntu 20.10.</p>

<p>The transition from iptables to nftables is largely transparent when using UFW — UFW abstracts both backends. Problems arise when iptables rules are mixed with nftables rules, or when Docker (which uses iptables directly) is running on a system using nftables.</p>

<h2>nftables vs iptables</h2>
<p>iptables uses separate tables (filter, nat, mangle) with separate commands. nftables uses a single <code>nft</code> command with a unified syntax. nftables supports sets (groups of addresses or ports) natively, reducing rule count. nftables has better performance at high rule counts due to kernel-level set operations.</p>

<h2>Docker and nftables Conflict</h2>
<p>Docker uses iptables compatibility mode on nftables systems. This can cause the DOCKER chain in iptables to not interact correctly with nftables rules, leading to UFW-like bypass issues where containers appear protected but are actually accessible. The fix involves explicitly configuring Docker to use the nftables-compatible iptables backend.</p>""",
        "faqs": [
            ("Is nftables better than iptables?", "For new deployments, yes. nftables has cleaner syntax, better performance at scale, native set support, and is actively maintained. For existing setups, migration requires care — Docker, fail2ban, and some VPN software still default to iptables rules that need compatibility configuration."),
            ("How do I check if my system is using nftables or iptables?", "Run <code>sudo nft list ruleset</code>. If it returns rules, nftables is active. Run <code>sudo iptables -L</code> — on nftables systems this uses the iptables-nft compatibility layer. Check <code>dpkg -l nftables iptables</code> to see which packages are installed."),
            ("Does UFW work with nftables?", "Yes. UFW on Ubuntu 20.10+ uses the nftables backend by default. The firewall rules you write with <code>ufw allow/deny</code> are translated to nftables rules. However, Docker's iptables rules may not integrate correctly — see the Docker UFW bypass glossary entry."),
        ],
        "related_tools": [("Firewall Auditor", "/firewall/")],
        "related_fixes": [("/fix/nftables/ubuntu-22/", "nftables Ubuntu 22 fix"), ("/fix/nftables/docker-conflict/", "nftables Docker conflict fix")],
        "tags": ["nftables", "iptables", "Firewall", "Linux", "Networking", "Ubuntu"],
    },
    {
        "slug": "ipv6-mismatch",
        "title": "IPv6 Mismatch",
        "short": "An IPv6 mismatch occurs when firewall rules protect a service on IPv4 but the same port is exposed and unprotected on IPv6, because UFW and iptables rules are not automatically duplicated across address families.",
        "body": """<p>IPv6 mismatch is a silent security gap. UFW manages both IPv4 (iptables) and IPv6 (ip6tables) rules, but they must be explicitly configured. A rule like <code>ufw deny 5432</code> only blocks IPv4 connections to PostgreSQL if the UFW IPv6 backend is not configured. If <code>IPV6=yes</code> is not set in <code>/etc/default/ufw</code>, the IPv6 variant of the rule is not applied.</p>

<p>Many VPS providers (Hetzner, DigitalOcean) assign both IPv4 and IPv6 addresses to servers. A service bound to <code>0.0.0.0</code> (which in many configurations also binds to <code>::</code>) may be accessible over IPv6 even when IPv4 access is blocked.</p>

<h2>How to Check</h2>
<p>Run <code>ufw status verbose</code> and look for IPv6 entries. Each allow/deny rule should appear in both the IPv4 and IPv6 sections. If IPv6 entries are missing, check <code>/etc/default/ufw</code> for <code>IPV6=yes</code>. Also verify with <code>ip6tables -L INPUT</code> — if the chain is empty while UFW is active, IPv6 rules are not being applied.</p>""",
        "faqs": [
            ("How do I enable IPv6 rules in UFW?", "Edit <code>/etc/default/ufw</code> and set <code>IPV6=yes</code>. Then run <code>ufw disable && ufw enable</code> to reload. UFW will now create both iptables and ip6tables rules for every subsequent allow/deny command."),
            ("Does Docker expose ports on IPv6?", "Docker's default bridge network does not expose IPv6 unless explicitly configured with <code>--ipv6</code> in daemon.json. However, services bound to <code>0.0.0.0</code> may also bind to <code>::</code> depending on the Linux kernel's <code>net.ipv6.bindv6only</code> setting."),
            ("How do I detect IPv6 firewall mismatches?", "Paste your <code>ufw status verbose</code> output into ConfigClarity's Firewall Auditor. It compares IPv4 and IPv6 rule parity and flags rules that exist in one address family but not the other."),
        ],
        "related_tools": [("Firewall Auditor", "/firewall/")],
        "related_fixes": [("/fix/ufw/ipv6-mismatch/", "UFW IPv6 mismatch fix")],
        "tags": ["IPv6", "UFW", "Firewall", "iptables", "Networking", "Security"],
    },
    {
        "slug": "dangling-route",
        "title": "Dangling Route",
        "short": "A dangling route is a reverse proxy configuration entry pointing to a backend service that no longer exists — a stopped container, a removed service, or a hostname that no longer resolves — causing 502 or 504 errors.",
        "body": """<p>Dangling routes accumulate over time as services are added, renamed, or removed without updating the reverse proxy configuration. Nginx does not validate that upstream servers exist at startup — it will start successfully even if every defined upstream is unreachable.</p>

<p>In Traefik with Docker labels, dangling routes occur when a container is removed but the Nginx config referencing it was not updated. In static Nginx configurations, they occur when services are moved to different ports or hostnames without updating the <code>proxy_pass</code> directive.</p>

<h2>Impact</h2>
<p>End users see 502 (bad gateway) or 504 (gateway timeout) errors. The reverse proxy server logs are flooded with upstream connection failures. Health check monitors flag the service as down. In some configurations, Traefik will continue attempting connections to removed backends, consuming resources.</p>

<h2>Detection</h2>
<p>ConfigClarity's Reverse Proxy Mapper analyses your nginx.conf or Docker Compose labels, extracts all defined upstream targets, and flags any that don't correspond to a running service definition in the same config file.</p>""",
        "faqs": [
            ("How do dangling routes happen in Docker Compose?", "When a container is removed from docker-compose.yml but the Nginx config in another service still references it via <code>proxy_pass http://removed-service:port</code>. Docker removes the DNS entry for the removed service, but Nginx's config is not automatically updated."),
            ("Will Nginx start with a dangling upstream?", "Yes. Nginx validates config syntax with <code>nginx -t</code> but does not check whether upstream servers are reachable at startup. The error only appears at runtime when a request is made to the dangling route."),
            ("How do I find dangling routes in my Nginx config?", "Paste your nginx.conf into ConfigClarity's Reverse Proxy Mapper. It extracts all <code>proxy_pass</code> targets and cross-references them against the upstream definitions and Docker service names defined in the same config."),
        ],
        "related_tools": [("Reverse Proxy Mapper", "/proxy/")],
        "related_fixes": [("/fix/nginx/502-bad-gateway/", "Nginx 502 fix"), ("/fix/nginx/upstream-timeout/", "Upstream timeout fix")],
        "tags": ["Nginx", "Reverse Proxy", "Traefik", "502", "Routing", "Docker"],
    },
    {
        "slug": "resource-limits",
        "title": "Resource Limits (Docker)",
        "short": "Docker resource limits are configuration directives that cap the CPU and memory a container can consume, preventing a single container from exhausting host resources and causing the entire server to become unresponsive.",
        "body": """<p>Without resource limits, any container can consume all available CPU and memory on the host. A memory leak in one container can OOM-kill other containers or the host kernel. A runaway process in one container can starve all other containers of CPU time.</p>

<p>Resource limits in Docker Compose are defined under the <code>deploy.resources</code> key (Compose v3) or the top-level <code>mem_limit</code>/<code>cpus</code> keys (Compose v2). Compose v3 limits require Docker Swarm mode unless you use the <code>--compatibility</code> flag with docker-compose.</p>

<h2>Memory Limits</h2>
<p>Memory limits prevent OOM conditions. Set both <code>memory</code> (hard limit) and <code>memory_reservation</code> (soft limit). When the hard limit is reached, Docker kills the container with OOM. When the soft limit is reached, Docker throttles memory allocation.</p>

<h2>CPU Limits</h2>
<p><code>cpus: "0.5"</code> limits the container to 50% of one CPU core. <code>cpu_shares</code> is a relative weight — containers with higher shares get more CPU time under contention but are not hard-capped. For consistent limits, prefer <code>cpus</code> over <code>cpu_shares</code>.</p>""",
        "faqs": [
            ("What happens if I don't set memory limits on Docker containers?", "A container with a memory leak or runaway process can consume all available RAM on the host. The Linux OOM killer will then terminate processes — often killing other containers or system services rather than the container at fault."),
            ("How do I set resource limits in docker-compose.yml?", "In Compose v3 with Swarm: use <code>deploy.resources.limits</code>. Without Swarm, use the Compose v2 format: <code>mem_limit: 512m</code> and <code>cpus: '0.5'</code> at the service level. ConfigClarity's Docker Auditor flags services with no resource limits defined."),
            ("What is a good starting memory limit for a web service?", "Start conservative — 256m to 512m for small services, 1g to 2g for larger applications. Monitor with <code>docker stats</code> under normal load and adjust. The OOM risk of setting limits too low is lower than the availability risk of not setting them."),
        ],
        "related_tools": [("Docker Auditor", "/docker/")],
        "related_fixes": [("/fix/docker/resource-limits/", "Docker resource limits fix")],
        "tags": ["Docker", "Resource Limits", "Memory", "CPU", "OOM", "Container", "DevOps"],
    },
    {
        "slug": "log-overflow",
        "title": "Log Overflow",
        "short": "Log overflow occurs when container or application logs grow without bound, filling the host disk and causing the server and all containers to fail when the filesystem reaches 100% capacity.",
        "body": """<p>Docker stores container logs in JSON files on the host at <code>/var/lib/docker/containers/CONTAINER_ID/CONTAINER_ID-json.log</code>. Without log rotation configured, verbose containers (web servers, databases) can fill the host disk within days or weeks.</p>

<p>When the host disk hits 100%, writes fail silently across all containers. The symptoms are non-obvious: cron jobs appear to run but write nothing, application errors increase, containers restart unexpectedly. The root cause — a full disk — is often discovered late.</p>

<h2>Docker Log Rotation Options</h2>
<p>The <code>json-file</code> logging driver (default) supports <code>max-size</code> and <code>max-file</code> options. Setting <code>max-size: "10m"</code> and <code>max-file: "3"</code> keeps at most 30MB of logs per container. This can be set globally in <code>/etc/docker/daemon.json</code> or per-service in docker-compose.yml under the <code>logging</code> key.</p>

<h2>Checking Disk Usage</h2>
<p>Run <code>docker system df</code> to see Docker's total disk usage. Run <code>du -sh /var/lib/docker/containers/*/</code> to see per-container log sizes. A single misbehaving container can account for gigabytes of logs.</p>""",
        "faqs": [
            ("How do I prevent Docker log files from filling my disk?", "Set log rotation in /etc/docker/daemon.json: <code>{\"log-driver\": \"json-file\", \"log-opts\": {\"max-size\": \"10m\", \"max-file\": \"3\"}}</code>. This applies to all containers globally. Or set per-service in docker-compose.yml under the <code>logging:</code> key."),
            ("How do I clear existing Docker logs without deleting containers?", "Truncate the log file: <code>sudo truncate -s 0 /var/lib/docker/containers/CONTAINER_ID/CONTAINER_ID-json.log</code>. Or run <code>docker system prune</code> to remove stopped containers and their logs. Running containers' logs can only be truncated, not deleted."),
            ("What is the best Docker logging driver for production?", "For self-hosted setups with disk space concerns: <code>json-file</code> with rotation limits is simplest. For centralized log collection: <code>loki</code> (with Grafana Loki) or <code>syslog</code>. For AWS deployments: <code>awslogs</code>. Avoid <code>none</code> — it discards all logs, making debugging impossible."),
        ],
        "related_tools": [("Docker Auditor", "/docker/")],
        "related_fixes": [("/fix/docker/log-overflow/", "Docker log overflow fix")],
        "tags": ["Docker", "Logging", "Disk Space", "Log Rotation", "DevOps"],
    },
]

# ─── BUILDER FUNCTIONS ─────────────────────────────────────────────────────────

def build_term_page(term):
    slug = term["slug"]
    title = term["title"]
    short = term["short"]
    related_tool_links = "".join([
        f'<a href="{url}">{name} →</a>'
        for name, url in term["related_tools"]
    ])
    related_fix_links = "".join([
        f'<a href="{url}">{label}</a>'
        for url, label in term["related_fixes"]
    ])
    tags_html = "".join([f'<span class="tag">{t}</span>' for t in term["tags"]])

    faq_schema_items = ",\n".join([
        f'{{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}'
        for q, a in term["faqs"]
    ])
    faq_html = "\n".join([
        f'''<div class="faq-item">
        <div class="faq-q">{q}</div>
        <div class="faq-a">{a}</div>
      </div>'''
        for q, a in term["faqs"]
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — DevOps Glossary — ConfigClarity</title>
  <meta name="description" content="{short}">
  <meta name="keywords" content="{", ".join(term["tags"]).lower()}, linux server, devops glossary">
  <link rel="canonical" href="https://configclarity.dev/glossary/{slug}/">
  <meta property="og:title" content="{title} — ConfigClarity Glossary">
  <meta property="og:description" content="{short}">
  <meta property="og:url" content="https://configclarity.dev/glossary/{slug}/">
  {FONT}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "DefinedTerm",
    "name": "{title}",
    "url": "https://configclarity.dev/glossary/{slug}/",
    "description": "{short}",
    "inDefinedTermSet": {{
      "@type": "DefinedTermSet",
      "name": "ConfigClarity DevOps Glossary",
      "url": "https://configclarity.dev/glossary/"
    }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{faq_schema_items}]
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Glossary","item":"https://configclarity.dev/glossary/"}},
    {{"@type":"ListItem","position":3,"name":"{title}","item":"https://configclarity.dev/glossary/{slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/glossary/">Glossary</a> › {title}
  </div>
  <div class="content">
    <h1>{title}</h1>
    <div class="definition-box">{short}</div>
    <div>{tags_html}</div>
    {term["body"]}
    <h2>Related Tools</h2>
    <div class="related-links">{related_tool_links}</div>
    <h2>Fix Guides</h2>
    <div class="related-links">{related_fix_links}</div>
    <h2>Frequently Asked Questions</h2>
    {faq_html}
  </div>
{FOOTER}
</body>
</html>"""

def build_glossary_index():
    cards = "\n".join([
        f'''    <a href="/glossary/{t["slug"]}/" class="card" style="display:block;">
      <div class="card-title">{t["title"]}</div>
      <div class="card-desc">{t["short"][:100]}...</div>
    </a>'''
        for t in TERMS
    ])

    term_list_items = ",\n".join([
        f'{{"@type":"ListItem","position":{i+1},"url":"https://configclarity.dev/glossary/{t["slug"]}/","name":"{t["title"]}"}}'
        for i, t in enumerate(TERMS)
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevOps & Linux Server Glossary — ConfigClarity</title>
  <meta name="description" content="Definitions for Docker UFW bypass, port binding, SSL certificate expiry, cron job collision, flock safety, reverse proxy, Traefik labels, nftables, and more DevOps terms.">
  <meta name="keywords" content="devops glossary, linux server terms, docker ufw bypass definition, flock safety, reverse proxy definition, ssl certificate expiry">
  <link rel="canonical" href="https://configclarity.dev/glossary/">
  <meta property="og:title" content="DevOps & Linux Server Glossary — ConfigClarity">
  <meta property="og:description" content="Definitions for common Linux server and Docker terms — with fix guides for each issue.">
  <meta property="og:url" content="https://configclarity.dev/glossary/">
  {FONT}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "DefinedTermSet",
    "name": "ConfigClarity DevOps & Linux Server Glossary",
    "url": "https://configclarity.dev/glossary/",
    "description": "Definitions for Docker, UFW, Nginx, SSL, cron, and reverse proxy terms — with exact fix guides.",
    "hasPart": [{term_list_items}]
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"ItemList",
    "name":"ConfigClarity Glossary Terms",
    "itemListElement":[{term_list_items}]
  }}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › Glossary</div>
  <div class="content">
    <h1>DevOps &amp; Linux Server Glossary</h1>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:2rem;">Definitions for Docker, UFW, SSL, cron, and reverse proxy terms — written for sysadmins, not academics. Each term links to the relevant fix guide and ConfigClarity tool.</p>
  </div>
  <div class="grid" style="max-width:900px;margin:0 auto;padding:0 2rem 3rem;">
{cards}
  </div>
{FOOTER}
</body>
</html>"""

if __name__ == '__main__':
    print("=== Building Glossary Pages ===\n")
    os.makedirs("glossary", exist_ok=True)

    # Index
    idx = build_glossary_index()
    with open("glossary/index.html", "w") as f:
        f.write(idx)
    print(f"  ✅ glossary/index.html ({len(idx):,} bytes)")

    # Term pages
    for term in TERMS:
        path = f"glossary/{term['slug']}/index.html"
        os.makedirs(f"glossary/{term['slug']}", exist_ok=True)
        html = build_term_page(term)
        with open(path, "w") as f:
            f.write(html)
        print(f"  ✅ {path} ({len(html):,} bytes)")

    print(f"\nDone. {1 + len(TERMS)} glossary pages built.")
