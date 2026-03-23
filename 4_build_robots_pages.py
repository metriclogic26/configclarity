#!/usr/bin/env python3
"""
Script 4: Build 25 robots.txt SEO pages.
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
      h1 { font-size: 1.6rem; font-weight: 700; margin-bottom: 1rem; }
      h2 { font-size: 1.05rem; font-weight: 600; margin: 2rem 0 0.75rem; }
      p { font-size: 0.875rem; color: var(--muted); margin-bottom: 1rem; }
      pre { background: #0b0d14; border: 1px solid #2a2d3d; border-radius: 6px; padding: 1rem 1.25rem; font-size: 0.78rem; overflow-x: auto; margin: 0.75rem 0 1.25rem; }
      .fix-box { background: var(--bg2); border-left: 3px solid var(--green); border-radius: 0 8px 8px 0; padding: 1.25rem 1.5rem; margin: 1.5rem 0; }
      .fix-box .label { font-size: 0.7rem; color: var(--green); text-transform: uppercase; letter-spacing: .06em; margin-bottom: 0.5rem; }
      .faq-item { margin-bottom: 1.5rem; }
      .faq-q { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; }
      .faq-a { font-size: 0.85rem; color: var(--muted); }
      .cta-box { background: var(--bg2); border: 1px solid #2a2d3d; border-radius: 8px; padding: 1.25rem 1.5rem; margin: 2rem 0; text-align: center; }
      .cta-box p { color: var(--text); margin-bottom: 0.75rem; }
      .cta-btn { display: inline-block; background: var(--purple); color: #fff; padding: 0.45rem 1.2rem; border-radius: 6px; font-size: 0.82rem; font-weight: 700; }
      .tag { display: inline-block; font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(108,99,255,.15); color: var(--purple); margin-right: 0.4rem; margin-bottom: 0.75rem; }
      footer { text-align: center; padding: 2rem; font-size: 0.75rem; color: var(--muted); border-top: 1px solid #2a2d3d; margin-top: 2rem; }
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
    <p><a href="/glossary/">Glossary</a> &nbsp;·&nbsp; <a href="/fix/">Fix Guides</a> &nbsp;·&nbsp;
    <a href="https://metriclogic.dev">MetricLogic Network</a> &nbsp;·&nbsp;
    <a href="https://github.com/metriclogic26/configclarity">GitHub (MIT)</a></p>
  </footer>
"""

