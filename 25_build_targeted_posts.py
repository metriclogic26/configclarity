#!/usr/bin/env python3
"""
Script 25: Build 4 targeted blog posts in natural human language.
1. How cron job overlaps crash your server
2. Reading crontab -l output like a sysadmin
3. Common cron scheduling mistakes that cause real problems
4. AI crawler opt-out: what robots.txt can and can't do
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

# ── POST 1 ────────────────────────────────────────────────────────────────────

POST1 = {
    "slug": "cron-job-overlaps-crash-server",
    "title": "How Cron Job Overlaps Crash Your Server (And How to Find Them)",
    "meta_desc": "Overlapping cron jobs are one of the most common causes of mysterious server load spikes. How they happen, why they're hard to spot, and how to find every conflict in your crontab.",
    "keywords": "cron job overlap, overlapping cron jobs, cron job collision, cron job server load spike, crontab overlap detection",
    "date": "2026-03-31",
    "tags": ["Cron", "Linux", "DevOps", "Server"],
    "lede": "Your server slows down every night at midnight. You restart it, everything's fine. A week later it happens again. You've checked the logs a dozen times and can't find the cause. The culprit is probably sitting in your crontab, completely invisible unless you know where to look.",
    "body": """
<p>Cron jobs don't announce themselves. They run quietly in the background, doing their thing — backing up databases, rotating logs, sending emails, running reports. Most of the time they're fine. But when two jobs happen to run at the same time and compete for the same resources, things get ugly fast.</p>

<p>The frustrating part is that the problem is invisible in the logs. You see high CPU usage, maybe some slow queries or timeouts, and then everything goes back to normal. Fifteen minutes later it's fine. Nothing in the error logs. No clear cause. Just a recurring mystery that gets worse over time as you add more jobs.</p>

<h2>What actually happens when cron jobs overlap</h2>

<p>Take a simple example. You have a database backup that runs every night at midnight and takes about 20 minutes. You also have a report generation job that runs at midnight. And a log cleanup script — also midnight, because that's the obvious "run it when no one's around" time.</p>

<p>At 00:00 all three jobs start simultaneously. The backup is hammering disk I/O. The report generator is running heavy queries against the same database. The log cleanup is scanning the filesystem. The server CPU spikes. The database slows down. If any of your services have health checks or timeouts, they start failing. Users hitting your site at 12:01 AM get slow responses or errors.</p>

<p>This is the midnight pile-up. It's the most common cron scheduling problem on the internet and it's almost entirely avoidable.</p>

<h2>The hidden version: jobs that run too long</h2>

<p>The midnight pile-up is obvious once you know to look for it. The harder problem is when a single job occasionally runs longer than its interval.</p>

<p>You have a job scheduled every 15 minutes. Most of the time it runs in 3 minutes and exits. But occasionally — when the database is under load, or the network is slow, or there's just more data than usual — it takes 18 minutes. At minute 15, cron fires a second instance of the same job. Now you have two copies running simultaneously, both competing for the same database connections, both writing to the same output files.</p>

<pre># This looks innocent:
*/15 * * * * /usr/bin/process-queue.sh

# But if process-queue.sh takes 18 minutes, you get this:
# 00:00 — instance 1 starts
# 00:15 — instance 2 starts (instance 1 still running)
# 00:18 — instance 1 finishes
# 00:30 — instance 3 starts (instance 2 still running)
# ... and so on</pre>

<p>This compounds. Under heavy load the job takes longer. A longer job means more overlap. More overlap means more load. More load means the job takes even longer. It's a death spiral that's nearly impossible to debug after the fact because by the time you look at it, the jobs have already finished.</p>

<h2>Why this is hard to see in your crontab</h2>

<p>Look at a typical crontab:</p>

<pre>0 2 * * *    /usr/bin/db-backup.sh
*/30 * * * * /usr/bin/sync-data.sh
0 * * * *    /usr/bin/health-check.sh
30 1 * * *   /usr/bin/generate-report.sh
0 0 * * *    /usr/bin/cleanup-logs.sh
*/5 * * * *  /usr/bin/process-queue.sh</pre>

