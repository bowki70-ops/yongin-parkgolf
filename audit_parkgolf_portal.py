import os
import sys
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Ensure utf-8 output for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def run_audit(html_path="index.html"):
    print("=" * 70)
    print(f"   PARKGOLF PORTAL AUDIT: {html_path}")
    print("=" * 70)

    if not os.path.exists(html_path):
        print(f"ERROR: {html_path} not found.")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    base_dir = os.path.dirname(os.path.abspath(html_path))

    # --- 1. Meta & SEO & OG Check ---
    print("\n[1] Technical SEO & Open Graph (OG) Check")
    print("-" * 50)
    
    title_tag = soup.find("title")
    title_text = title_tag.get_text().strip() if title_tag else None
    print(f"[TITLE] {title_text if title_text else 'MISSING [X]'}")

    viewport = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
    if viewport:
        print(f"[VIEWPORT] {viewport.get('content')}")
    else:
        print("[VIEWPORT] MISSING [X]")

    description = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    print(f"[DESCRIPTION] {description.get('content') if description else 'MISSING [X]'}")

    canonical = soup.find("link", attrs={"rel": "canonical"})
    print(f"[CANONICAL] {canonical.get('href') if canonical else 'MISSING [!]'}")

    # Favicons
    icons = soup.find_all("link", attrs={"rel": re.compile(r"icon", re.I)})
    print(f"\n[FAVICON] {len(icons)} icon tags found:")
    if not icons:
        print("  [X] No favicon link tags found!")
    for ic in icons:
        href = ic.get("href")
        rel = ic.get("rel")
        exists = os.path.exists(os.path.join(base_dir, href)) if href and not href.startswith("http") else True
        status = "OK [V]" if exists else "FILE NOT FOUND [X]"
        print(f"  - rel='{rel}', href='{href}' -> {status}")

    # OG Tags
    og_properties = ["og:title", "og:description", "og:image", "og:url", "og:type", "og:site_name", "og:locale"]
    print("\n[OPEN GRAPH] Tags Status:")
    og_found = {}
    for prop in og_properties:
        tag = soup.find("meta", attrs={"property": prop})
        if tag:
            val = tag.get("content", "")
            og_found[prop] = val
            print(f"  - {prop}: {val}")
        else:
            print(f"  - {prop}: MISSING [X]")

    # OG Image check
    if "og:image" in og_found:
        img_url = og_found["og:image"]
        if not img_url.startswith("http"):
            img_path = os.path.join(base_dir, img_url.lstrip("/"))
            if not os.path.exists(img_path):
                print(f"  [!] og:image local file check: File does not exist ({img_url})")
            else:
                print(f"  [V] og:image local file check: Exists ({img_url})")

    # --- 2. Link & Resource Integrity ---
    print("\n[2] Link & Resource Integrity Check")
    print("-" * 50)

    # Collect element IDs for anchor validation
    all_ids = set(tag.get("id") for tag in soup.find_all(True) if tag.get("id"))

    # Check <a> href
    anchors = soup.find_all("a")
    print(f"[ANCHORS] Total <a> links: {len(anchors)}")
    broken_anchors = []
    dummy_anchors = []
    
    for a in anchors:
        href = a.get("href")
        text = a.get_text(strip=True)[:30]
        if not href or href == "#" or href == "javascript:void(0)" or href == "javascript:;":
            dummy_anchors.append((text, href))
        elif href.startswith("#"):
            target_id = href[1:]
            if target_id and target_id not in all_ids:
                broken_anchors.append((text, href, f"Anchor ID #{target_id} not found in page"))
        elif not href.startswith(("http://", "https://", "mailto:", "tel:", "sms:", "javascript:")):
            # Local file link
            clean_href = href.split("#")[0].split("?")[0]
            if clean_href and not os.path.exists(os.path.join(base_dir, clean_href)):
                broken_anchors.append((text, href, f"Local file missing: {clean_href}"))

    print(f"  - Dummy/Empty Hrefs ('#' or 'javascript:'): {len(dummy_anchors)}")
    for txt, hr in dummy_anchors[:10]:
        print(f"    [!] Text: '{txt}' -> href='{hr}'")
    if len(dummy_anchors) > 10:
        print(f"    ... and {len(dummy_anchors)-10} more")

    print(f"  - Broken Links: {len(broken_anchors)}")
    for txt, hr, reason in broken_anchors:
        print(f"    [X] Text: '{txt}' -> href='{hr}' ({reason})")

    # Check <img> src
    imgs = soup.find_all("img")
    print(f"\n[IMAGES] Total <img> tags: {len(imgs)}")
    broken_imgs = []
    missing_alt = []

    for img in imgs:
        src = img.get("src")
        alt = img.get("alt")
        if alt is None:
            missing_alt.append(src)
        if not src:
            broken_imgs.append(("NO SRC", "Missing src attribute"))
        elif not src.startswith(("http://", "https://", "data:")):
            clean_src = src.split("?")[0]
            if not os.path.exists(os.path.join(base_dir, clean_src)):
                broken_imgs.append((src, f"Local image missing: {clean_src}"))

    print(f"  - Missing/Broken Image Resources: {len(broken_imgs)}")
    for src, reason in broken_imgs:
        print(f"    [X] src='{src}' ({reason})")
    print(f"  - Images without alt attribute: {len(missing_alt)}")
    if missing_alt:
        print(f"    Sample missing alt src (first 5): {missing_alt[:5]}")

    # Check <script> src and <link> href
    scripts = soup.find_all("script", src=True)
    broken_scripts = []
    for sc in scripts:
        src = sc.get("src")
        if not src.startswith(("http://", "https://")):
            clean_src = src.split("?")[0]
            if not os.path.exists(os.path.join(base_dir, clean_src)):
                broken_scripts.append(src)
    print(f"\n[SCRIPTS] Missing script files: {len(broken_scripts)}")
    for sc in broken_scripts:
        print(f"  [X] script src='{sc}' missing")

    stylesheets = soup.find_all("link", rel=lambda r: r and "stylesheet" in (r if isinstance(r, list) else [r]))
    broken_css = []
    for css in stylesheets:
        href = css.get("href")
        if href and not href.startswith(("http://", "https://")):
            clean_href = href.split("?")[0]
            if not os.path.exists(os.path.join(base_dir, clean_href)):
                broken_css.append(href)
    print(f"[STYLESHEETS] Missing stylesheet files: {len(broken_css)}")
    for css in broken_css:
        print(f"  [X] css href='{css}' missing")

    # Check Audio/Media elements
    audio_tags = soup.find_all("audio")
    audio_sources = soup.find_all("source")
    broken_media = []
    for tag in audio_tags + audio_sources:
        src = tag.get("src")
        if src and not src.startswith(("http://", "https://", "data:")):
            clean_src = src.split("?")[0]
            if not os.path.exists(os.path.join(base_dir, clean_src)):
                broken_media.append(src)
    print(f"[MEDIA] Audio tags: {len(audio_tags)}, Missing Media files: {len(broken_media)}")
    for m in broken_media:
        print(f"    [X] media src='{m}' missing")


    # --- 3. 5070 Mobile UI & Font & Accessibility Check ---
    print("\n[3] 5070 Mobile UI & Accessibility Scan")
    print("-" * 50)

    # Check small inline font sizes
    small_fonts = []
    for elem in soup.find_all(True, style=True):
        style = elem.get("style", "")
        match = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)\s*(px|pt|rem|em)", style, re.I)
        if match:
            val, unit = float(match.group(1)), match.group(2).lower()
            if (unit == "px" and val < 13) or (unit == "rem" and val < 0.8) or (unit == "pt" and val < 9):
                small_fonts.append((elem.name, elem.get_text(strip=True)[:30], style))

    print(f"[FONT ACCESSIBILITY] Extremely small inline font sizes (<13px) detected: {len(small_fonts)}")
    for tag, txt, st in small_fonts[:10]:
        print(f"  [!] <{tag}> '{txt}' -> style='{st}'")

    # Touch viewport accessibility
    if viewport:
        vp_content = viewport.get('content', '')
        if "user-scalable=no" in vp_content or "maximum-scale=1.0" in vp_content or "maximum-scale=1" in vp_content:
            print("  [!] Viewport restricts zooming ('user-scalable=no' or 'maximum-scale=1.0'). Recommended to allow pinch zoom for 5070 senior users!")
        else:
            print("  [V] Viewport allows user zooming for accessibility.")

    # --- 4. Park Golf Official Terms & Typo Scan ---
    print("\n[4] Park Golf Terminology & Typo Scan")
    print("-" * 50)

    text_nodes = soup.get_text()

    # Rule check: Club length standard is 86cm max.
    club_matches = re.findall(r"\d+\s*cm|\d+\s*m", text_nodes, re.I)
    print(f"[RULES] Length mentions found: {set(club_matches)}")

    # Penalty strokes
    penalty_matches = re.findall(r"\d+\s*벌타|벌타\s*\d+", text_nodes)
    print(f"[RULES] Penalty stroke mentions found: {set(penalty_matches)}")

    # Check specific potential typos or terminology errors
    typo_patterns = [
        (r"85cm", "86cm가 공식 파크골프채 최대 길이 기준입니다."),
        (r"87cm", "86cm가 공식 파크골프채 최대 길이 기준입니다."),
        (r"1벌타", "파크골프 표준 벌타는 기본 2벌타입니다. (1벌타 표기 맥락 확인 필요)"),
        (r"3벌타", "파크골프 표준 벌타 확인 필요"),
        (r"파크\s*골프", "파크골프 (공식 명칭 붙여쓰기)"),
        (r"원해\b", "오탈자 의심"),
        (r"86cm", "공식 클럽 길이 규정"),
    ]

    print("\n[TERMINOLOGY & TYPOS] Pattern Matching:")
    for pat, desc in typo_patterns:
        matches = re.findall(pat, content)
        if matches:
            print(f"  - Pattern '{pat}' ({desc}): {len(matches)} occurrences")
            count = 0
            for tag in soup.find_all(string=re.compile(pat)):
                parent = tag.parent.name if tag.parent else 'text'
                snippet = tag.strip()[:60]
                if snippet:
                    print(f"     * [{parent}] {snippet}")
                    count += 1
                    if count >= 3:
                        break
        else:
            print(f"  - Pattern '{pat}' ({desc}): 0 found")

    print("\n" + "=" * 70)
    print("   END OF AUDIT")
    print("=" * 70)

if __name__ == "__main__":
    run_audit("index.html")
