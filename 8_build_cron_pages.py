#!/usr/bin/env python3
"""
Script 8: Build Cron expression SEO pages (23 pages).
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
      h1 { font-size:1.6rem; font-weight:700; margin-bottom:0.75rem; }
      h2 { font-size:1.05rem; font-weight:700; margin:2rem 0 0.6rem; }
      p { font-size:0.875rem; color:var(--muted); margin-bottom:1rem; }
      .expr-hero { background:var(--bg2); border:1px solid #2a2d3d; border-radius:8px; padding:1.5rem 2rem; margin:1.25rem 0 2rem; text-align:center; }
      .expr-code { font-size:1.8rem; font-weight:700; color:var(--purple); letter-spacing:0.1em; display:block; margin-bottom:0.5rem; }
      .expr-meaning { font-size:0.9rem; color:var(--text); }
      .field-table { width:100%; border-collapse:collapse; font-size:0.82rem; margin:1rem 0 1.5rem; }
      .field-table th { text-align:left; padding:0.5rem 0.75rem; color:var(--muted); font-weight:600; border-bottom:1px solid #2a2d3d; }
      .field-table td { padding:0.5rem 0.75rem; border-bottom:1px solid #1a1c26; }
      .field-table td:first-child { color:var(--purple); font-weight:700; }
      .field-table tr.active td { color:var(--text); }
      pre { background:#0d0f1a; border:1px solid #2a2d3d; border-radius:8px; padding:1rem 1.25rem; font-size:0.78rem; overflow-x:auto; margin:0.75rem 0 1.25rem; line-height:1.7; }
      .variants { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:0.75rem; margin:1rem 0 1.5rem; }
      .variant-card { background:var(--bg2); border:1px solid #2a2d3d; border-radius:6px; padding:0.85rem 1rem; }
      .variant-expr { font-size:0.9rem; font-weight:700; color:var(--purple); }
      .variant-desc { font-size:0.75rem; color:var(--muted); margin-top:0.25rem; }
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
    <p><a href="/fix/cron/">Cron Fix Guides</a> &nbsp;·&nbsp; <a href="/glossary/cron-job-collision/">Cron Job Collision</a> &nbsp;·&nbsp;
    <a href="https://metriclogic.dev">MetricLogic</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>"""

# ── CRON EXPRESSION PAGES ─────────────────────────────────────────────────────
# Each entry: (slug, expression, meaning, fields, use_cases, variants, faqs)