<p>Reading this and mentally computing all the overlaps is genuinely hard. The <code>*/30</code> job runs at :00 and :30 of every hour. The <code>0 * * * *</code> job runs at the top of every hour. So they overlap at :00 of every hour. The cleanup job at midnight and the health check at midnight also overlap. The report job at 1:30 runs for how long? If it takes more than 30 minutes it will still be running when the 2am backup starts.</p>

<p>Six jobs and you already need a spreadsheet to track the interactions. Real crontabs have 15-30 jobs. The mental model breaks down completely.</p>

<h2>How to find every overlap</h2>

<p>The right approach is to visualize the schedule — render every job as a bar on a timeline and see where they overlap visually.</p>

<pre># Step 1: export your crontab
crontab -l

# Step 2: paste into a visualizer and look for overlapping bars</pre>

<div class="cta">
  <p>Paste your crontab and see every job on a 24-hour timeline. Overlaps are flagged in red with exact conflict windows and severity ratings.</p>
  <a href="/">Open Cron Visualiser →</a>
</div>

<h2>Fixing overlaps: stagger the schedule</h2>

<p>The simplest fix for the midnight pile-up is to spread jobs across different minutes:</p>

<pre># Before — three jobs colliding at midnight:
0 0 * * * /usr/bin/cleanup-logs.sh
0 0 * * * /usr/bin/generate-report.sh
0 0 * * * /usr/bin/db-backup.sh

# After — staggered by 10 minutes:
0 0 * * *  /usr/bin/cleanup-logs.sh
10 0 * * * /usr/bin/generate-report.sh
20 0 * * * /usr/bin/db-backup.sh</pre>

<p>This doesn't prevent overlap if jobs run longer than their stagger window — but it eliminates the simultaneous start problem.</p>

<h2>Fixing concurrent runs: flock</h2>

<p>For jobs that might run longer than their interval, use <code>flock</code> to prevent concurrent execution:</p>

<pre># Without flock — two instances can run simultaneously:
*/15 * * * * /usr/bin/process-queue.sh

# With flock — second instance exits immediately if first is still running:
*/15 * * * * flock -n /tmp/process-queue.lock /usr/bin/process-queue.sh</pre>

<p>The <code>-n</code> flag means non-blocking — if the lock is held, exit immediately rather than waiting. The lock file is automatically released when the first process finishes, even if it crashes.</p>

<h2>What to check in your crontab right now</h2>

<p>Three patterns to look for:</p>

<p><strong>Jobs scheduled at exactly 0 0 * * *</strong> — midnight is the most over-scheduled minute in every crontab. Count how many of your jobs run at midnight and spread them out.</p>

<p><strong>Jobs with short intervals doing heavy work</strong> — anything running every 1, 5, or 15 minutes that touches a database or makes HTTP requests should have flock protection.</p>

<p><strong>Jobs with no runtime estimate</strong> — if you don't know how long a job takes, find out. Run it manually with <code>time /usr/bin/yourscript.sh</code> and compare against its interval.</p>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/cron/overlapping-jobs/">Overlapping cron jobs fix guide</a></li>
  <li><a href="/fix/cron/flock-safety/">Adding flock safety to cron jobs</a></li>
  <li><a href="/fix/cron/server-load-spike/">Cron jobs causing server load spikes</a></li>
  <li><a href="/fix/cron/silent-failure/">Cron jobs failing silently</a></li>
  <li><a href="/glossary/cron-job-collision/">Cron job collision explained</a></li>
