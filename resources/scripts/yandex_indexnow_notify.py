#!/usr/bin/env python3
"""
==============================================================================
Yandex & Bing IndexNow Instant Indexing Notification Script
Reads sitemap.xml and submits all canonical URLs of widewayfootwear.com
to Yandex (https://yandex.com/indexnow) and IndexNow API (https://api.indexnow.org/indexnow).
==============================================================================
"""
import os
import re
import sys
import json
import urllib.request
import urllib.error

_curr = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_curr) if os.path.basename(_curr) == "scripts" else _curr
SITEMAP_PATH = os.path.join(BASE_DIR, "sitemap.xml")
HOST = "www.widewayfootwear.com"
KEY = "e8a4c9f21b0d4637a9e52c3f8b7d6e21"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

ENDPOINTS = [
    "https://yandex.com/indexnow",
    "https://api.indexnow.org/indexnow"
]

DEFAULT_URLS = [
    f"https://{HOST}/",
    f"https://{HOST}/ru/",
    f"https://{HOST}/ru/cis-central-asia/",
    f"https://{HOST}/products",
    f"https://{HOST}/sport-outdoor-shoes-wholesale",
    f"https://{HOST}/casual-shoes-oem-manufacturer",
    f"https://{HOST}/mens-sneakers-bulk-supplier",
    f"https://{HOST}/womens-sneakers-oem-factory",
    f"https://{HOST}/slides-sandals-slippers-manufacturer",
    f"https://{HOST}/oem-odm",
    f"https://{HOST}/production-capacity",
    f"https://{HOST}/quality-control",
    f"https://{HOST}/certifications",
    f"https://{HOST}/sustainability",
    f"https://{HOST}/case-studies",
    f"https://{HOST}/heritage-footwear-reproduction",
    f"https://{HOST}/brand-identity",
    f"https://{HOST}/about",
    f"https://{HOST}/videos",
    f"https://{HOST}/news",
    f"https://{HOST}/contact",
    f"https://{HOST}/sitemap.xml",
    f"https://{HOST}/llms.txt",
    f"https://{HOST}/llms-full.txt"
]

def load_urls_from_sitemap():
    if not os.path.exists(SITEMAP_PATH):
        print(f"[INFO] sitemap.xml not found at {SITEMAP_PATH}, using default URL list.")
        return DEFAULT_URLS
    try:
        with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        url_blocks = re.findall(r"<url>(.*?)</url>", content, flags=re.S)
        urls = []
        for block in url_blocks:
            m = re.search(r"<loc>(https://(?:www\.)?widewayfootwear\.com[^<]+)</loc>", block)
            if m:
                clean_u = m.group(1).strip()
                # Normalize to canonical www domain
                if "https://widewayfootwear.com" in clean_u and "www." not in clean_u:
                    clean_u = clean_u.replace("https://widewayfootwear.com", "https://www.widewayfootwear.com")
                urls.append(clean_u)
        if not urls:
            return DEFAULT_URLS
        # Ensure Russian portals are always present
        urls.append(f"https://{HOST}/ru/")
        urls.append(f"https://{HOST}/ru/cis-central-asia/")
        return list(dict.fromkeys(urls))
    except Exception as e:
        print(f"[WARN] Error reading sitemap.xml: {e}, using default list.")
        return DEFAULT_URLS

def submit_indexnow(urls):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "WidewayFootwear-IndexNow-Client/1.2"
    }

    for endpoint in ENDPOINTS:
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"[SUCCESS] {endpoint} -> HTTP {resp.status} ({len(urls)} URLs submitted)")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            print(f"[WARN] {endpoint} -> HTTP {e.code}: {body[:200]}")
        except Exception as e:
            print(f"[ERROR] {endpoint} -> {e}")

if __name__ == "__main__":
    custom_urls = sys.argv[1:] if len(sys.argv) > 1 else None
    urls = custom_urls or load_urls_from_sitemap()
    print(f"Submitting {len(urls)} canonical URLs for widewayfootwear.com to Yandex & Bing IndexNow...")
    submit_indexnow(urls)
