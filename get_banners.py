import urllib.request
import re
import json

url = 'https://halahandicraft.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html_doc = resp.read().decode('utf-8')
    
    # Find all Shopify CDN images
    img_urls = re.findall(r'//halahandicraft\.com/cdn/shop/files/[^\"\'\s\?]+', html_doc)
    clean_imgs = list(dict.fromkeys(['https:' + img for img in img_urls if any(ext in img.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp'])]))
    
    print(f"Found {len(clean_imgs)} banner/asset images on halahandicraft.com homepage:")
    for i, img in enumerate(clean_imgs):
        print(f"[{i+1}] {img}")

    # Also check collections and products
    collections_url = 'https://halahandicraft.com/collections.json'
    try:
        req2 = urllib.request.Request(collections_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req2) as resp2:
            cols = json.loads(resp2.read().decode('utf-8')).get('collections', [])
            print("\nCollections found:")
            for c in cols:
                print(f"- {c.get('title')}: Image: {c.get('image', {}).get('src') if c.get('image') else 'None'}")
    except Exception as e:
        print("Collections error:", e)

except Exception as e:
    print('Error:', e)