</ul>
""",
    "faq": [
        ("How do I know if my cron jobs are overlapping?",
         "The most reliable way is to visualize your full crontab on a timeline. Paste your crontab -l output into ConfigClarity's Cron Visualiser and it will show every job as a bar on a 24-hour timeline with overlapping windows flagged in red."),
        ("What is the most common cron scheduling mistake?",
         "Scheduling multiple jobs at exactly midnight (0 0 * * *). This is the default time developers choose when a job has no specific time requirement, resulting in multiple heavy jobs running simultaneously and causing server load spikes."),
        ("What is flock and why should I use it with cron?",
         "flock is a Linux utility that prevents a script from running if a previous instance is still executing. Using flock -n /tmp/jobname.lock command prevents concurrent cron job execution when a job runs longer than its scheduled interval."),
    ],
}

# ── POST 2 ────────────────────────────────────────────────────────────────────

POST2 = {
    "slug": "reading-crontab-output",
    "title": "Reading crontab -l Output Like a Sysadmin",
    "meta_desc": "How to read and understand crontab -l output — the five fields, special strings, environment variables, and what the common patterns actually mean.",
    "keywords": "crontab -l output, read crontab, crontab explained, crontab fields explained, crontab format",
    "date": "2026-03-31",
    "tags": ["Cron", "Linux", "Sysadmin"],
    "lede": "You run crontab -l and get a wall of asterisks, numbers, and paths. Some lines make sense. Some are completely opaque. Here's how to read every part of it.",
    "body": """
<p>The crontab format was designed in 1975 and has barely changed since. It's terse, unforgiving, and gives you zero feedback when you get it wrong. But once you understand the five-field structure, the rest falls into place quickly.</p>

<h2>The five fields</h2>

<pre># minute  hour  day-of-month  month  day-of-week  command
  *       *     *             *      *            /usr/bin/mycommand</pre>

<p>From left to right: minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-7, where both 0 and 7 mean Sunday). Then the command.</p>

<p>A <code>*</code> means "every value." So <code>* * * * *</code> means every minute of every hour of every day. <code>0 * * * *</code> means the top of every hour (minute 0, every hour). <code>0 2 * * *</code> means 2:00 AM every day.</p>

<h2>Reading the common patterns</h2>

<pre>*/5 * * * *     # every 5 minutes
0 * * * *       # every hour, on the hour
0 0 * * *       # daily at midnight
0 2 * * *       # daily at 2am
0 9 * * 1-5     # 9am on weekdays (Monday=1, Friday=5)
0 0 1 * *       # first day of every month at midnight
0 0 * * 0       # every Sunday at midnight</pre>

<p>The <code>*/5</code> pattern means "every 5th value" — so in the minute field it fires at 0, 5, 10, 15... 55. In the hour field, <code>*/6</code> would fire at 0, 6, 12, 18.</p>

<p>The <code>1-5</code> pattern is a range — Monday through Friday. You can also use lists: <code>1,3,5</code> means Monday, Wednesday, Friday.</p>

<h2>Special strings</h2>

<p>Some crontabs use special strings instead of the five fields:</p>

<pre>@reboot    # runs once when cron starts (every system boot)
@hourly    # same as 0 * * * *
@daily     # same as 0 0 * * *
@weekly    # same as 0 0 * * 0
@monthly   # same as 0 0 1 * *
@yearly    # same as 0 0 1 1 *</pre>

<p><code>@reboot</code> is the one that confuses people. It runs every time the cron daemon starts, which is every system boot. It's not a one-time setup job — it runs on every reboot.</p>

<h2>Environment variables at the top</h2>

<p>Many crontabs have variable definitions above the jobs:</p>

<pre>SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=admin@yourdomain.com

0 2 * * * /usr/bin/backup.sh</pre>

<p><code>SHELL</code> sets which shell runs the commands. <code>PATH</code> is critical — cron has a minimal PATH by default, which is why scripts that work fine when you run them manually fail silently in cron. If your script calls a command that's not in cron's default PATH, it won't be found.</p>

<p><code>MAILTO</code> is where cron sends output. If you set <code>MAILTO=""</code> — all output is discarded silently. This is the most common cause of "my cron job isn't doing anything." Set <code>MAILTO</code> to your email address during debugging.</p>

<h2>Why scripts fail in cron but work manually</h2>

<p>Three reasons:</p>

<p><strong>PATH is different.</strong> Cron's default PATH is <code>/usr/bin:/bin</code>. If your script calls <code>python3</code> or <code>node</code> or any tool installed in <code>/usr/local/bin</code>, cron won't find it. Fix: use absolute paths in your scripts (<code>/usr/bin/python3</code> not just <code>python3</code>) or set PATH at the top of your crontab.</p>

