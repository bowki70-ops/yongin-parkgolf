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
    subpages = [
        {"loc": "https://yonginparkgolf.co.kr/", "priority": "1.0"},
        {"loc": "https://yonginparkgolf.co.kr/pogok", "priority": "0.9"},
        {"loc": "https://yonginparkgolf.co.kr/suji", "priority": "0.9"},
        {"loc": "https://yonginparkgolf.co.kr/giheung", "priority": "0.9"},
        {"loc": "https://yonginparkgolf.co.kr/license", "priority": "0.9"},
    ]

    sitemap_items = ""
    for page in subpages:
        sitemap_items += f"""  <url>
    <loc>{page['loc']}</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{page['priority']}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}</urlset>
"""

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content.strip() + "\n")
    print(f"[SUCCESS] Created sitemap.xml ({os.path.getsize('sitemap.xml')} bytes)")

    # 3. rss.xml
    rss_items = f"""  <item>
    <title>용인 파크골프 정보 포털 메인</title>
    <link>https://yonginparkgolf.co.kr/</link>
    <description>용인 관내 주요 파크골프장 운영정보, 회원 직거래 장터, 라운딩 조인, 레슨 정보</description>
    <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
    <guid>https://yonginparkgolf.co.kr/</guid>
  </item>
  <item>
    <title>포곡 파크골프장 이용 가이드 | 실시간 현황 및 위치</title>
    <link>https://yonginparkgolf.co.kr/pogok</link>
    <description>용인 포곡 파크골프장 18홀 위치, 월요일 휴장일, 실시간 대기시간 안내</description>
    <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
    <guid>https://yonginparkgolf.co.kr/pogok</guid>
  </item>
  <item>
    <title>수지 아르피아 파크골프장 이용 가이드</title>
    <link>https://yonginparkgolf.co.kr/suji</link>
    <description>수지 아르피아 파크골프장 9홀 코스 위치 및 이용시간 안내</description>
    <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
    <guid>https://yonginparkgolf.co.kr/suji</guid>
  </item>
  <item>
    <title>기흥 호수공원 파크골프장 가이드</title>
    <link>https://yonginparkgolf.co.kr/giheung</link>
    <description>기흥 호수공원 파크골프장 운영안내 및 이용 가이드</description>
    <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
    <guid>https://yonginparkgolf.co.kr/giheung</guid>
  </item>
  <item>
    <title>파크골프 자격증 가이드 | 생활스포츠지도사 2급 취득 방법</title>
    <link>https://yonginparkgolf.co.kr/license</link>
    <description>국가공인 생활스포츠지도사 2급 및 파크골프 지도자/심판 자격증 완벽 가이드</description>
    <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
    <guid>https://yonginparkgolf.co.kr/license</guid>
  </item>
"""

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>용인 파크골프 정보 포털</title>
  <link>https://yonginparkgolf.co.kr</link>
  <description>용인 파크골프 정보 포털 - 수지·포곡·기흥 주요 구장 실시간 운영현황, 날씨, 자격증 가이드</description>
  <language>ko</language>
  <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate>
{rss_items}</channel>
</rss>
"""

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_content.strip() + "\n")
    print(f"[SUCCESS] Created rss.xml ({os.path.getsize('rss.xml')} bytes)")

if __name__ == "__main__":
    generate_seo_files()
