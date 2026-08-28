import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'products.json')

with open(json_path, 'r', encoding='utf-8') as f:
    prods = json.load(f)

print(f"Total products in products.json: {len(prods)}")

# Check products with halahandicraft.com images
hala_prods = [p for p in prods if 'halahandicraft.com' in p.get('image', '') or 'shopify' in p.get('image', '')]
print(f"Products with real halahandicraft CDN images: {len(hala_prods)}")

print("\nSample top real products:")
for p in hala_prods[:15]:
    name = p['name'].encode('ascii', 'ignore').decode('ascii')
    print(f"ID: {p['id']} | {name} | Rs. {p['price']} | {p['category']}")