<p><strong>No home directory.</strong> Cron doesn't set <code>$HOME</code> the same way your login shell does. Scripts that reference <code>~/.config/something</code> may fail.</p>

<p><strong>Output is going nowhere.</strong> If your script prints errors but you're not capturing output, you'll never see them. Add <code>&gt;&gt; /var/log/myjob.log 2&gt;&amp;1</code> to the end of your cron command to capture both stdout and stderr to a log file.</p>

<pre># Debug-friendly cron entry:
0 2 * * * /usr/bin/backup.sh >> /var/log/backup.log 2>&1</pre>

<h2>Reading a real-world crontab</h2>

<pre>SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=""

# System maintenance
0 0 * * *    flock -n /tmp/cleanup.lock /usr/local/bin/cleanup.sh
15 0 * * *   /usr/local/bin/db-backup.sh >> /var/log/db-backup.log 2>&1
0 2 * * 0    /usr/local/bin/weekly-report.sh

# Application jobs
*/5 * * * *  flock -n /tmp/queue.lock /app/bin/process-queue
0 * * * *    /app/bin/sync-remote-data >> /var/log/sync.log 2>&1

@reboot      /usr/local/bin/start-monitoring.sh</pre>

<p>Reading this line by line: cleanup runs at midnight with flock protection. DB backup runs at 12:15 AM (staggered from cleanup) with output logged. Weekly report runs Sunday at 2 AM. Queue processor runs every 5 minutes with flock. Remote sync runs every hour. Monitoring script starts on every boot.</p>

<p>This is a well-structured crontab: staggered schedules, flock on anything that might overlap, output captured to logs.</p>

<h2>Visualise it before you change it</h2>

<p>The hardest part of editing a crontab is understanding the interactions between existing jobs before adding a new one. A new job at <code>0 0 * * *</code> might look innocent but collide with three existing midnight jobs.</p>

<div class="cta">
  <p>Paste your crontab -l output to see every job on a timeline — before you make changes that cause problems at 2am.</p>
  <a href="/">Open Cron Visualiser →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/cron/every-minute/">Every minute cron expression</a></li>
  <li><a href="/cron/every-hour/">Every hour cron expression</a></li>
  <li><a href="/cron/every-day-midnight/">Daily at midnight cron expression</a></li>
  <li><a href="/fix/cron/silent-failure/">Cron jobs failing silently fix</a></li>
  <li><a href="/blog/cron-job-overlaps-crash-server/">How cron job overlaps crash your server</a></li>
</ul>
""",
    "faq": [
        ("What do the five fields in a crontab entry mean?",
         "Left to right: minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-7 where 0 and 7 both mean Sunday). An asterisk means every value. So 0 2 * * * means 2:00 AM every day."),
        ("Why does my cron job work manually but not in cron?",
         "The most common cause is PATH. Cron has a minimal default PATH of /usr/bin:/bin. Commands installed in /usr/local/bin are not found. Fix this by using absolute paths in your script or setting PATH at the top of your crontab."),
        ("What does MAILTO= mean in a crontab?",
         "MAILTO controls where cron sends the output of your jobs. Setting MAILTO= (empty) silently discards all output, which is the most common reason cron jobs appear to do nothing. Set MAILTO to your email address during debugging, or redirect output to a log file with >> /var/log/job.log 2>&1."),
    ],
}

# ── POST 3 ────────────────────────────────────────────────────────────────────

POST3 = {
    "slug": "cron-scheduling-mistakes",
    "title": "Common Cron Scheduling Mistakes That Cause Real Problems",
    "meta_desc": "The cron scheduling mistakes that actually cause outages — midnight pile-ups, missing flock, silent failures, wrong timezones, and jobs that grow over time.",
    "keywords": "cron job mistakes, cron scheduling mistakes, cron job best practices, cron job problems, crontab common errors",
    "date": "2026-03-31",
    "tags": ["Cron", "Linux", "DevOps"],
    "lede": "Most cron problems aren't syntax errors — those you catch immediately. The real problems are scheduling decisions that look fine when you set them up and only surface weeks later at 2am when everything breaks at once.",
    "body": """
