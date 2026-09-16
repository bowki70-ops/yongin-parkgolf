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

    # 3. rss.xml
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>용인 파크골프 정보 포털</title>
  <link>https://yonginparkgolf.co.kr</link>
  <description>용인 파크골프 정보 포털 - 수지·포곡·기흥 주요 구장 실시간 운영현황, 날씨, 자격증 가이드</description>
  <language>ko</language>
  <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
  <item>
    <title>용인 파크골프 정보 포털 메인</title>
    <link>https://yonginparkgolf.co.kr/</link>
    <description>용인 관내 주요 파크골프장 운영정보, 라운딩 조인, 레슨 정보</description>
    <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
    <guid>https://yonginparkgolf.co.kr/</guid>
  </item>
</channel>
</rss>
"""

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_content.strip() + "\n")
    print(f"[SUCCESS] Created rss.xml ({os.path.getsize('rss.xml')} bytes)")

if __name__ == "__main__":
    generate_seo_files()

