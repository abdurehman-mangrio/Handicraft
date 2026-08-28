import urllib.request
import re

url = 'https://halahandicraft.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html_doc = resp.read().decode('utf-8')

# Find image-banner or slideshow sections
banners = re.findall(r'<div[^>]*class="[^"]*(?:banner|slideshow|image-with-text|hero)[^"]*"[^>]*>([\s\S]*?)</div>', html_doc, re.I)
print(f"Found {len(banners)} banner divs")

# Find all full image URLs and their context
img_matches = re.findall(r'<img[^>]+src="([^">]+)"[^>]*alt="([^"]*)"', html_doc)
print(f"\nFound {len(img_matches)} img tags:")
for src, alt in img_matches:
    if 'cdn/shop' in src:
        clean_src = 'https:' + src if src.startswith('//') else src
        clean_src = clean_src.split('&')[0]
        print(f"Alt: {alt} -> {clean_src}")

# Also find srcset images
srcset_matches = re.findall(r'srcset="([^">]+)"', html_doc)
print(f"\nFound {len(srcset_matches)} srcset attributes:")
for s in srcset_matches[:10]:
    urls = [u.strip().split(' ')[0] for u in s.split(',') if 'cdn/shop' in u]
    if urls:
        last_highres = urls[-1]
        clean_highres = 'https:' + last_highres if last_highres.startswith('//') else last_highres
        print("HighRes:", clean_highres)