<p>Cron is one of the oldest scheduling tools in Unix and one of the most reliably misused. Not because it's complicated — the five-field format is actually quite simple — but because the mistakes are invisible until they compound into something you can't ignore.</p>

<h2>Mistake 1: Everything at midnight</h2>

<p>This is the most common cron mistake on the planet. When you need to run something "once a day when nobody's around," you pick midnight. So does every other developer on the team. So did whoever set up the server three years ago. Before long, half your crontab fires simultaneously at 00:00 and your server resembles a traffic jam.</p>

<pre># The typical result:
0 0 * * * /usr/bin/db-backup.sh          # takes 15 minutes
0 0 * * * /usr/bin/cleanup-old-files.sh  # hammers disk
0 0 * * * /usr/bin/generate-reports.sh   # heavy queries
0 0 * * * /usr/bin/send-daily-digest.sh  # lots of DB reads</pre>

<p>The fix is simple: stagger your jobs. Spread them across different minutes or even different hours. The exact time usually doesn't matter — almost nothing needs to run at exactly midnight.</p>

<pre>0  0 * * * /usr/bin/db-backup.sh
15 0 * * * /usr/bin/cleanup-old-files.sh
30 0 * * * /usr/bin/generate-reports.sh
45 0 * * * /usr/bin/send-daily-digest.sh</pre>

<h2>Mistake 2: No flock on jobs that run more than a few seconds</h2>

<p>If a job runs every 5 minutes and occasionally takes 6 minutes, you now have two copies running simultaneously. Both hitting the same database. Both writing to the same files. Both consuming memory. This compounds — the extra load makes the next run take even longer.</p>

<pre># Vulnerable:
*/5 * * * * /usr/bin/process-orders.sh

# Protected:
*/5 * * * * flock -n /tmp/process-orders.lock /usr/bin/process-orders.sh</pre>

<p>flock is installed on every Linux system. There's no reason not to use it on any job that does real work.</p>

<h2>Mistake 3: Silently discarding output</h2>

<p>Cron sends job output to the system mail. Most servers either don't have a mail daemon configured or the mail goes somewhere nobody reads. The result is that cron job failures are completely silent.</p>

<pre># Silent — you'll never know if this fails:
0 2 * * * /usr/bin/backup.sh

# Auditable — errors go to a log you can check:
0 2 * * * /usr/bin/backup.sh >> /var/log/backup.log 2>&1

# Even better — log with timestamps:
0 2 * * * echo "$(date): starting backup" >> /var/log/backup.log && /usr/bin/backup.sh >> /var/log/backup.log 2>&1</pre>

<div class="callout">
  <p><strong>Check your crontab right now:</strong> how many jobs redirect output? If the answer is "none," you have no idea whether half your cron jobs are working.</p>
</div>

<h2>Mistake 4: Wrong timezone</h2>

<p>Cron uses the system timezone. Your server is probably set to UTC. Your laptop is probably set to your local timezone. When you write a cron job thinking "I want this to run at 9 AM," you need to know which 9 AM you mean.</p>

<pre># Check your server timezone:
timedatectl | grep "Time zone"
date

# If your server is UTC and you want 9am New York time:
# New York is UTC-5 (winter) or UTC-4 (summer)
# So 9am New York = 14:00 UTC (winter) or 13:00 UTC (summer)
0 14 * * * /usr/bin/morning-report.sh  # winter
0 13 * * * /usr/bin/morning-report.sh  # summer</pre>

<p>The daylight saving time transition is particularly painful — a job set to "9am Eastern" in winter runs an hour off in summer if you calculated it in UTC wrong. Use UTC for everything and convert deliberately.</p>

<h2>Mistake 5: Jobs that grow over time</h2>