CRON_EXPRESSIONS = [
    {
        "slug": "every-minute",
        "expr": "* * * * *",
        "meaning": "Run every minute",
        "meta_desc": "Cron expression * * * * * runs a command every minute of every hour, every day. Use cases, risks, and safer alternatives.",
        "keywords": "cron every minute, * * * * * cron, cron expression every minute",
        "fields": [("*","minute","every minute"),("*","hour","every hour"),("*","day","every day"),("*","month","every month"),("*","weekday","every weekday")],
        "body": """<p>Running a cron job every minute is rarely necessary and carries real risk. If the job takes more than 60 seconds, a second instance starts before the first finishes. Without flock safety, both run simultaneously — competing for the same resources or processing the same data twice.</p>
<h2>Use flock for every-minute jobs</h2>
<pre>* * * * * flock -n /tmp/myjob.lock /usr/local/bin/myjob.sh</pre>
<p>If the job is still running when the next minute fires, the new invocation exits immediately without running.</p>""",
        "variants": [
            ("*/2 * * * *", "Every 2 minutes"),
            ("*/5 * * * *", "Every 5 minutes"),
            ("*/10 * * * *", "Every 10 minutes"),
            ("*/15 * * * *", "Every 15 minutes"),
            ("*/30 * * * *", "Every 30 minutes"),
        ],
        "use_cases": ["Health check polling", "Log tail processing", "Real-time queue drain (use a queue instead)", "Metric collection"],
        "faqs": [
            ("Is * * * * * the most frequent cron can run?", "Yes. Cron's minimum resolution is one minute. For sub-minute scheduling, use a process manager like systemd timers with AccuracySec=1s, or a dedicated job queue like Sidekiq or Celery."),
            ("Why does my every-minute job sometimes run twice?", "If the job takes over 60 seconds and you don't have flock safety, a second instance starts before the first finishes. Wrap with flock -n /tmp/job.lock to prevent concurrent runs."),
        ],
    },
    {
        "slug": "every-5-minutes",
        "expr": "*/5 * * * *",
        "meaning": "Run every 5 minutes",
        "meta_desc": "Cron expression */5 * * * * runs a job every 5 minutes. Breakdown, use cases, flock safety, and related expressions.",
        "keywords": "cron every 5 minutes, */5 * * * * cron meaning, cron expression 5 minutes",
        "fields": [("*/5","minute","every 5 minutes (0,5,10,15...)"),("*","hour","every hour"),("*","day","every day"),("*","month","every month"),("*","weekday","every weekday")],
        "body": """<p>The <code>*/5</code> syntax means "every 5th value" — so <code>*/5</code> in the minute field fires at minutes 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, and 55 of every hour. It does not mean "5 minutes after the last run". If the job starts at 00:00 and takes 8 minutes, the next invocation fires at 00:05 regardless.</p>
<h2>Combining with flock</h2>
<pre>*/5 * * * * flock -n /tmp/sync.lock /usr/local/bin/sync.sh</pre>""",
        "variants": [
            ("*/2 * * * *", "Every 2 minutes"),
            ("*/3 * * * *", "Every 3 minutes"),
            ("*/10 * * * *", "Every 10 minutes"),
            ("*/15 * * * *", "Every 15 minutes"),
            ("1-59/5 * * * *", "Every 5 min starting at :01"),
        ],
        "use_cases": ["Cache warming", "RSS feed polling", "Metrics collection", "Webhook retries"],
        "faqs": [
            ("What does */5 mean in a cron expression?", "*/5 means 'every 5th value of the field's range'. In the minute field, the range is 0-59, so */5 fires at 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, and 55 of every hour."),
            ("Does */5 start exactly 5 minutes after the last run?", "No. */5 fires at fixed points in the minute field (0, 5, 10...) regardless of when the previous run completed. If you need exactly 5 minutes between runs, use a service manager with a delay loop, not cron."),
        ],
    },
    {
        "slug": "every-hour",
        "expr": "0 * * * *",
        "meaning": "Run at the start of every hour",
        "meta_desc": "Cron expression 0 * * * * runs a job at minute 0 of every hour (top of the hour). Breakdown, use cases, and variants.",
        "keywords": "cron every hour, 0 * * * * cron, cron expression hourly, cron top of hour",
        "fields": [("0","minute","at minute 0 (top of the hour)"),("*","hour","every hour"),("*","day","every day"),("*","month","every month"),("*","weekday","every weekday")],
        "body": """<p>Running jobs at <code>0 * * * *</code> (top of the hour) is one of the most common cron patterns. It's also one of the most common causes of server load spikes — because every sysadmin defaults to this expression, dozens of jobs pile up at :00.</p>
<h2>Spread top-of-hour jobs</h2>
<pre># Instead of all at :00, stagger them:
0 * * * *  /usr/local/bin/job-a.sh
5 * * * *  /usr/local/bin/job-b.sh
15 * * * * /usr/local/bin/job-c.sh
25 * * * * /usr/local/bin/job-d.sh</pre>""",
        "variants": [
            ("0 * * * *", "Every hour at :00"),
            ("30 * * * *", "Every hour at :30"),
            ("15 * * * *", "Every hour at :15"),
            ("0 */2 * * *", "Every 2 hours"),
            ("0 */6 * * *", "Every 6 hours"),
        ],
        "use_cases": ["Cache invalidation", "Report generation", "Log rotation triggers", "Uptime checks"],
        "faqs": [
            ("What is the difference between 0 * * * * and */60 * * * *?", "*/60 is technically invalid — the minute field range is 0-59, so */60 only matches minute 0 (since 60 doesn't exist) and behaves like 0 * * * *. Use 0 * * * * explicitly to be clear."),
            ("How do I run a job every hour but not on the hour?", "Use a specific minute offset: 15 * * * * runs at :15 past every hour. 45 * * * * runs at :45 past every hour. Offsetting from :00 reduces load concentration."),
        ],
    },
    {
        "slug": "every-day-midnight",
        "expr": "0 0 * * *",
        "meaning": "Run once a day at midnight",
        "meta_desc": "Cron expression 0 0 * * * runs a job at midnight every day. Breakdown, timezone considerations, and load spike avoidance.",
        "keywords": "cron every day midnight, 0 0 * * * cron, cron midnight daily, cron daily at midnight",
        "fields": [("0","minute","at minute 0"),("0","hour","at hour 0 (midnight)"),("*","day","every day"),("*","month","every month"),("*","weekday","every weekday")],
        "body": """<p>Midnight is the most overloaded minute in any server's cron schedule. Backups, cleanups, reports, cache clears — they all default to <code>0 0 * * *</code>. A server with five midnight jobs experiences a simultaneous I/O and CPU spike at 00:00 every night.</p>
<h2>The load spike fix</h2>
<pre># Spread midnight jobs across 30 minutes:
0  0 * * * flock -n /tmp/backup.lock    /usr/local/bin/backup.sh
5  0 * * * flock -n /tmp/cleanup.lock   /usr/local/bin/cleanup.sh
15 0 * * * flock -n /tmp/report.lock    /usr/local/bin/report.sh
25 0 * * * flock -n /tmp/db-dump.lock   /usr/local/bin/db-dump.sh</pre>
<h2>Timezone note</h2>
<p>Cron runs in the server's local timezone. If your server is UTC and your users are in a different timezone, "midnight" may not be the quiet window you expect. Check with <code>timedatectl</code>.</p>""",
        "variants": [
            ("0 0 * * *", "Midnight every day"),
            ("0 1 * * *", "1am every day"),
            ("0 2 * * *", "2am every day (common for backups)"),
            ("0 0 * * 0", "Midnight every Sunday"),
            ("30 23 * * *", "11:30pm every day"),
        ],
        "use_cases": ["Daily database backups", "Log archival", "Report generation", "Cache warming", "Cleanup jobs"],
        "faqs": [
            ("Why do all my cron jobs run at midnight?", "It's the most common default. When setting up a job without a specific time requirement, developers choose 0 0 * * *. When multiple jobs pile up at the same minute, the server CPU and disk I/O spike simultaneously. Stagger jobs by at least 5 minutes."),
            ("How do I run a cron job at a random time around midnight?", "Cron doesn't support randomisation natively. Use: 0 0 * * * sleep $((RANDOM % 1800)) && /path/to/script.sh to add a random 0–30 minute delay. This spreads load across servers in a fleet."),
        ],
    },
    {
        "slug": "every-monday",
        "expr": "0 9 * * 1",
        "meaning": "Run every Monday at 9am",
        "meta_desc": "Cron expression 0 9 * * 1 runs a job every Monday at 9am. Weekday numbering, timezone notes, and weekly cron patterns.",
        "keywords": "cron every monday, 0 9 * * 1 cron, cron weekly monday, cron expression weekday",
        "fields": [("0","minute","at minute 0"),("9","hour","at 9am"),("*","day","any day of month"),("*","month","every month"),("1","weekday","Monday (0=Sun, 1=Mon...7=Sun)")],
        "body": """<p>Weekday values in cron: 0 = Sunday, 1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday (7 is also valid for Sunday in most cron implementations).</p>
<h2>Weekly patterns</h2>
<pre># Monday 9am:
0 9 * * 1

# Weekdays (Mon-Fri) at 8am:
0 8 * * 1-5

# Weekend midnight:
0 0 * * 6,0

# Every weekday at noon:
0 12 * * 1-5</pre>""",
        "variants": [
            ("0 9 * * 1", "Every Monday 9am"),
            ("0 9 * * 1-5", "Every weekday 9am"),
            ("0 0 * * 1", "Every Monday midnight"),
            ("0 9 * * 5", "Every Friday 9am"),
            ("0 9 * * 0", "Every Sunday 9am"),
        ],
        "use_cases": ["Weekly reports", "Monday morning data syncs", "Weekly cleanup jobs", "Scheduled email digests"],
        "faqs": [
            ("What is the weekday numbering in cron?", "0 = Sunday, 1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday (both 0 and 7 represent Sunday for compatibility)."),
            ("What does 1-5 mean in the weekday field?", "1-5 means Monday through Friday — a range of weekday values. Combined with specific hours: 0 9 * * 1-5 runs at 9am on every weekday."),
        ],
    },
    {
        "slug": "first-day-of-month",
        "expr": "0 0 1 * *",
        "meaning": "Run on the 1st of every month at midnight",
        "meta_desc": "Cron expression 0 0 1 * * runs a job on the first day of every month at midnight. Monthly cron patterns and last-day-of-month workarounds.",
        "keywords": "cron first day of month, 0 0 1 * * cron, cron monthly first day, cron expression monthly",
        "fields": [("0","minute","at minute 0"),("0","hour","at midnight"),("1","day","on the 1st of the month"),("*","month","every month"),("*","weekday","any weekday")],
        "body": """<p>The day-of-month field runs from 1 to 31. Using <code>1</code> runs on the 1st of every month. Cron has no built-in way to run on the last day of the month, since months have different lengths.</p>
<h2>Last day of month workaround</h2>
<pre># Run on 28th — safe for all months:
0 0 28 * *

# Or: check if tomorrow is the 1st (run on last day):
0 23 * * * [ "$(date -d tomorrow +%d)" = "01" ] && /usr/local/bin/month-end.sh</pre>""",
        "variants": [
            ("0 0 1 * *", "1st of every month"),
            ("0 0 15 * *", "15th of every month"),
            ("0 0 1 */3 *", "1st of every quarter"),
            ("0 0 1 1 *", "January 1st every year"),
            ("0 0 28 * *", "28th of every month (safe last-week job)"),
        ],
        "use_cases": ["Monthly billing runs", "End-of-month reports", "Monthly archive jobs", "Subscription renewals"],
        "faqs": [
            ("How do I run a cron job on the last day of the month?", "Cron can't calculate the last day natively. The standard workaround is to check if tomorrow is the 1st: 0 23 * * * [ \"$(date -d tomorrow +%d)\" = \"01\" ] && /your/script.sh. On macOS use date -v+1d +%d instead."),
            ("What happens if I use 31 in the day-of-month field?", "The job only runs in months that have 31 days (January, March, May, July, August, October, December). It silently skips months with fewer days — no error, just no execution."),
        ],
    },
    {
        "slug": "every-weekday",
        "expr": "0 9 * * 1-5",
        "meaning": "Run every weekday (Mon–Fri) at 9am",
        "meta_desc": "Cron expression 0 9 * * 1-5 runs a job every weekday Monday through Friday at 9am. Weekday range syntax and business hours cron patterns.",
        "keywords": "cron every weekday, 0 9 * * 1-5 cron, cron business hours, cron monday friday",
        "fields": [("0","minute","at minute 0"),("9","hour","at 9am"),("*","day","any day of month"),("*","month","every month"),("1-5","weekday","Monday through Friday")],
        "body": """<p>The range syntax <code>1-5</code> in the weekday field means "Monday through Friday". This is one of the most useful cron patterns for business-hours tasks.</p>
<h2>Business hours patterns</h2>
<pre># Every weekday at 9am:
0 9 * * 1-5

# Every hour during business hours, weekdays:
0 9-17 * * 1-5

# Every 30 minutes, business hours, weekdays:
*/30 9-17 * * 1-5

# Weekdays at 6am (before work):
0 6 * * 1-5</pre>""",
        "variants": [
            ("0 9 * * 1-5", "Weekdays at 9am"),
            ("0 17 * * 1-5", "Weekdays at 5pm"),
            ("0 9-17 * * 1-5", "Top of every business hour"),
            ("0 6 * * 1-5", "Weekdays 6am (pre-work)"),
            ("0 0 * * 6,0", "Weekends at midnight"),
        ],
        "use_cases": ["Business report generation", "Weekday data syncs", "Morning digests", "End-of-day summaries"],
        "faqs": [
            ("Can I combine day-of-month and day-of-week in cron?", "Yes, but cron treats them as OR, not AND. If you set both a day-of-month value and a day-of-week value (both non-*), the job runs when EITHER condition is true. To get AND behaviour, use a shell condition inside the script."),
            ("How do I skip public holidays in cron?", "Cron has no concept of public holidays. The standard approach is to check a holiday list inside the script: if grep -q \"$(date +%Y-%m-%d)\" /etc/holidays.txt; then exit 0; fi at the start of your script."),
        ],
    },
    {
        "slug": "twice-a-day",
        "expr": "0 9,17 * * *",
        "meaning": "Run twice a day at 9am and 5pm",
        "meta_desc": "Cron expression 0 9,17 * * * runs a job twice a day at 9am and 5pm. List syntax in cron expressions and twice-daily scheduling patterns.",
        "keywords": "cron twice a day, 0 9 17 * * * cron, cron twice daily, cron list syntax",
        "fields": [("0","minute","at minute 0"),("9,17","hour","at 9am AND 5pm (list)"),("*","day","every day"),("*","month","every month"),("*","weekday","every weekday")],
        "body": """<p>Comma-separated values in any field create a list — the job runs when the field matches any value in the list. <code>9,17</code> in the hour field means "at hour 9 OR hour 17".</p>
<h2>List syntax examples</h2>
<pre># Twice daily at 9am and 5pm:
0 9,17 * * *

# Three times daily:
0 6,12,18 * * *

# Specific days of week:
0 9 * * 1,3,5   # Mon, Wed, Fri at 9am

# Multiple minutes:
0,30 * * * *    # Top and bottom of every hour</pre>""",
        "variants": [
            ("0 9,17 * * *", "9am and 5pm daily"),
            ("0 6,12,18 * * *", "6am, noon, 6pm"),
            ("0 8,20 * * *", "8am and 8pm"),
            ("0 0,12 * * *", "Midnight and noon"),
            ("0 9,17 * * 1-5", "9am and 5pm weekdays only"),
        ],
        "use_cases": ["Twice-daily backups", "Morning and evening reports", "Cache refresh cycles", "API rate-limited sync jobs"],
        "faqs": [
            ("What is the list syntax in cron?", "Comma-separated values in any cron field create a list of specific values to match. 9,17 in the hour field matches hours 9 and 17. 1,3,5 in the weekday field matches Monday, Wednesday, and Friday."),
            ("Can I mix list and range syntax in cron?", "Yes. 1-5,0 in the weekday field means Monday through Friday plus Sunday. 0,30 * * * * runs at the top and bottom of every hour. You can combine ranges, lists, and step values in the same field."),
        ],
    },
    {
        "slug": "every-15-minutes",
        "expr": "*/15 * * * *",
        "meaning": "Run every 15 minutes",
        "meta_desc": "Cron expression */15 * * * * runs a job every 15 minutes. Fires at :00, :15, :30, :45 of every hour. Step syntax and use cases.",
        "keywords": "cron every 15 minutes, */15 * * * * cron meaning, cron 15 minute interval",
        "fields": [("*/15","minute","every 15 minutes (0,15,30,45)"),("*","hour","every hour"),("*","day","every day"),("*","month","every month"),("*","weekday","every weekday")],
        "body": """<p><code>*/15</code> fires at minutes 0, 15, 30, and 45 of every hour — four times per hour, 96 times per day. It's one of the most common intervals for health checks, polling jobs, and cache warming.</p>
<pre># With flock to prevent overlap:
*/15 * * * * flock -n /tmp/check.lock /usr/local/bin/health-check.sh</pre>""",
        "variants": [
            ("*/15 * * * *", "Every 15 minutes"),
            ("*/10 * * * *", "Every 10 minutes"),
            ("*/20 * * * *", "Every 20 minutes"),
            ("*/30 * * * *", "Every 30 minutes"),
            ("5,20,35,50 * * * *", "Every 15 min starting at :05"),
        ],
        "use_cases": ["Health checks", "Certificate expiry monitoring", "Queue depth checks", "API sync jobs"],
        "faqs": [
            ("Does */15 always start at minute 0?", "Yes. */15 fires at minutes 0, 15, 30, and 45 — these are fixed points relative to the hour, not 15 minutes after the job last ran. To start at a different minute, use a list: 5,20,35,50 * * * *."),
            ("How many times does */15 run per day?", "4 times per hour × 24 hours = 96 times per day."),
        ],
    },
    {
        "slug": "reboot",
        "expr": "@reboot",
        "meaning": "Run once when the system starts up",
        "meta_desc": "Cron @reboot special string runs a command once when the system starts. Timing issues, startup delays, and how to handle service dependencies.",
        "keywords": "cron reboot, @reboot cron, cron on startup, cron at boot linux",
        "fields": [("@reboot","special","runs once at system startup — no other fields")],
        "body": """<p><code>@reboot</code> runs the command once when the cron daemon starts, which is typically at system boot. Unlike regular cron jobs, it has no fields — just <code>@reboot command</code>.</p>
<h2>The startup timing problem</h2>
<p>@reboot jobs run early in the boot process. Network may not be up, databases may not be ready, mounted drives may not be accessible yet. Add a sleep to let services settle:</p>
<pre># Wait 30 seconds for services to start:
@reboot sleep 30 && /usr/local/bin/start-app.sh

# Wait for PostgreSQL specifically:
@reboot sleep 10 && until pg_isready -h localhost; do sleep 2; done && /usr/local/bin/start-app.sh</pre>
<h2>systemd is usually better for boot services</h2>
<p>For services that need to start on boot with proper dependency handling, systemd service units are more reliable than @reboot cron. @reboot is fine for simple one-off scripts.</p>""",
        "variants": [
            ("@reboot", "At system startup"),
            ("@reboot sleep 30 && cmd", "At startup with 30s delay"),
            ("@hourly", "= 0 * * * *"),
            ("@daily", "= 0 0 * * *"),
            ("@weekly", "= 0 0 * * 0"),
            ("@monthly", "= 0 0 1 * *"),
        ],
        "use_cases": ["Start background services", "Mount drives", "Restore iptables rules", "Start tunnels or VPN connections"],
        "faqs": [
            ("Does @reboot run on every boot or just once ever?", "Every boot. @reboot runs each time the cron daemon starts, which happens on every system startup. It is not a one-time job."),
            ("What user does @reboot run as?", "@reboot in a user's crontab (crontab -e) runs as that user. @reboot in /etc/crontab or /etc/cron.d/ runs as the user specified in the username field."),
        ],
    },
    {
        "slug": "every-sunday-2am",
        "expr": "0 2 * * 0",
        "meaning": "Run every Sunday at 2am",
        "meta_desc": "Cron expression 0 2 * * 0 runs a job every Sunday at 2am. Weekly maintenance window scheduling and Sunday cron patterns.",
        "keywords": "cron every sunday, 0 2 * * 0 cron, cron weekly maintenance, cron sunday 2am",
        "fields": [("0","minute","at minute 0"),("2","hour","at 2am"),("*","day","any day"),("*","month","every month"),("0","weekday","Sunday (0 or 7)")],
        "body": """<p>Sunday 2am is the classic maintenance window — low traffic, full week ahead to monitor the results. This pattern is commonly used for weekly database maintenance, full system backups, and OS update runs.</p>
<pre># Weekly full backup, Sunday 2am:
0 2 * * 0 flock -n /tmp/weekly-backup.lock /usr/local/bin/full-backup.sh

# Weekly vacuum on PostgreSQL:
0 2 * * 0 psql -U postgres -c "VACUUM ANALYZE;"

# Weekly OS security updates (unattended):
0 2 * * 0 /usr/bin/unattended-upgrade</pre>""",
        "variants": [
            ("0 2 * * 0", "Sunday 2am"),
            ("0 2 * * 6", "Saturday 2am"),
            ("0 3 * * 0", "Sunday 3am"),
            ("0 2 * * 0,6", "Weekend 2am"),
            ("0 2 * * 7", "Sunday 2am (7 also = Sunday)"),
        ],
        "use_cases": ["Weekly full backups", "Database VACUUM/ANALYZE", "Log archive and rotation", "OS security updates", "Weekly reports"],
        "faqs": [
            ("Is 0 in the weekday field Sunday or Monday?", "0 is Sunday. The weekday numbering is: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday, 7=Sunday (7 is also accepted as Sunday for compatibility)."),
            ("Why is 2am the standard maintenance window?", "2am is typically the lowest traffic window for sites serving US and European timezones. It also gives time for maintenance to complete before business hours. For Asia-Pacific primary audiences, adjust to local off-peak hours."),
        ],
    },
    {
        "slug": "every-6-hours",
        "expr": "0 */6 * * *",
        "meaning": "Run every 6 hours",
        "meta_desc": "Cron expression 0 */6 * * * runs a job every 6 hours at midnight, 6am, noon, and 6pm. Six-hour interval cron patterns.",
        "keywords": "cron every 6 hours, 0 */6 * * * cron, cron four times a day, cron every six hours",
        "fields": [("0","minute","at minute 0"),("*/6","hour","every 6 hours (0,6,12,18)"),("*","day","every day"),("*","month","every month"),("*","weekday","every weekday")],
        "body": """<p><code>*/6</code> in the hour field fires at hours 0, 6, 12, and 18 — four times per day. Combined with minute 0, the job runs at midnight, 6am, noon, and 6pm.</p>
<pre># Every 6 hours:
0 */6 * * *

# Offset to avoid the midnight pile-up:
30 1,7,13,19 * * *   # 1:30am, 7:30am, 1:30pm, 7:30pm</pre>""",
        "variants": [
            ("0 */6 * * *", "Every 6 hours at :00"),
            ("0 */4 * * *", "Every 4 hours (6x/day)"),
            ("0 */8 * * *", "Every 8 hours (3x/day)"),
            ("0 */12 * * *", "Every 12 hours (2x/day)"),
            ("30 */6 * * *", "Every 6 hours at :30"),
        ],
        "use_cases": ["Incremental backups", "Data syncs", "Cache refresh", "Certificate pre-checks", "Remote config pulls"],
        "faqs": [
            ("What times does 0 */6 * * * run?", "It fires at 00:00, 06:00, 12:00, and 18:00 every day — four times per day, 6 hours apart."),
            ("How do I offset a 6-hourly job away from midnight?", "Use an explicit hour list with an offset minute: 30 1,7,13,19 * * * runs at 01:30, 07:30, 13:30, and 19:30 — same 6-hour interval but avoiding the midnight load spike."),
        ],
    },
]

