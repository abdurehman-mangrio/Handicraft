import urllib.request
import json
import re
import html

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean_text = re.sub(r'<[^>]+>', ' ', raw_html)
    clean_text = html.unescape(clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def fetch_all_products():
    all_products = []
    page = 1
    
    while True:
        url = f"https://halahandicraft.com/products.json?limit=250&page={page}"
        print(f"Fetching page {page}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                products = data.get('products', [])
                if not products:
                    break
                all_products.extend(products)
                print(f"Fetched {len(products)} products on page {page}.")
                page += 1
                if len(products) < 250:
                    break
        except Exception as e:
            print(f"Error: {e}")
            break
            
    return all_products

def categorize_product(title, p_type, tags):
    text = (title + " " + p_type + " " + " ".join(tags)).lower()
    
    if any(k in text for k in ['pottery', 'kashi', 'vase', 'ceramic', 'plate', 'bowl', 'mug', 'cup', 'tile', 'pot']):
        return 'kashi', 'Kashi Pottery'
    elif any(k in text for k in ['ajrak', 'ajrakh', 'block print', 'shawl', 'chaddar', 'chadar']):
        return 'ajrak', 'Sindhi Ajrak & Shawls'
    elif any(k in text for k in ['sussi', 'soosi', 'chunri', 'chunri dress', '3pc', '2pc', 'kurti', 'dress', 'frock', 'suit', 'lawn', 'cotton', 'koti']):
        return 'clothing', 'Handmade Dresses & Sussi'
    elif any(k in text for k in ['bedsheet', 'bed sheet', 'bed cover', 'quilt', 'ralli', 'rilli', 'cushion', 'pillow']):
        return 'ralli', 'Bedsheets & Ralli'
    elif any(k in text for k in ['furniture', 'jhoola', 'swing', 'peeri', 'chair', 'table', 'jandi', 'wood', 'bed']):
        return 'furniture', 'Jandi Woodwork & Furniture'
    elif any(k in text for k in ['topi', 'cap', 'hat']):
        return 'topi', 'Sindhi Topi'
    elif any(k in text for k in ['bag', 'handbag', 'tote', 'clutch']):
        return 'accessories', 'Handmade Bags & Accessories'
    else:
        return 'clothing', 'Hala Traditional Craft'

def main():
    raw_products = fetch_all_products()
    print(f"Total raw products fetched: {len(raw_products)}")
    
    transformed_products = []
    
    # Process scraped products first to get real images
    current_id = 1
    
    # Add carefully selected flagship products with real CDN images
    flagship_items = [
        {
            "id": current_id,
            "name": "Authentic Sindhi Ajrak Block Print Shawl",
            "category": "ajrak",
            "categoryLabel": "Sindhi Ajrak & Shawls",
            "badge": "Best Seller",
            "price": 2800,
            "image": "https://cdn.shopify.com/s/files/1/0971/6160/9397/collections/C0F0C4A8-1A3A-4B9E-809B-E609203874B0.jpg",
            "description": "100% Hand-blocked Sindhi Ajrak crafted in Hala with natural vegetable dyes and organic indigo. Woven on premium soft cotton with the traditional 20-step block printing process.",
            "sizes": ["Standard (2.5m x 1.2m)"],
            "colors": ["Traditional Crimson & Indigo"]
        },
        {
            "id": current_id + 1,
            "name": "Royal Kashi Blue Pottery Glazed Vase",
            "category": "kashi",
            "categoryLabel": "Kashi Pottery",
            "badge": "Masterpiece",
            "price": 3500,
            "image": "https://halahandicraft.com/cdn/shop/collections/pexels-kamo11235-667838.jpg",
            "description": "Exquisite hand-thrown terracotta vase hand-painted in iconic Hala cobalt and turquoise floral motifs (Kashi Kari). Kiln-fired to high gloss glazed perfection.",
            "sizes": ["10 Inches", "14 Inches", "18 Inches"],
            "colors": ["Cobalt Blue & Turquoise", "Mustard Gold & White"]
        },
        {
            "id": current_id + 2,
            "name": "Traditional Hand-Embroidered 3-Piece Suit",
            "category": "clothing",
            "categoryLabel": "Handmade Dresses & Sussi",
            "badge": "New Arrival",
            "price": 4500,
            "image": "https://halahandicraft.com/cdn/shop/collections/9D49E813-8BBB-4542-B2D0-3AE7083A4BBA.png",
            "description": "Exquisite 3-piece traditional Sindhi hand-embroidered suit with fine thread work, matching dupatta, and comfortable unstitched fabric.",
            "sizes": ["Unstitched 3-Piece"],
            "colors": ["Mustard Yellow", "Crimson Maroon", "Emerald Green"]
        },
        {
            "id": current_id + 3,
            "name": "Authentic Sindhi Patchwork Ralli Bedsheet Set",
            "category": "ralli",
            "categoryLabel": "Bedsheets & Ralli",
            "badge": "Heritage",
            "price": 6500,
            "image": "https://halahandicraft.com/cdn/shop/collections/0152B282-4AAB-48C2-A4C4-1A330DA53FF6.jpg",
            "description": "Traditional Sindhi Ralli quilt and bedsheet set featuring complex geometric appliqué and patchwork hand-stitched with love by artisans in Hala, Sindh.",
            "sizes": ["King Size (90x108 in) + 2 Pillow Covers"],
            "colors": ["Vibrant Sindhi Multi-Patchwork"]
        },
        {
            "id": current_id + 4,
            "name": "Hand-Carved Jandi Wooden Swing (Jhoola)",
            "category": "furniture",
            "categoryLabel": "Jandi Woodwork & Furniture",
            "badge": "Royal Luxury",
            "price": 48000,
            "image": "https://cdn.shopify.com/s/files/1/0971/6160/9397/collections/D22754EE-8169-4670-A657-050F8C9F0B3C.jpg",
            "description": "Regal handcrafted Hala swing made of solid Sheesham wood with vibrant lacquer turned woodwork (Jandi). Includes heavy brass chains and ornate floral engraving.",
            "sizes": ["Full Size (Seats 3 Persons)"],
            "colors": ["Royal Walnut & Multicolored Lacquer"]
        },
        {
            "id": current_id + 5,
            "name": "Handcrafted Mirror-Work Sindhi Topi",
            "category": "topi",
            "categoryLabel": "Sindhi Topi",
            "badge": "Authentic",
            "price": 1400,
            "image": "https://cdn.shopify.com/s/files/1/0971/6160/9397/collections/6991E83B-CFAC-4A4E-9A55-08485491C3B2.jpg",
            "description": "Master-crafted traditional Sindhi Topi featuring dense silk thread embroidery, geometric patterns, and sparkling glass mirror work (Shisha Kari).",
            "sizes": ["Medium (21.5 in)", "Large (22.5 in)", "XL (23.5 in)"],
            "colors": ["Crimson Maroon & Gold", "Emerald Green & Silver", "Jet Black & Gold"]
        },
        {
            "id": current_id + 6,
            "name": "Handmade Artisan Embroidery Clutch / Handbag",
            "category": "accessories",
            "categoryLabel": "Handbags & Accessories",
            "badge": "Trendy",
            "price": 1800,
            "image": "https://halahandicraft.com/cdn/shop/collections/02BB6DD3-C45B-49A0-865B-B35448970227.png",
            "description": "Traditional Sindhi mirror work and thread embroidery clutch bag with metallic chain strap. Perfect for weddings, events, and casual cultural styling.",
            "sizes": ["Standard (10x6 in)"],
            "colors": ["Black & Multi-thread", "Maroon & Gold"]
        },
        {
            "id": current_id + 7,
            "name": "Traditional Chunri Lawn Kurti Collection",
            "category": "clothing",
            "categoryLabel": "Handmade Dresses & Sussi",
            "badge": "Popular",
            "price": 2600,
            "image": "https://halahandicraft.com/cdn/shop/collections/pexels-dhanno-19589912.jpg",
            "description": "Pure cotton Chunri tie-dye pattern stitched kurti with delicate neckline lace and wooden buttons. Extremely soft, lightweight, and vibrant.",
            "sizes": ["Small", "Medium", "Large", "XL"],
            "colors": ["Mustard & Red", "Royal Blue & White", "Teal & Orange"]
        }
    ]
    
    for item in flagship_items:
        if "images" not in item:
            item["images"] = [item["image"]]

    transformed_products.extend(flagship_items)
    current_id += len(flagship_items)
    
    # Process scraped products
    for p in raw_products:
        images = p.get('images', [])
        if not images:
            continue
        
        main_img = images[0].get('src', '')
        if not main_img:
            continue
        
        # Ensure high resolution and extract up to 4 images
        main_img = main_img.split('?')[0]
        product_images = []
        for img in images[:4]:
            img_src = img.get('src', '')
            if img_src:
                product_images.append(img_src.split('?')[0])
        
        title = p.get('title', '').strip()
        if not title:
            continue
            
        variants = p.get('variants', [])
        if variants:
            try:
                price = int(float(variants[0].get('price', 0)))
            except:
                price = 2500
        else:
            price = 2500
            
        if price <= 0:
            price = 2500
            
        body_html = p.get('body_html', '')
        desc = clean_html(body_html)
        if not desc or len(desc) < 10:
            desc = f"Authentic handcrafted {title} made with traditional Sindhi artisan techniques directly in Hala, Sindh. High quality, authentic and durable."
            
        p_type = p.get('product_type', '')
        tags = p.get('tags', [])
        cat_key, cat_label = categorize_product(title, p_type, tags)
        
        sizes = []
        colors = []
        for opt in p.get('options', []):
            opt_name = opt.get('name', '').lower()
            values = opt.get('values', [])
            if 'size' in opt_name:
                sizes = [v for v in values if v.lower() != 'default title']
            elif 'color' in opt_name or 'colour' in opt_name:
                colors = [v for v in values if v.lower() != 'default title']
                
        badge = None
        if price > 5000:
            badge = "Premium"
        elif "ajrak" in title.lower():
            badge = "Best Seller"
        elif "dress" in title.lower() or "suit" in title.lower():
            badge = "New Arrival"
            
        transformed_products.append({
            "id": current_id,
            "name": title,
            "category": cat_key,
            "categoryLabel": cat_label,
            "badge": badge,
            "price": price,
            "image": main_img,
            "images": product_images,
            "description": desc,
            "sizes": sizes if sizes else ["Standard"],
            "colors": colors if colors else []
        })
        current_id += 1
        
    print(f"Total compiled products: {len(transformed_products)}")
    
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "products.json")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(transformed_products, f, indent=4, ensure_ascii=False)
        
    print("products.json successfully written!")

if __name__ == "__main__":
    main()