<p>A backup job that takes 3 minutes today will take 30 minutes in two years as your data grows. Nobody goes back and adjusts the schedule. Eventually it's still running when the next day's backup starts and you have two backups running simultaneously, each taking twice as long as it should.</p>

<p>The fix is to monitor job duration and review it periodically — or use flock so overlapping instances are prevented regardless of how long the job takes.</p>

<pre># Check how long your jobs actually take:
time /usr/bin/backup.sh

# Add to cron with timing logged:
0 2 * * * { time /usr/bin/backup.sh; } >> /var/log/backup.log 2>&1</pre>

<h2>Mistake 6: Using cron for things that should be monitored</h2>

<p>Cron fires and forgets. If a job fails, nothing happens. If a job stops running entirely (because the crontab got wiped, or the server rebooted and something didn't start), nothing happens. No alert. No notification. No indication anything is wrong until someone notices the data hasn't been processed in three days.</p>

<p>For anything critical, add a dead man's switch: a service like Healthchecks.io or a simple curl to a monitoring endpoint at the end of your job. If the ping doesn't arrive, you get alerted.</p>

<pre># Ping a healthcheck endpoint on success:
0 2 * * * /usr/bin/backup.sh && curl -s https://hc-ping.com/your-uuid</pre>

<h2>Mistake 7: Hardcoding paths that change</h2>

<pre># Will break if Python moves or a virtualenv is activated differently:
0 * * * * python3 /app/scripts/sync.py

# More robust — use absolute paths:
0 * * * * /usr/bin/python3 /app/scripts/sync.py

# Or activate virtualenv explicitly:
0 * * * * /app/venv/bin/python /app/scripts/sync.py</pre>

<h2>The quick audit</h2>

<p>Run <code>crontab -l</code> and check each job against this list:</p>

<ul style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.4;">
  <li>Is it scheduled at exactly <code>0 0 * * *</code>? Can it be staggered?</li>
  <li>Does it run more than once per hour? Does it have flock protection?</li>
  <li>Does it redirect output to a log file?</li>
  <li>Do you know how long it takes? Does that fit inside its interval?</li>
  <li>Is the timezone correct for what you intended?</li>
</ul>

<div class="cta">
  <p>Paste your crontab to see every job on a timeline, spot midnight pile-ups, and identify jobs that need flock protection.</p>
  <a href="/">Open Cron Visualiser →</a>
</div>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/blog/cron-job-overlaps-crash-server/">How cron job overlaps crash your server</a></li>
  <li><a href="/fix/cron/overlapping-jobs/">Overlapping cron jobs fix</a></li>
  <li><a href="/fix/cron/flock-safety/">Adding flock safety</a></li>
  <li><a href="/fix/cron/silent-failure/">Cron jobs failing silently</a></li>
  <li><a href="/fix/cron/server-load-spike/">Server load spikes from cron</a></li>
</ul>
""",
    "faq": [
        ("What is the most dangerous cron scheduling mistake?",
         "Scheduling multiple heavy jobs at exactly midnight (0 0 * * *) without staggering them. This causes simultaneous execution of competing processes and is responsible for the most common pattern of overnight server load spikes."),
        ("How do I prevent a cron job from running twice?",
         "Use flock: wrap your command with flock -n /tmp/jobname.lock your-command. If a previous instance is still running, the new invocation exits immediately without starting a second copy."),
        ("How do I know if my cron jobs are failing?",
         "Add output redirection to every job: append >> /var/log/jobname.log 2>&1 to capture both stdout and stderr. Without this, all output is silently discarded and failures are invisible."),
    ],
}

# ── POST 4 ────────────────────────────────────────────────────────────────────

POST4 = {
    "slug": "ai-crawler-opt-out-robots-txt",
    "title": "AI Crawler Opt-Out: What robots.txt Can and Can't Do",
    "meta_desc": "Should you block AI crawlers in robots.txt? What GPTBot, ClaudeBot, PerplexityBot actually respect, what they ignore, and how to make an informed decision for your site.",
    "keywords": "block ai crawlers robots.txt, gptbot robots.txt, block chatgpt crawler, claudebot robots.txt, ai crawler opt out, robots.txt ai bots",
    "date": "2026-03-31",
    "tags": ["robots.txt", "SEO", "AI", "Web"],
    "lede": "Every webmaster is now asking whether to block AI crawlers. The answer isn't obvious — and robots.txt is a weaker tool than most people think. Here's what actually happens when you add GPTBot to your disallow list.",
    "body": """
<p>Since OpenAI published GPTBot's user agent string in 2023, the robots.txt conversation has changed permanently. Now there are a dozen AI crawlers with named user agents, and every site owner has to decide: allow them, block them, or do nothing.</p>

<p>Before you add a line to your robots.txt, it's worth understanding what that line actually does — and what it doesn't.</p>

<h2>The crawlers you need to know about</h2>

<p>The major AI crawlers with named user agents that respond to robots.txt:</p>

<ul style="font-size:0.875rem;color:var(--muted);padding-left:1.5rem;line-height:2.4;">
  <li><strong>GPTBot</strong> — OpenAI's training crawler. Documented since August 2023. Generally respects robots.txt.</li>
  <li><strong>ClaudeBot</strong> — Anthropic's crawler. Documented and respects robots.txt.</li>
  <li><strong>Google-Extended</strong> — Controls whether Google uses your content for Bard/Gemini training and AI Overviews. Separate from Googlebot — blocking Google-Extended doesn't affect your search rankings.</li>
  <li><strong>PerplexityBot</strong> — Perplexity AI's crawler. Respects robots.txt but has been reported as inconsistent.</li>
  <li><strong>Bytespider</strong> — ByteDance (TikTok parent company). Compliance is less consistent than the others.</li>
  <li><strong>CCBot</strong> — Common Crawl. Used by many AI training datasets. Compliance varies widely.</li>
</ul>

<h2>What robots.txt actually does</h2>

<p>robots.txt is a voluntary protocol. There is no technical enforcement. A well-behaved crawler reads your robots.txt before crawling and respects the Disallow directives. A poorly-behaved or malicious crawler ignores it entirely.</p>

<p>The major named AI crawlers — GPTBot, ClaudeBot, Google-Extended — are from large companies with reputational stakes and legal teams. They generally respect robots.txt. The long tail of smaller crawlers and scrapers? Much less consistent.</p>

<div class="callout">
  <p><strong>Key point:</strong> blocking a crawler in robots.txt prevents future crawling from that crawler. It does not remove your content from training datasets that were built before you added the block. If GPTBot already crawled your site last year, that data is already in the training set.</p>
</div>

<h2>Should you block AI crawlers?</h2>

<p>This is a genuine strategic decision, not a clear-cut technical one. The right answer depends on what you want:</p>

<p><strong>Block if:</strong> your content is proprietary, paywalled, or you're concerned about your work being used to train commercial AI models without compensation. Publishers, news organizations, and content creators with monetized archives are the clearest cases for blocking.</p>

<p><strong>Allow if:</strong> you want your content cited in AI-generated answers. When someone asks ChatGPT or Perplexity a question and your content is in the training data or can be crawled, there's a chance your site gets cited. This is called GEO — Generative Engine Optimisation — and it's the emerging counterpart to traditional SEO. Sites that block all AI crawlers are excluded from this entirely.</p>

<p><strong>Selective approach:</strong> block training crawlers (GPTBot, CCBot) while allowing retrieval crawlers (PerplexityBot) and keeping Google-Extended allowed for AI Overviews. This attempts to avoid training data use while preserving citation opportunities.</p>

<h2>How to block specific AI crawlers</h2>

<pre># Block OpenAI training crawler:
User-agent: GPTBot
Disallow: /

# Block Anthropic crawler:
User-agent: ClaudeBot
Disallow: /

# Block Google's AI training (doesn't affect search rankings):
User-agent: Google-Extended
Disallow: /

# Block ByteDance:
User-agent: Bytespider
Disallow: /

# Block Common Crawl:
User-agent: CCBot
Disallow: /</pre>

<h2>How to allow all AI crawlers explicitly</h2>

<pre># Explicit allow for AI crawlers (GEO strategy):
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /</pre>

<p>You don't technically need to add Allow directives if you're not blocking anything — crawlers are allowed by default. But explicit Allow entries signal intent and may be read by AI systems evaluating whether your content is available for citation.</p>

<h2>What about the Google-Extended nuance</h2>

<p>Google-Extended is worth understanding separately because it controls two different things: whether your content is used for AI model training, and whether it's included in AI Overviews (the AI-generated summaries at the top of search results).</p>

<p>Blocking Google-Extended removes you from both. If you want to appear in AI Overviews (which drives traffic) but don't want your content in training data, the current robots.txt spec doesn't support that distinction — it's all or nothing with Google-Extended.</p>

<h2>Check your current AI bot coverage</h2>

<p>Most robots.txt files were written before AI crawlers existed and don't address them at all. The first step is knowing where you currently stand.</p>

<div class="cta">
  <p>Paste your robots.txt to see your AI bot coverage score — which crawlers are explicitly allowed, which are blocked, and which are unaddressed.</p>
  <a href="/robots/">Open robots.txt Validator →</a>
</div>

<h2>The honest answer</h2>

<p>robots.txt is a reasonable first line of defence against well-behaved AI crawlers. It's not a legal instrument, it's not technically enforced, and it doesn't reach data that's already been collected. But for the major named crawlers from large companies, it's generally respected and worth using if you have a clear preference.</p>

<p>The most important thing is to make a deliberate decision rather than ignoring the question. An unaddressed robots.txt in 2026 is an implicit "I haven't thought about this" — which is a fine answer but probably not the one you intend.</p>

<h2>Related guides</h2>
<ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);line-height:2.2;">
  <li><a href="/fix/robots/blocking-ai-bots/">Blocking AI bots in robots.txt</a></li>
  <li><a href="/fix/robots/allow-ai-bots/">Allowing AI bots for GEO</a></li>
  <li><a href="/fix/robots/block-gptbot/">Block GPTBot specifically</a></li>
  <li><a href="/fix/robots/block-claudebot/">Block ClaudeBot specifically</a></li>
  <li><a href="/fix/robots/noindex-vs-disallow/">noindex vs Disallow — what's the difference</a></li>
