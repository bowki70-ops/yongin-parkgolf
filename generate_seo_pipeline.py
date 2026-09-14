import sys
import os
import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def generate_seo_files():
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    print(f"Generating SEO pipeline files for date: {today_str}")

    # 1. robots.txt
    robots_content = f"""User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Yeti
Allow: /

User-agent: Naverbot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

Sitemap: https://yonginparkgolf.co.kr/sitemap.xml
"""

    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content.strip() + "\n")
    print(f"[SUCCESS] Created robots.txt ({os.path.getsize('robots.txt')} bytes)")

    # 2. sitemap.xml
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yonginparkgolf.co.kr/</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content.strip() + "\n")
    print(f"[SUCCESS] Created sitemap.xml ({os.path.getsize('sitemap.xml')} bytes)")

if __name__ == "__main__":
    generate_seo_files()