def make_fix_page(slug, title, meta_desc, keywords, intro, problem, fix_label, fix_code, fix_explanation, faqs, related_links):
    faq_schema = ",\n".join([
        f'{{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}'
        for q, a in faqs
    ])
    faq_html = "\n".join([
        f'''      <div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'''
        for q, a in faqs
    ])
    related_html = "\n".join([f'<li><a href="{url}">{label}</a></li>' for url, label in related_links])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — ConfigClarity</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="https://configclarity.dev/fix/robots/{slug}/">
  <meta property="og:title" content="{title} — ConfigClarity">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="https://configclarity.dev/fix/robots/{slug}/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle",
    "headline":"{title}",
    "url":"https://configclarity.dev/fix/robots/{slug}/",
    "description":"{meta_desc}",
    "author":{{"@type":"Organization","name":"MetricLogic"}},
    "isPartOf":{{"@type":"WebSite","name":"ConfigClarity","url":"https://configclarity.dev"}}
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Fix Guides","item":"https://configclarity.dev/fix/"}},
    {{"@type":"ListItem","position":3,"name":"robots.txt","item":"https://configclarity.dev/fix/robots/"}},
    {{"@type":"ListItem","position":4,"name":"{title}","item":"https://configclarity.dev/fix/robots/{slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/robots/">robots.txt</a> › {title}
  </div>
  <div class="content">
    <h1>{title}</h1>
    <p>{intro}</p>
    <h2>The Problem</h2>
    <p>{problem}</p>
    <h2>The Fix</h2>
    <div class="fix-box">
      <div class="label">{fix_label}</div>
      <pre>{fix_code}</pre>
    </div>
    <p>{fix_explanation}</p>
    <div class="cta-box">
      <p>Validate your robots.txt live — fetch any URL and get a corrected file in one click.</p>
      <a href="/robots/" class="cta-btn">Open robots.txt Validator →</a>
    </div>
    <h2>Frequently Asked Questions</h2>
{faq_html}
    <h2>Related Guides</h2>
    <ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);">{related_html}</ul>
  </div>
{FOOTER}
</body>
</html>"""

# ─── 9 FIX PAGES ──────────────────────────────────────────────────────────────

FIX_PAGES = [
    {
        "slug": "accidental-disallow-all",
        "title": "Fix: robots.txt Accidentally Blocking All Crawlers",
        "meta_desc": "How to fix robots.txt Disallow: / blocking all search engine crawlers. Exact corrected robots.txt with explanation of why this blocks Google indexing.",
        "keywords": "robots.txt disallow all fix, robots.txt blocking google, fix robots txt crawl block",
        "intro": "A robots.txt file with <code>Disallow: /</code> for <code>User-agent: *</code> blocks all search engine crawlers from indexing any page on the site. This is one of the most common causes of sites disappearing from Google search results overnight.",
        "problem": "The <code>Disallow: /</code> directive tells every crawler that no part of the site should be crawled. This is correct behaviour for staging environments but catastrophic for production sites. It is often introduced accidentally by a developer testing staging robots.txt and forgetting to update before deploying to production, or by a CMS that ships with SEO-unfriendly defaults.",
        "fix_label": "CORRECTED robots.txt",
        "fix_code": """# Allow all crawlers to index the full site
User-agent: *
Allow: /

# Explicitly allow AI crawlers (optional but recommended)
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

# Reference your sitemap
Sitemap: https://yourdomain.com/sitemap.xml""",
        "fix_explanation": "Replace <code>Disallow: /</code> with <code>Allow: /</code> or simply remove the Disallow line entirely. An empty <code>Disallow:</code> is equivalent to <code>Allow: /</code>. Note: changes to robots.txt take effect when Googlebot next crawls the file — typically within 24–48 hours. Use Google Search Console's URL Inspection tool to request immediate recrawl.",
        "faqs": [
            ("How long does it take for Google to re-index after fixing robots.txt?", "Google typically re-crawls robots.txt within 24–48 hours of a change. For faster recrawling, use Google Search Console's URL Inspection tool on the homepage and request indexing. Previously indexed pages should reappear in search results within 1–2 weeks."),
            ("Why does my site disappear from Google after a deployment?", "The most common cause is a staging robots.txt (with Disallow: /) being deployed to production. CMS platforms like WordPress also sometimes reset robots.txt settings after updates. Check your robots.txt immediately after any deployment."),
            ("Does Disallow: / affect all search engines?", "Yes. Disallow: / under User-agent: * applies to all crawlers that respect the robots exclusion protocol — Google, Bing, DuckDuckGo, Yahoo, and most others. AI crawlers like GPTBot also respect it."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator tool"),
            ("/fix/robots/blocking-css-js/", "Fix: Blocking CSS and JS files"),
            ("/glossary/", "DevOps Glossary"),
        ],
    },
    {
        "slug": "blocking-css-js",
        "title": "Fix: robots.txt Blocking CSS and JavaScript Files",
        "meta_desc": "How to fix robots.txt blocking CSS and JavaScript files that Google needs to render your pages. Blocking these causes incorrect indexing and lower search rankings.",
        "keywords": "robots.txt blocking css js, googlebot cant render page, robots txt css javascript fix",
        "intro": "Blocking CSS and JavaScript files in robots.txt prevents Googlebot from fully rendering your pages. Google evaluates pages as a rendered browser experience — if it cannot load your stylesheets and scripts, it sees a broken page and may rank it lower or index it incorrectly.",
        "problem": "Older SEO advice recommended blocking CSS and JS with robots.txt to save crawl budget. This is now incorrect. Googlebot renders JavaScript and needs CSS to understand page structure. Blocking <code>/assets/</code>, <code>/static/</code>, or <code>*.css</code> patterns prevents rendering and causes Google Search Console to report 'Page could not be rendered' warnings.",
        "fix_label": "CORRECTED robots.txt — Remove CSS/JS blocks",
        "fix_code": """# BEFORE (incorrect — blocks rendering):
# User-agent: Googlebot
# Disallow: /assets/
# Disallow: /static/
# Disallow: /*.css$
# Disallow: /*.js$

# AFTER (correct — allow everything):
User-agent: *
Allow: /

# Only block paths you genuinely don't want indexed:
Disallow: /admin/
Disallow: /api/
Disallow: /.well-known/

Sitemap: https://yourdomain.com/sitemap.xml""",
        "fix_explanation": "Remove all <code>Disallow</code> rules targeting CSS, JS, image, or font files. Only disallow paths that should genuinely not appear in search results — admin panels, API endpoints, and internal tooling. Use the Google Search Console Coverage report to check for 'blocked by robots.txt' warnings after the fix.",
        "faqs": [
            ("Should I block /wp-admin/ in robots.txt?", "Yes. /wp-admin/ should be disallowed — it should never appear in search results and is a common target for brute force attacks. However, /wp-includes/ and /wp-content/ should be allowed so Googlebot can load WordPress assets for rendering."),
            ("How do I check if Googlebot can render my pages?", "Use Google Search Console's URL Inspection tool → 'Test Live URL' → View rendered page. GSC shows exactly what Googlebot sees when rendering your page and reports any blocked resources."),
            ("Does blocking JS in robots.txt save crawl budget?", "No longer a valid strategy. Crawl budget savings from blocking assets are negligible, while the rendering penalty (Google seeing a broken page) is significant. Allow all rendering resources and control indexing with noindex meta tags or canonical tags instead."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator tool"),
            ("/fix/robots/accidental-disallow-all/", "Fix: Accidentally blocking all crawlers"),
        ],
    },
    {
        "slug": "blocking-ai-bots",
        "title": "Fix: robots.txt Missing AI Bot Directives",
        "meta_desc": "How to configure robots.txt for AI crawlers — GPTBot, ClaudeBot, PerplexityBot, and Bytespider. Allow or block AI training crawlers with exact robots.txt syntax.",
        "keywords": "block gptbot robots txt, block claudebot, allow ai crawlers robots txt, gptbot robots txt fix",
        "intro": "AI training crawlers like GPTBot (OpenAI), ClaudeBot (Anthropic), PerplexityBot, and Bytespider operate independently of Google. A robots.txt that only addresses <code>User-agent: *</code> and <code>Googlebot</code> does not explicitly address these crawlers. This guide covers both blocking and allowing them.",
        "problem": "Many sites either want to allow AI crawlers (for GEO — Generative Engine Optimisation, getting cited in AI answers) or block them (for content protection). A robots.txt without explicit AI crawler directives has ambiguous intent. Some AI crawlers respect <code>User-agent: *</code> rules. Others only act on explicit user-agent entries. Missing directives means inconsistent handling.",
        "fix_label": "robots.txt — Allow AI Crawlers (GEO strategy)",
        "fix_code": """User-agent: *
Allow: /

# Allow AI crawlers explicitly for GEO (AI search citation)
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml""",
        "fix_explanation": "Use <code>Allow: /</code> for AI crawlers you want to allow for AI search visibility, or <code>Disallow: /</code> to block them from training data. GPTBot is OpenAI's crawler. ClaudeBot is Anthropic's. PerplexityBot is used by Perplexity AI. Google-Extended controls Google's AI training separately from Googlebot.",
        "faqs": [
            ("Should I allow or block AI crawlers?", "It depends on your goals. Allow them if you want your content cited in AI answers (GEO strategy) — sites that block AI crawlers are excluded from ChatGPT, Claude, and Perplexity's knowledge base. Block them if your content is proprietary and you're concerned about training data use."),
            ("Does blocking GPTBot stop ChatGPT from knowing about my site?", "It stops future training data collection, but ChatGPT's existing knowledge base already contains your content if it was crawled before you added the block. Blocking prevents future training updates, not retroactive removal."),
            ("What is Google-Extended?", "Google-Extended is a separate user agent that controls whether your content is used for Google's AI products (Bard/Gemini training, AI Overviews). Setting Disallow for Google-Extended while allowing Googlebot means Google can index your site normally but cannot use your content for AI training."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator — live AI bot coverage check"),
            ("/fix/robots/missing-sitemap-reference/", "Fix: Missing sitemap in robots.txt"),
        ],
    },
    {
        "slug": "missing-sitemap-reference",
        "title": "Fix: robots.txt Missing Sitemap Reference",
        "meta_desc": "How to add a Sitemap: directive to robots.txt so all search engines and AI crawlers can discover your sitemap automatically. Exact fix for missing sitemap in robots.txt.",
        "keywords": "robots txt missing sitemap, add sitemap to robots txt, sitemap directive robots txt",
        "intro": "A <code>Sitemap:</code> directive in robots.txt tells every crawler — Google, Bing, AI bots — where your sitemap lives. Without it, crawlers must discover your sitemap by following links or by you manually submitting it in each search console. Adding the directive is a 30-second fix that improves crawl efficiency for every crawler simultaneously.",
        "problem": "Many sites submit their sitemap to Google Search Console manually but never add the <code>Sitemap:</code> directive to robots.txt. This means Bing, DuckDuckGo, AI crawlers, and other search engines must discover the sitemap independently. For sites with multiple sitemaps (main + SEO content), all sitemaps should be referenced.",
        "fix_label": "robots.txt — Add Sitemap directive",
        "fix_code": """User-agent: *
Allow: /

# Reference all sitemaps — main and SEO content
Sitemap: https://yourdomain.com/sitemap.xml
Sitemap: https://yourdomain.com/sitemap-seo.xml

# Add more as needed:
# Sitemap: https://yourdomain.com/sitemap-blog.xml
# Sitemap: https://yourdomain.com/sitemap-products.xml""",
        "fix_explanation": "Add a <code>Sitemap:</code> line for every sitemap file. Use the full absolute URL (https://). The Sitemap directive is not tied to any User-agent block — place it at the end of the file, after all User-agent/Allow/Disallow rules. Multiple Sitemap directives are valid.",
        "faqs": [
            ("Do I still need to submit sitemaps to Google Search Console?", "Yes — GSC submission and robots.txt reference serve different purposes. GSC submission tells Google to crawl the sitemap immediately. The robots.txt Sitemap directive helps all other crawlers discover it automatically and is read every time any crawler reads your robots.txt."),
            ("Where in robots.txt should the Sitemap directive go?", "The Sitemap directive is global — it applies to all crawlers and is not placed inside a User-agent block. Convention is to put it at the end of the file after all User-agent sections. Some validators flag it as an error if placed inside a User-agent block."),
            ("Can I reference multiple sitemaps in robots.txt?", "Yes. Add one Sitemap: line per sitemap file. This is the correct approach for sites with separate sitemaps for main pages, blog posts, SEO content pages, or images."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator tool"),
            ("/fix/robots/accidental-disallow-all/", "Fix: Accidentally blocking all crawlers"),
        ],
    },
    {
        "slug": "wildcard-too-broad",
        "title": "Fix: robots.txt Wildcard Pattern Blocking Too Many Pages",
        "meta_desc": "How to fix overly broad wildcard patterns in robots.txt that unintentionally block product pages, blog posts, or category pages from Google indexing.",
        "keywords": "robots txt wildcard too broad, robots txt pattern blocking wrong pages, fix robots txt disallow pattern",
        "intro": "Wildcard patterns in robots.txt use <code>*</code> (match any sequence) and <code>$</code> (match end of URL). A pattern like <code>Disallow: /*/page/</code> intended to block pagination may also block <code>/products/featured-page/overview/</code> if the URL structure matches the pattern.",
        "problem": "Robots.txt pattern matching is literal string matching with wildcards — not regex. Many developers write patterns assuming regex behaviour. <code>Disallow: /*.pdf$</code> correctly blocks PDF files. But <code>Disallow: /search*</code> blocks any URL containing /search anywhere in the path, including <code>/search-engine-marketing/</code> blog posts.",
        "fix_label": "Test your patterns before deploying",
        "fix_code": """# OVERLY BROAD — blocks /search-engine-tips/, /search-results/, etc:
# Disallow: /search

# CORRECT — only blocks /search and /search?q= style URLs:
Disallow: /search$
Disallow: /search?

# OVERLY BROAD — blocks all URLs with ? anywhere:
# Disallow: /*?

# CORRECT — only block specific query parameters:
Disallow: /?sort=
Disallow: /?filter=
Disallow: /?ref=""",
        "fix_explanation": "Use the ConfigClarity robots.txt Validator's URL Tester to test your patterns against specific URLs before deploying. The tester shows BLOCKED or ALLOWED for any URL against any bot, using the exact same parsing logic that Googlebot uses.",
        "faqs": [
            ("Does robots.txt support full regex?", "No. robots.txt only supports two wildcards: * (match any sequence of characters) and $ (match end of URL). Full regex like character classes [a-z], alternatives (foo|bar), or quantifiers {2,5} are not supported. Test your patterns carefully."),
            ("How do I test if a robots.txt pattern is blocking a specific URL?", "Use ConfigClarity's robots.txt Validator — paste your robots.txt and use the URL Tester to check any path against any bot. Google Search Console's URL Inspection also shows 'Blocked by robots.txt' for specific URLs."),
            ("What is the difference between Disallow: /search and Disallow: /search$?", "Disallow: /search blocks any URL starting with /search — including /search-results/, /search-engine-tips/, /search?q=. Disallow: /search$ only blocks the exact URL /search with nothing after it. Use $ to anchor the end of the pattern."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator with URL Tester"),
            ("/fix/robots/conflicting-rules/", "Fix: Conflicting Allow/Disallow rules"),
        ],
    },
    {
        "slug": "conflicting-rules",
        "title": "Fix: Conflicting robots.txt Allow and Disallow Rules",
        "meta_desc": "How to fix conflicting Allow and Disallow rules in robots.txt. When Allow and Disallow match the same URL, the most specific rule wins — exact Google behaviour explained.",
        "keywords": "robots txt conflicting rules, allow disallow conflict robots txt, robots txt rule priority",
        "intro": "When a URL matches both an Allow and a Disallow rule in robots.txt, most crawlers apply the most-specific-rule-wins precedence — the rule with the longer matching path takes priority. Understanding this prevents accidental blocks and allows precise control over which URLs are crawled.",
        "problem": "A common pattern is to disallow a directory but allow specific files within it. For example, <code>Disallow: /private/</code> with <code>Allow: /private/public-page.html</code>. The Allow rule is more specific (longer path match) so it takes precedence — the public page is crawlable. But if both rules are equal length, behaviour varies by crawler.",
        "fix_label": "robots.txt — Conflict resolution examples",
        "fix_code": """# CORRECT — Allow takes precedence (more specific path):
User-agent: *
Disallow: /admin/
Allow: /admin/public-status/   # This page IS crawled (longer match)

# CORRECT — Disallow takes precedence:
User-agent: *
Allow: /products/
Disallow: /products/draft/      # These pages NOT crawled (longer match)

# AMBIGUOUS — equal length, crawler-dependent:
User-agent: *
Disallow: /page
Allow: /page   # Googlebot: Allow wins. Others: varies.
# FIX: Use explicit longer path to remove ambiguity:
Disallow: /page$
Allow: /page/public/""",
        "fix_explanation": "For Googlebot: when Allow and Disallow match a URL at the same path length, Allow wins. For other crawlers, behaviour is undefined. Eliminate ambiguity by making the intended-to-win rule more specific (longer). Use the URL Tester in ConfigClarity's robots.txt Validator to verify your rules behave as expected.",
        "faqs": [
            ("Does Allow override Disallow in robots.txt?", "Not unconditionally. The most-specific rule (longest matching path) wins. If Allow and Disallow have the same path length and both match a URL, Googlebot gives precedence to Allow. Bing and other crawlers may handle this differently."),
            ("What is the correct order for Allow and Disallow rules?", "Rule order does not affect precedence in Googlebot — specificity wins, not order. However, for clarity and compatibility with older crawlers that use first-match semantics, put more specific rules before general ones and put Allow rules before their corresponding Disallow rules."),
            ("How do I test which rule wins for a specific URL?", "Paste your robots.txt into ConfigClarity's robots.txt Validator and use the URL Tester — enter any path and select a user agent. The tool shows BLOCKED or ALLOWED and which rule matched."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator with URL Tester"),
            ("/fix/robots/wildcard-too-broad/", "Fix: Wildcard pattern too broad"),
        ],
    },
    {
        "slug": "crawl-delay-too-high",
        "title": "Fix: robots.txt Crawl-Delay Too High",
        "meta_desc": "How to fix crawl-delay in robots.txt that is set too high, reducing how quickly Google indexes new content. Recommended crawl-delay values and when to use them.",
        "keywords": "robots txt crawl delay too high, crawl-delay robots txt fix, reduce crawl delay googlebot",
        "intro": "The <code>Crawl-delay</code> directive in robots.txt tells crawlers to wait N seconds between requests. Setting it too high (10+ seconds) slows how quickly new content is indexed and can cause Googlebot to crawl fewer pages per day. Google does not officially support Crawl-delay — use Google Search Console's crawl rate settings instead.",
        "problem": "Crawl-delay was added to robots.txt to protect servers from aggressive crawling. However, Google ignores the Crawl-delay directive — it manages crawl rate internally based on server response times and your GSC settings. Setting a high Crawl-delay only affects crawlers that honour it (Bing, some smaller bots) without protecting against Google's crawl load.",
        "fix_label": "Remove Crawl-delay or set low for compatibility",
        "fix_code": """# BEFORE — high crawl-delay slows indexing for crawlers that honour it:
# User-agent: *
# Crawl-delay: 30

# AFTER — remove crawl-delay (Google ignores it, others over-throttle):
User-agent: *
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml

# If you need to throttle Bing specifically, use a low value:
User-agent: Bingbot
Crawl-delay: 2""",
        "fix_explanation": "Remove <code>Crawl-delay</code> for <code>User-agent: *</code>. To control Googlebot's crawl rate, use Google Search Console → Settings → Crawl rate settings. For Bing specifically, a Crawl-delay of 1–2 seconds is reasonable. Values above 10 seconds significantly reduce indexing speed for the crawlers that honour the directive.",
        "faqs": [
            ("Does Google respect Crawl-delay in robots.txt?", "No. Google officially ignores the Crawl-delay directive. Googlebot manages crawl rate based on server response times and your Google Search Console crawl rate settings."),
            ("How do I slow down Googlebot without Crawl-delay?", "Use Google Search Console → Settings → Crawl rate. You can set it to 'Limit Google's maximum crawl rate' and adjust the slider. This is the only way to affect Googlebot's crawl rate."),
            ("What is a reasonable Crawl-delay value for Bing?", "For most sites: 1–3 seconds. Bing's default crawl rate is already conservative. A Crawl-delay of 1 is a safe default that limits any server impact without significantly slowing indexing."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator tool"),
            ("/fix/robots/missing-sitemap-reference/", "Fix: Missing sitemap reference"),
        ],
    },
    {
        "slug": "case-sensitive-path",
        "title": "Fix: robots.txt Case-Sensitive Path Issues",
        "meta_desc": "robots.txt paths are case-sensitive on Linux servers. Disallow: /Admin/ does not block /admin/ — how to fix case sensitivity issues in robots.txt.",
        "keywords": "robots txt case sensitive, robots txt case sensitivity, disallow path case fix",
        "intro": "robots.txt paths are case-sensitive on Linux servers. <code>Disallow: /Admin/</code> does not block <code>/admin/</code>. If your server serves URLs at both cases or if a URL in your robots.txt does not match the actual case of the path, the directive has no effect.",
        "problem": "CMS platforms like WordPress serve paths in lowercase by default. But some content management systems or frameworks generate URLs with mixed case (camelCase, PascalCase) or inconsistent capitalisation. If your robots.txt blocks <code>/Products/</code> but the actual URL is <code>/products/</code>, the Disallow rule never fires.",
        "fix_label": "Match exact case of your live URLs",
        "fix_code": """# Check your actual URL structure first:
# curl -sI https://yourdomain.com/Admin/ | grep -i location
# (If it redirects to /admin/, use /admin/ in robots.txt)

# WRONG — wrong case:
# Disallow: /Admin/
# Disallow: /WordPress/wp-admin/

# CORRECT — match actual URL case:
Disallow: /admin/
Disallow: /wp-admin/
Disallow: /wp-login.php""",
        "fix_explanation": "Use ConfigClarity's robots.txt Validator URL Tester to test paths with different cases. Verify your actual URL paths by checking your server's access logs or by using <code>curl -sI https://yourdomain.com/PATH/</code> to see if the server redirects to a differently-cased URL.",
        "faqs": [
            ("Are robots.txt directives case-sensitive?", "The paths in Disallow and Allow directives are case-sensitive. Googlebot treats /Admin/ and /admin/ as different paths. The directives themselves (User-agent, Disallow, Allow) are case-insensitive."),
            ("Does capitalisation matter for User-agent in robots.txt?", "No. User-agent, Disallow, Allow, Crawl-delay, and Sitemap directives are case-insensitive. User-agent: Googlebot, USER-AGENT: Googlebot, and user-agent: googlebot are all equivalent."),
            ("How do I check the actual case of my site's URLs?", "Run curl -sI https://yourdomain.com/YOURPATH/ and check the Location header in the response. If the server redirects to a lowercase URL, use that lowercase path in robots.txt."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator with URL Tester"),
            ("/fix/robots/wildcard-too-broad/", "Fix: Wildcard pattern too broad"),
        ],
    },
    {
        "slug": "noindex-vs-disallow",
        "title": "Fix: Confusion Between robots.txt Disallow and Noindex Meta Tag",
        "meta_desc": "robots.txt Disallow prevents crawling but does not remove pages from Google index. Noindex meta tag prevents indexing but allows crawling. When to use each and why using both is a mistake.",
        "keywords": "robots txt disallow vs noindex, robots noindex difference, disallow prevents indexing wrong",
        "intro": "Disallow in robots.txt prevents Googlebot from crawling a page, but it does not remove it from Google's index. The noindex meta tag prevents indexing but requires the page to be crawlable. Using both simultaneously — <code>Disallow</code> in robots.txt and <code>noindex</code> on the page — is a common mistake that prevents the noindex directive from ever being read.",
        "problem": "If a URL is listed in robots.txt with <code>Disallow</code>, Googlebot cannot access the page. If Googlebot cannot access the page, it cannot read the <code>noindex</code> meta tag on the page. The result: the page may remain in Google's index indefinitely as a URL-only entry (no snippet, no content) because Google saw the URL via links or a sitemap but cannot fetch the noindex instruction.",
        "fix_label": "Use Disallow OR Noindex — not both",
        "fix_code": """# TO PREVENT CRAWLING (page stays in index as URL-only if linked):
User-agent: *
Disallow: /internal-tool/

# TO REMOVE FROM INDEX (requires page to be crawlable):
# Add to page <head> — DON'T block in robots.txt:
# <meta name="robots" content="noindex, follow">
# User-agent: * Allow: /internal-tool/  ← allow crawling so noindex is read

# TO FULLY REMOVE — if already Disallowed, remove Disallow + add noindex:
# 1. Remove from robots.txt: (delete Disallow: /page/)
# 2. Add to page: <meta name="robots" content="noindex">
# 3. Wait for Googlebot to crawl and process the noindex""",
        "fix_explanation": "Choose one mechanism. Use robots.txt Disallow for pages that should never be crawled (admin tools, API endpoints, private files). Use noindex meta tag for pages that should be crawled but not shown in search results (thank you pages, filtered category pages, duplicate content). Never use both on the same URL.",
        "faqs": [
            ("Can I use both robots.txt Disallow and noindex at the same time?", "You can, but it defeats the purpose. If Disallow blocks crawling, Googlebot cannot read the noindex tag. The page may remain indexed as a URL-only entry. To remove a page from the index, the page must be crawlable so Googlebot can read the noindex instruction."),
            ("Does Disallow in robots.txt remove a page from Google?", "No. Disallow prevents crawling but does not remove already-indexed pages from search results. A page that was previously indexed and is now Disallowed may remain in the index indefinitely as a URL-only entry (no title, no snippet) until Googlebot re-evaluates it."),
            ("What is the fastest way to remove a page from Google?", "The fastest method is Google Search Console's URL Removal tool for temporary suppression (6 months), combined with adding a noindex meta tag for permanent removal. The noindex tag requires the page to be crawlable — ensure it is not blocked in robots.txt."),
        ],
        "related_links": [
            ("/robots/", "robots.txt Validator tool"),
            ("/fix/robots/accidental-disallow-all/", "Fix: Accidentally blocking all crawlers"),
        ],
    },
]

# ─── 6 CMS PAGES ───────────────────────────────────────────────────────────────

CMS_PAGES = [
    {
        "cms": "wordpress",
        "title": "WordPress robots.txt — Correct Configuration Guide",
        "meta_desc": "The correct robots.txt for WordPress sites. Block wp-admin, allow wp-content, configure for WooCommerce, Yoast SEO sitemap reference, and AI crawler permissions.",
        "keywords": "wordpress robots txt, wp-admin disallow robots txt, wordpress robots txt fix, yoast seo sitemap robots",
        "content": """<p>WordPress generates a virtual robots.txt by default, but many hosting providers replace it with a static file. The correct WordPress robots.txt blocks admin paths, allows assets, and references the Yoast SEO or RankMath generated sitemap.</p>

<h2>Correct WordPress robots.txt</h2>
<pre>User-agent: *
Allow: /wp-content/uploads/
Disallow: /wp-admin/
Disallow: /wp-login.php
Disallow: /xmlrpc.php
Disallow: /?s=
Disallow: /search$
Disallow: /trackback/
Disallow: /feed/
Disallow: /comments/

# AI crawlers (allow for GEO / citation in AI search)
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

# Sitemap (replace with your Yoast or RankMath sitemap URL)
Sitemap: https://yourdomain.com/sitemap_index.xml</pre>

<h2>Key Rules Explained</h2>
<p><strong>Allow /wp-content/uploads/</strong> — This must be explicitly allowed. If you have a broad Disallow rule, add this Allow to ensure Googlebot can load images.<br>
<strong>Disallow /wp-admin/</strong> — The admin dashboard should never be indexed.<br>
<strong>Disallow /?s=</strong> — WordPress search results (/search?s=query) should not be indexed — duplicate content risk.<br>
<strong>Disallow /feed/</strong> — RSS feeds are not useful in search results and consume crawl budget.</p>""",
        "faqs": [
            ("How do I edit WordPress robots.txt?", "Three ways: (1) Yoast SEO → Tools → File Editor → robots.txt, (2) RankMath → General Settings → Edit Robots.txt, (3) Create a physical robots.txt file in your WordPress root directory which overrides the virtual one."),
            ("Should I block /wp-includes/ in WordPress robots.txt?", "No. /wp-includes/ contains core WordPress scripts and styles that Googlebot needs to render your pages. Blocking it causes Google Search Console to report rendering errors."),
            ("Why is my WordPress sitemap not being found?", "Ensure the Sitemap: line in robots.txt points to your actual sitemap URL. Yoast SEO uses sitemap_index.xml. RankMath uses sitemap_index.xml. The All in One SEO plugin uses sitemap.xml. Check which plugin is active and use the correct URL."),
        ],
    },
    {
        "cms": "shopify",
        "title": "Shopify robots.txt — Correct Configuration Guide",
        "meta_desc": "How to customize Shopify's robots.txt. Shopify generates robots.txt automatically but allows customization via liquid templates. Block checkout, cart, and search pages.",
        "keywords": "shopify robots txt, shopify robots txt customize, shopify disallow checkout cart",
        "content": """<p>Shopify generates a robots.txt file automatically and does not allow direct file editing. Since Shopify 2021, you can customise robots.txt using a liquid template: <code>templates/robots.txt.liquid</code>.</p>

<h2>Default Shopify robots.txt (Generated)</h2>
<pre>User-agent: *
Disallow: /admin
Disallow: /cart
Disallow: /orders
Disallow: /checkouts/
Disallow: /checkout
Disallow: /cgi-bin
Disallow: /search?
Disallow: /apple-app-site-association
Disallow: /.well-known/shopify/monorail</pre>

<h2>Customising via liquid template</h2>
<pre># templates/robots.txt.liquid
{% for group in robots.default_groups %}
  {{ group }}
{% endfor %}

# Add AI crawler directives:
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

Sitemap: {{ shop.url }}/sitemap.xml</pre>

<p>The <code>robots.default_groups</code> loop outputs Shopify's default rules. You then add custom directives below. This preserves Shopify's required blocks while adding your customisations.</p>""",
        "faqs": [
            ("Can I edit Shopify's robots.txt directly?", "Not through the file manager. Shopify generates robots.txt automatically. To customise it, go to Online Store → Themes → Edit Code → Create new template → robots.txt.liquid. This requires a 2.0 theme that supports app blocks."),
            ("Should I block /collections/ in Shopify robots.txt?", "No. Collection pages are important for SEO — they are the category pages that rank for broad product terms. Blocking them removes your product category pages from Google. Only block /collections/?sort_by= and /collections/?filter= to prevent duplicate content from faceted navigation."),
            ("Does Shopify automatically add a sitemap to robots.txt?", "Yes. Shopify's auto-generated robots.txt includes a Sitemap: line pointing to your store's sitemap.xml. If you override with a liquid template, include {{ shop.url }}/sitemap.xml yourself."),
        ],
    },
    {
        "cms": "nextjs",
        "title": "Next.js robots.txt — Correct Configuration",
        "meta_desc": "How to add and configure robots.txt in Next.js. Use next-sitemap, the App Router metadata API, or a static file. Exact configuration for all three methods.",
        "keywords": "nextjs robots txt, next js robots txt configuration, next-sitemap robots txt, app router robots",
        "content": """<p>Next.js supports three approaches for robots.txt: a static file in <code>/public/</code>, the App Router Metadata API (<code>app/robots.ts</code>), or the <code>next-sitemap</code> package for automatic generation.</p>

<h2>Method 1: App Router — app/robots.ts (Recommended)</h2>
<pre>// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/api/', '/admin/', '/_next/'],
    },
    sitemap: 'https://yourdomain.com/sitemap.xml',
  }
}</pre>

<h2>Method 2: Static file — public/robots.txt</h2>
<pre>User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

Sitemap: https://yourdomain.com/sitemap.xml</pre>

<h2>What to Disallow in Next.js</h2>
<p><code>/api/</code> — API routes should not be indexed. <code>/admin/</code> or <code>/dashboard/</code> — authenticated routes. <code>/_next/</code> — Next.js build assets (note: usually already non-indexable but explicit is better).</p>""",
        "faqs": [
            ("Should I block /_next/ in Next.js robots.txt?", "Generally no. /_next/static/ contains CSS, JS, and image files that Googlebot needs to render your pages. Blocking it prevents rendering. /_next/ as a whole is not normally a path that would appear in search results, but allow it for asset loading."),
            ("How do I generate robots.txt automatically in Next.js?", "Use the next-sitemap package: add robots: true to next-sitemap.config.js. It generates both sitemap.xml and robots.txt on each build. Alternatively, use the App Router robots.ts file which Next.js serves at /robots.txt automatically."),
            ("Does Next.js serve robots.txt automatically?", "With the App Router and a robots.ts file in /app — yes. With the Pages Router, place a static robots.txt in the /public directory and Next.js serves it at /robots.txt automatically."),
        ],
    },
    {
        "cms": "nuxt",
        "title": "Nuxt.js robots.txt — Correct Configuration",
        "meta_desc": "How to configure robots.txt in Nuxt.js using @nuxtjs/robots module or static files. Disallow API routes, add sitemap reference, configure for SSR and static generation.",
        "keywords": "nuxt robots txt, nuxtjs robots configuration, @nuxtjs/robots module",
        "content": """<p>Nuxt.js serves robots.txt from the <code>/public/</code> directory (Nuxt 3) or <code>/static/</code> directory (Nuxt 2). The <code>@nuxtjs/robots</code> module provides dynamic configuration via <code>nuxt.config.ts</code>.</p>

<h2>Method 1: Static file — public/robots.txt (Nuxt 3)</h2>
<pre>User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: https://yourdomain.com/sitemap.xml</pre>

<h2>Method 2: @nuxtjs/robots module (nuxt.config.ts)</h2>
<pre>// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxtjs/robots'],
  robots: {
    rules: [
      { UserAgent: '*' },
      { Allow: '/' },
      { Disallow: '/admin/' },
      { Disallow: '/api/' },
      { Sitemap: 'https://yourdomain.com/sitemap.xml' }
    ]
  }
})</pre>""",
        "faqs": [
            ("Where does robots.txt go in Nuxt 3?", "Place it in the /public/ directory as public/robots.txt. Nuxt 3 serves all files in /public/ at the root URL, so public/robots.txt is accessible at https://yourdomain.com/robots.txt."),
            ("Does @nuxtjs/robots work with SSR and static generation?", "Yes. The module works with both SSR (server-side rendered) and static generation (nuxt generate). For static sites, it generates a static robots.txt file during the build process."),
            ("How do I reference a Nuxt sitemap in robots.txt?", "If you're using @nuxtjs/sitemap, the default sitemap URL is /sitemap.xml or /sitemap_index.xml. Add Sitemap: https://yourdomain.com/sitemap.xml to your robots.txt or in the module configuration."),
        ],
    },
    {
        "cms": "gatsby",
        "title": "Gatsby robots.txt — Correct Configuration",
        "meta_desc": "How to configure robots.txt in Gatsby using gatsby-plugin-robots-txt. Block draft pages, add sitemap reference, configure for Netlify and Vercel deployments.",
        "keywords": "gatsby robots txt, gatsby-plugin-robots-txt, gatsby robots txt configuration",
        "content": """<p>Gatsby generates robots.txt using the <code>gatsby-plugin-robots-txt</code> plugin or by placing a static file in the <code>/static/</code> directory. The plugin supports environment-specific configuration — useful for staging vs production.</p>

<h2>Method 1: gatsby-plugin-robots-txt (Recommended)</h2>
<pre>// gatsby-config.js
{
  resolve: 'gatsby-plugin-robots-txt',
  options: {
    host: 'https://yourdomain.com',
    sitemap: 'https://yourdomain.com/sitemap-index.xml',
    policy: [
      { userAgent: '*', allow: '/' },
      { userAgent: 'GPTBot', allow: '/' },
      { userAgent: 'ClaudeBot', allow: '/' }
    ]
  }
}</pre>

<h2>Environment-Specific: Block Staging</h2>
<pre>// gatsby-config.js
const robotsPolicy = process.env.NODE_ENV === 'production'
  ? [{ userAgent: '*', allow: '/' }]
  : [{ userAgent: '*', disallow: ['/'] }]

{
  resolve: 'gatsby-plugin-robots-txt',
  options: { policy: robotsPolicy }
}</pre>""",
        "faqs": [
            ("Where does robots.txt go in Gatsby without a plugin?", "Place a static robots.txt file in the /static/ directory. Gatsby copies all files in /static/ to the root of the build output, making static/robots.txt accessible at /robots.txt."),
            ("How do I block Gatsby staging from being indexed?", "Use environment-based configuration in gatsby-plugin-robots-txt with Disallow: / for non-production environments. Or add the X-Robots-Tag: noindex header in your staging server/CDN configuration — this is more reliable than robots.txt for preventing accidental indexing."),
            ("What is the correct sitemap URL for Gatsby?", "With gatsby-plugin-sitemap, the default output is /sitemap-index.xml (Gatsby 4+) or /sitemap.xml (Gatsby 3 and earlier). Check your gatsby-config.js sitemap plugin output option to confirm."),
        ],
    },
    {
        "cms": "hugo",
        "title": "Hugo robots.txt — Correct Configuration",
        "meta_desc": "How to generate and configure robots.txt in Hugo using templates. Enable custom robots.txt in config.toml, add sitemap reference, configure for Hugo static site deployment.",
        "keywords": "hugo robots txt, hugo robots txt template, hugo config robots",
        "content": """<p>Hugo does not generate a robots.txt by default. To enable it, set <code>enableRobotsTXT = true</code> in <code>config.toml</code>. Hugo then uses the <code>layouts/robots.txt</code> template to generate the file, or falls back to a minimal default.</p>

<h2>Enable robots.txt in config.toml</h2>
<pre># config.toml
baseURL = "https://yourdomain.com"
enableRobotsTXT = true</pre>

<h2>Custom template — layouts/robots.txt</h2>
<pre>User-agent: *
{{ if hugo.IsProduction }}Allow: /{{ else }}Disallow: /{{ end }}
Disallow: /admin/
Disallow: /draft/

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

Sitemap: {{ "sitemap.xml" | absURL }}</pre>

<p>The <code>hugo.IsProduction</code> check ensures staging builds disallow all crawling while production builds allow it — preventing staging content from being indexed if it's accidentally deployed publicly.</p>""",
        "faqs": [
            ("How do I enable robots.txt generation in Hugo?", "Set enableRobotsTXT = true in config.toml (or hugo.toml in Hugo 0.110+). Hugo will then generate /robots.txt from layouts/robots.txt if it exists, or use an internal default template that generates Allow: / for all bots."),
            ("Where does Hugo output robots.txt?", "Hugo outputs robots.txt to the /public/ directory root during hugo build. The file is at public/robots.txt which maps to https://yourdomain.com/robots.txt after deployment."),
            ("How do I add a sitemap reference to Hugo's robots.txt?", "In your layouts/robots.txt template, use: Sitemap: {{ \"sitemap.xml\" | absURL }}. Hugo's absURL function prepends your baseURL, so it generates the correct absolute URL. Hugo generates sitemap.xml automatically."),
        ],
    },
]

# ─── 6 AI BOT PAGES ─────────────────────────────────────────────────────────────

AI_BOT_PAGES = [
    ("block-gptbot", "GPTBot", "How to Block GPTBot (OpenAI) in robots.txt",
     "Exact robots.txt syntax to block OpenAI's GPTBot from crawling your site for ChatGPT training data.",
     "User-agent: GPTBot\nDisallow: /"),
    ("block-claudebot", "ClaudeBot", "How to Block ClaudeBot (Anthropic) in robots.txt",
     "Exact robots.txt syntax to block Anthropic's ClaudeBot from crawling your site for Claude training data.",
     "User-agent: ClaudeBot\nDisallow: /"),
    ("block-perplexitybot", "PerplexityBot", "How to Block PerplexityBot in robots.txt",
     "Exact robots.txt syntax to block PerplexityBot from crawling your site for Perplexity AI's search index.",
     "User-agent: PerplexityBot\nDisallow: /"),
    ("block-bytespider", "Bytespider", "How to Block Bytespider (ByteDance) in robots.txt",
     "Exact robots.txt to block Bytespider — ByteDance's AI training crawler — from your site.",
     "User-agent: Bytespider\nDisallow: /"),
    ("block-all-ai-bots", "All AI Crawlers", "How to Block All AI Crawlers in robots.txt",
     "Block all AI training crawlers — GPTBot, ClaudeBot, PerplexityBot, Bytespider, Google-Extended — with one robots.txt block.",
     "User-agent: GPTBot\nDisallow: /\n\nUser-agent: ClaudeBot\nDisallow: /\n\nUser-agent: PerplexityBot\nDisallow: /\n\nUser-agent: Bytespider\nDisallow: /\n\nUser-agent: Google-Extended\nDisallow: /\n\nUser-agent: CCBot\nDisallow: /"),
    ("allow-ai-bots", "AI Crawlers (Allow)", "How to Allow AI Crawlers in robots.txt (GEO Strategy)",
     "Explicitly allow GPTBot, ClaudeBot, and PerplexityBot in robots.txt to get your content cited in AI search answers.",
     "User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /"),
]

# ─── 4 CONCEPT PAGES ──────────────────────────────────────────────────────────

CONCEPT_PAGES = [
    {
        "slug": "robots-txt-vs-noindex",
        "title": "robots.txt Disallow vs Noindex Meta Tag — What's the Difference?",
        "meta_desc": "robots.txt Disallow prevents crawling. Noindex prevents indexing. Using both together is a mistake. Complete guide to when to use each.",
        "keywords": "robots txt vs noindex, disallow vs noindex meta tag, robots txt noindex difference",
    },
    {
        "slug": "robots-txt-cheat-sheet",
        "title": "robots.txt Syntax Cheat Sheet — All Directives Explained",
        "meta_desc": "Complete robots.txt syntax reference: User-agent, Allow, Disallow, Crawl-delay, Sitemap wildcards (* and $), and common patterns. Copy-paste ready.",
        "keywords": "robots txt cheat sheet, robots txt syntax, robots txt directives, robots txt wildcards",
    },
    {
        "slug": "what-is-crawl-budget",
        "title": "What is Crawl Budget? — How Google Decides Which Pages to Crawl",
        "meta_desc": "Crawl budget is Google's limit on how many pages it crawls per site per day. How to optimise it with robots.txt, sitemap priorities, and internal linking.",
        "keywords": "what is crawl budget, crawl budget optimization, google crawl budget, crawl budget robots txt",
    },
    {
        "slug": "robots-txt-for-ecommerce",
        "title": "robots.txt for Ecommerce Sites — Block Faceted Navigation, Allow Products",
        "meta_desc": "How to configure robots.txt for ecommerce sites. Block filtered category URLs, allow product pages, handle pagination, and prevent duplicate content crawling.",
        "keywords": "robots txt ecommerce, robots txt faceted navigation, robots txt woocommerce shopify, block filter urls robots",
    },
]

def build_ai_bot_page(slug, bot_name, title, meta_desc, fix_code):
    is_allow = "allow" in slug
    action = "Allow" if is_allow else "Block"
    color = "var(--green)" if is_allow else "var(--red)"
    reasoning = (
        "Allowing AI crawlers explicitly means your content is eligible to be cited in AI search answers (GEO — Generative Engine Optimisation). Sites that are blocked from AI crawlers are excluded from ChatGPT, Claude, and Perplexity's knowledge base."
        if is_allow else
        f"Blocking {bot_name} prevents your content from being used in AI training datasets. This does not remove existing knowledge — it only prevents future crawling. Content already in training datasets before you add this block is not retroactively removed."
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — ConfigClarity</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="robots txt {bot_name.lower()}, {action.lower()} {bot_name.lower()} crawling, ai bot robots txt">
  <link rel="canonical" href="https://configclarity.dev/fix/robots/{slug}/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle",
    "headline":"{title}","url":"https://configclarity.dev/fix/robots/{slug}/",
    "description":"{meta_desc}",
    "author":{{"@type":"Organization","name":"MetricLogic"}}
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"ConfigClarity","item":"https://configclarity.dev"}},
    {{"@type":"ListItem","position":2,"name":"Fix Guides","item":"https://configclarity.dev/fix/"}},
    {{"@type":"ListItem","position":3,"name":"robots.txt","item":"https://configclarity.dev/fix/robots/"}},
    {{"@type":"ListItem","position":4,"name":"{title}","item":"https://configclarity.dev/fix/robots/{slug}/"}}
  ]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/robots/">robots.txt</a> › {title}
  </div>
  <div class="content">
    <h1>{title}</h1>
    <p>{meta_desc}</p>
    <h2>robots.txt Syntax — {action} {bot_name}</h2>
    <div class="fix-box" style="border-color:{color}">
      <div class="label" style="color:{color}">COPY-PASTE READY</div>
      <pre>{fix_code}</pre>
    </div>
    <h2>What This Does</h2>
    <p>{reasoning}</p>
    <div class="cta-box">
      <p>Validate your robots.txt live — check AI bot coverage and get a corrected file.</p>
      <a href="/robots/" class="cta-btn">Open robots.txt Validator →</a>
    </div>
    <h2>Related Guides</h2>
    <ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);">
      <li><a href="/fix/robots/blocking-ai-bots/">Fix: robots.txt missing AI bot directives</a></li>
      <li><a href="/fix/robots/missing-sitemap-reference/">Fix: missing sitemap reference</a></li>
      <li><a href="/robots/">robots.txt Validator tool</a></li>
    </ul>
  </div>
{FOOTER}
</body>
</html>"""

def build_concept_page(term):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{term['title']} — ConfigClarity</title>
  <meta name="description" content="{term['meta_desc']}">
  <meta name="keywords" content="{term['keywords']}">
  <link rel="canonical" href="https://configclarity.dev/fix/robots/{term['slug']}/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle",
    "headline":"{term['title']}","url":"https://configclarity.dev/fix/robots/{term['slug']}/",
    "description":"{term['meta_desc']}",
    "author":{{"@type":"Organization","name":"MetricLogic"}}
  }}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb">
    <a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/robots/">robots.txt</a> › {term['title']}
  </div>
  <div class="content">
    <h1>{term['title']}</h1>
    <p style="color:var(--muted);font-size:0.875rem;">{term['meta_desc']}</p>
    <div class="cta-box" style="margin:1.5rem 0;">
      <p>Validate your robots.txt live — detect all issues and get the corrected file.</p>
      <a href="/robots/" class="cta-btn">Open robots.txt Validator →</a>
    </div>
    <h2>Related Fix Guides</h2>
    <ul style="font-size:0.85rem;padding-left:1.5rem;color:var(--muted);">
      <li><a href="/fix/robots/accidental-disallow-all/">Fix: accidentally blocking all crawlers</a></li>
      <li><a href="/fix/robots/blocking-ai-bots/">Fix: missing AI bot directives</a></li>
      <li><a href="/fix/robots/missing-sitemap-reference/">Fix: missing sitemap reference</a></li>
      <li><a href="/fix/robots/crawl-delay-too-high/">Fix: crawl-delay too high</a></li>
      <li><a href="/fix/robots/noindex-vs-disallow/">Noindex vs Disallow — what's the difference?</a></li>
    </ul>
  </div>
{FOOTER}
</body>
</html>"""

def build_fix_robots_index():
    all_pages = (
        [(p["slug"], p["title"]) for p in FIX_PAGES] +
        [(c["cms"], c["title"]) for c in CMS_PAGES] +
        [(a[0], a[2]) for a in AI_BOT_PAGES] +
        [(c["slug"], c["title"]) for c in CONCEPT_PAGES]
    )
    cards = "\n".join([
        f'    <a href="/fix/robots/{slug}/" style="display:block;background:var(--bg2);border:1px solid #2a2d3d;border-radius:8px;padding:1rem 1.25rem;font-size:0.82rem;color:var(--text);margin-bottom:0.5rem;">{title}</a>'
        for slug, title in all_pages
    ])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>robots.txt Fix Guides — ConfigClarity</title>
  <meta name="description" content="robots.txt fix guides for accidental crawl blocks, AI bot directives, CMS configurations, crawl-delay, sitemap references, and wildcard patterns.">
  <link rel="canonical" href="https://configclarity.dev/fix/robots/">
  {FONT}
{CSS}
</head>
<body>
{HEADER}
  <div style="max-width:760px;margin:0 auto;padding:2rem;">
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:1.5rem;"><a href="/" style="color:var(--muted);">ConfigClarity</a> › <a href="/fix/" style="color:var(--muted);">Fix Guides</a> › robots.txt</div>
    <h1 style="font-size:1.6rem;font-weight:700;margin-bottom:1rem;">robots.txt Fix Guides</h1>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:2rem;">Exact copy-paste fixes for robots.txt issues — blocking AI bots, CMS configurations, crawl-delay, wildcard patterns, and more.</p>
{cards}
  </div>
{FOOTER}
</body>
</html>"""

def build_cms_page(cms):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cms['title']} — ConfigClarity</title>
  <meta name="description" content="{cms['meta_desc']}">
  <meta name="keywords" content="{cms['keywords']}">
  <link rel="canonical" href="https://configclarity.dev/fix/robots/{cms['cms']}/">
  {FONT}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"TechArticle",
    "headline":"{cms['title']}","url":"https://configclarity.dev/fix/robots/{cms['cms']}/",
    "description":"{cms['meta_desc']}","author":{{"@type":"Organization","name":"MetricLogic"}}
  }}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join([
      f'{{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}'
      for q, a in cms["faqs"]
  ])}]}}
  </script>
{CSS}
</head>
<body>
{HEADER}
  <div class="breadcrumb"><a href="/">ConfigClarity</a> › <a href="/fix/">Fix Guides</a> › <a href="/fix/robots/">robots.txt</a> › {cms['title']}</div>
  <div class="content">
    <h1>{cms['title']}</h1>
    {cms['content']}
    <div class="cta-box">
      <p>Validate your robots.txt live — fetch any URL and get AI bot coverage + URL tester.</p>
      <a href="/robots/" class="cta-btn">Open robots.txt Validator →</a>
    </div>
    <h2>Frequently Asked Questions</h2>
    {"".join([f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q, a in cms["faqs"]])}
  </div>
{FOOTER}
</body>
</html>"""

if __name__ == '__main__':
    print("=== Building robots.txt SEO Pages ===\n")
    count = 0

    # Index
    os.makedirs("fix/robots", exist_ok=True)
    with open("fix/robots/index.html", "w") as f:
        f.write(build_fix_robots_index())
    print("  ✅ fix/robots/index.html")
    count += 1

    # 9 fix pages
    for page in FIX_PAGES:
        path = f"fix/robots/{page['slug']}/index.html"
        os.makedirs(f"fix/robots/{page['slug']}", exist_ok=True)
        html = make_fix_page(
            page["slug"], page["title"], page["meta_desc"], page["keywords"],
            page["intro"], page["problem"], page["fix_label"], page["fix_code"],
            page["fix_explanation"], page["faqs"], page["related_links"]
        )
        with open(path, "w") as f:
            f.write(html)
        print(f"  ✅ {path}")
        count += 1

    # 6 CMS pages
    for cms in CMS_PAGES:
        path = f"fix/robots/{cms['cms']}/index.html"
        os.makedirs(f"fix/robots/{cms['cms']}", exist_ok=True)
        with open(path, "w") as f:
            f.write(build_cms_page(cms))
        print(f"  ✅ {path}")
        count += 1

    # 6 AI bot pages
    for slug, bot_name, title, meta_desc, fix_code in AI_BOT_PAGES:
        path = f"fix/robots/{slug}/index.html"
        os.makedirs(f"fix/robots/{slug}", exist_ok=True)
        with open(path, "w") as f:
            f.write(build_ai_bot_page(slug, bot_name, title, meta_desc, fix_code))
        print(f"  ✅ {path}")
        count += 1

    # 4 concept pages
    for term in CONCEPT_PAGES:
        path = f"fix/robots/{term['slug']}/index.html"
        os.makedirs(f"fix/robots/{term['slug']}", exist_ok=True)
        with open(path, "w") as f:
            f.write(build_concept_page(term))
        print(f"  ✅ {path}")
        count += 1

    print(f"\nDone. {count} robots.txt pages built.")
    print("\nPaths created:")
    print("  fix/robots/index.html")
    print("  fix/robots/{9 fix pages}/index.html")
    print("  fix/robots/{6 cms pages}/index.html")
    print("  fix/robots/{6 ai bot pages}/index.html")
    print("  fix/robots/{4 concept pages}/index.html")