</ul>
""",
    "faq": [
        ("Does blocking GPTBot in robots.txt remove my content from ChatGPT?",
         "No. Blocking GPTBot prevents future crawling of your site but does not remove content that was already collected before you added the block. If your site was crawled during training data collection, that data is already in the model."),
        ("Does blocking Google-Extended affect my search rankings?",
         "No. Google-Extended is a separate user agent from Googlebot. Blocking Google-Extended prevents your content from being used for Google AI training and AI Overviews, but does not affect standard search indexing or rankings."),
        ("Which AI crawlers actually respect robots.txt?",
         "GPTBot (OpenAI), ClaudeBot (Anthropic), and Google-Extended generally respect robots.txt. PerplexityBot is usually compliant. Bytespider and CCBot have more inconsistent compliance. Smaller scrapers and unofficial crawlers often ignore robots.txt entirely."),
    ],
}

POSTS = [POST1, POST2, POST3, POST4]


def make_faq_schema(faqs):
    items = ",\n".join([
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faqs
    ])
    return f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}'


def build_blog_page(p):
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
    {{"@type":"ListItem","position":3,"name":"{p['title']}","item":"{canonical}"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/blog/">Blog</a> › {p['title'][:60]}</div>
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
    print("=== Building 4 targeted blog posts ===\n")

    new_rewrites = []
    new_sitemap = []

    for p in POSTS:
        html = build_blog_page(p)

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

    print(f"\nDone. Blog is now 16 posts.")
    print("\nRun:")
    print("  git add -A && git commit -m 'feat: 4 targeted blog posts — cron overlaps, crontab reading, cron mistakes, AI crawlers' && git push origin main && npx vercel --prod --force")
    print("\nGSC — submit tomorrow:")
    for url in new_sitemap:
        print(f"  https://configclarity.dev{url}")