def build_cron_expr_page(item):
    slug = item["slug"]
    expr = item["expr"]
    meaning = item["meaning"]

    # Field table
    fields_html = "\n".join([
        f'<tr class="active"><td>{v}</td><td>{f}</td><td>{d}</td></tr>'
        for v, f, d in item["fields"]
    ])

    # Variants
    variants_html = "\n".join([
        f'<div class="variant-card"><div class="variant-expr">{e}</div><div class="variant-desc">{d}</div></div>'
        for e, d in item["variants"]
    ])

    # Use cases
    uses_html = "\n".join([f"<li>{u}</li>" for u in item["use_cases"]])

    # FAQs
    faq_schema = ",\n".join([
        f'{{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}'
        for q, a in item["faqs"]
    ])
    faq_html = "\n".join([
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q, a in item["faqs"]
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Cron Expression: {expr} — {meaning} — ConfigClarity</title>
  <meta name="description" content="{item['meta_desc']}">
  <meta name="keywords" content="{item['keywords']}">
  <link rel="canonical" href="{BASE}/cron/{slug}/">
  <meta property="og:title" content="Cron {expr} — {meaning}">
  <meta property="og:description" content="{item['meta_desc']}">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle",
    "headline":"Cron Expression: {expr} — {meaning}",
    "url":"{BASE}/cron/{slug}/",
    "description":"{item['meta_desc']}",
    "author":{{"@type":"Organization","name":"MetricLogic"}},
    "datePublished":"{TODAY}"}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"{BASE}"}},
    {{"@type":"ListItem","position":2,"name":"Cron Visualiser","item":"{BASE}/"}},
    {{"@type":"ListItem","position":3,"name":"Cron Expressions","item":"{BASE}/cron/"}},
    {{"@type":"ListItem","position":4,"name":"{meaning}","item":"{BASE}/cron/{slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/cron/">Cron Expressions</a> › {meaning}
  </div>
  <div class="content">
    <h1>Cron Expression: {expr}</h1>
    <div class="expr-hero">
      <span class="expr-code">{expr}</span>
      <span class="expr-meaning">{meaning}</span>
    </div>

    <h2>Field Breakdown</h2>
    <table class="field-table">
      <tr><th>Value</th><th>Field</th><th>Meaning</th></tr>
      {fields_html}
    </table>

    {item["body"]}

    <h2>Related Expressions</h2>
    <div class="variants">{variants_html}</div>

    <h2>Common Use Cases</h2>
    <ul style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.2;">{uses_html}</ul>

    <div class="cta">
      <p>Paste your crontab to visualise every job on a 24-hour timeline — detect overlaps, collisions, and get flock-safe versions.</p>
      <a href="/">Open Cron Visualiser →</a>
    </div>

    <h2>Frequently Asked Questions</h2>
    {faq_html}
  </div>
{FOOTER}
</body>
</html>"""

def build_cron_index():
    cards = "\n".join([
        f"""    <a href="/cron/{item['slug']}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.6rem;text-decoration:none;">
      <span style="color:var(--purple);font-weight:700;font-size:0.9rem;">{item['expr']}</span>
      <span style="color:var(--muted);font-size:0.82rem;margin-left:1rem;">{item['meaning']}</span>
    </a>"""
        for item in CRON_EXPRESSIONS
    ])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Cron Expression Reference — ConfigClarity</title>
  <meta name="description" content="Cron expression reference — every minute, every hour, daily at midnight, weekly, monthly, and more. Field breakdowns, use cases, and flock safety examples.">
  <meta name="keywords" content="cron expression reference, cron syntax guide, cron examples, linux cron expressions">
  <link rel="canonical" href="{BASE}/cron/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"CollectionPage",
    "name":"Cron Expression Reference",
    "url":"{BASE}/cron/",
    "description":"Reference for common cron expressions — field breakdowns, use cases, and safety patterns."
  }}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div style="max-width:760px;margin:0 auto;padding:2rem;">
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:1.5rem;"><a href="/" style="color:var(--muted);">ConfigClarity</a> › Cron Expressions</div>
    <h1 style="font-size:1.6rem;font-weight:700;margin-bottom:0.75rem;">Cron Expression Reference</h1>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:2rem;">Field breakdowns, use cases, and flock safety patterns for the most common cron schedules. Paste your crontab into the <a href="/">Cron Visualiser</a> to see them on a timeline.</p>
{cards}
  </div>
{FOOTER}
</body>
</html>"""


if __name__ == '__main__':
    print("=== Building Cron Expression Pages ===\n")
    os.makedirs("cron", exist_ok=True)
    count = 0

    # Index
    with open("cron/index.html", "w") as f:
        f.write(build_cron_index())
    print("  ✅ cron/index.html")
    count += 1

    # Expression pages
    for item in CRON_EXPRESSIONS:
        os.makedirs(f"cron/{item['slug']}", exist_ok=True)
        with open(f"cron/{item['slug']}/index.html", "w") as f:
            f.write(build_cron_expr_page(item))
        print(f"  ✅ cron/{item['slug']}/index.html")
        count += 1

    print(f"\nCron pages built: {count}")

    # Update vercel.json
    with open("vercel.json", "r") as f:
        config = json.load(f)

    new_rewrites = [
        {"source": "/cron/", "destination": "/cron/index.html"},
        {"source": "/cron", "destination": "/cron/index.html"},
    ]
    for item in CRON_EXPRESSIONS:
        new_rewrites.append({"source": f"/cron/{item['slug']}/", "destination": f"/cron/{item['slug']}/index.html"})
        new_rewrites.append({"source": f"/cron/{item['slug']}", "destination": f"/cron/{item['slug']}/index.html"})

    added = sum(1 for r in new_rewrites if r not in config["rewrites"])
    for r in new_rewrites:
        if r not in config["rewrites"]:
            config["rewrites"].append(r)

    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  ✅ vercel.json — {added} cron rewrites added")

    # Update sitemap
    with open("sitemap-seo.xml", "r") as f:
        sitemap = f.read()

    new_urls = ["/cron/"] + [f"/cron/{item['slug']}/" for item in CRON_EXPRESSIONS]
    entries = "\n".join([
        f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        for u in new_urls if u not in sitemap
    ])
    if entries:
        sitemap = sitemap.replace("</urlset>", entries + "\n</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(sitemap)
    print(f"  ✅ sitemap-seo.xml — {len(new_urls)} cron URLs added")

    print(f"\nDone. {count} cron expression pages.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: proxy mapper pages + cron expression reference' && git push origin main && npx vercel --prod --force")
    print("\nTop GSC submissions:")
    print("  https://configclarity.dev/cron/")
    print("  https://configclarity.dev/cron/every-5-minutes/")
    print("  https://configclarity.dev/cron/every-day-midnight/")
    print("  https://configclarity.dev/fix/proxy/")
    print("  https://configclarity.dev/fix/proxy/traefik-v2-to-v3/")
    print("  https://configclarity.dev/fix/proxy/dangling-routes/")
