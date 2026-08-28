import os
import json
import urllib.request
import urllib.error
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("Warning: Pillow not installed. Images will be saved in their original formats without WebP compression.")

# Thread-safe console printing
print_lock = threading.Lock()
def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def download_file(url, filepath):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                with open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            return True
        except Exception as e:
            safe_print(f"Error downloading {url} (Attempt {attempt+1}): {e}")
            time.sleep(1)
    return False

def convert_to_webp(src_path, dest_path):
    if not HAS_PILLOW:
        return False
    try:
        with Image.open(src_path) as im:
            im.save(dest_path, "WEBP", quality=82)
        return True
    except Exception as e:
        safe_print(f"Error converting {src_path} to WebP: {e}")
        return False

def process_download_task(task):
    p_id, image_type, url, temp_path, final_webp_path, final_orig_path, webp_rel, orig_rel = task
    
    # 1. Download to temp path
    safe_print(f"[{p_id}] Downloading {image_type} image from {url}...")
    if download_file(url, temp_path):
        # 2. Convert to WebP if Pillow is available
        if HAS_PILLOW and convert_to_webp(temp_path, final_webp_path):
            try:
                os.remove(temp_path)
            except:
                pass
            return p_id, image_type, webp_rel
        else:
            # Save original file
            if os.path.exists(final_webp_path):
                try:
                    os.remove(final_webp_path)
                except:
                    pass
            try:
                if os.path.exists(final_orig_path):
                    os.remove(final_orig_path)
                os.rename(temp_path, final_orig_path)
            except Exception as e:
                safe_print(f"[{p_id}] Rename error: {e}")
            return p_id, image_type, orig_rel
            
    return p_id, image_type, None

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'products.json')
    assets_dir = os.path.join(current_dir, 'assets', 'products')
    
    os.makedirs(assets_dir, exist_ok=True)
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
        
    print(f"Loaded {len(products)} products from products.json.")
    print("Scanning for existing files & queuing downloads...")
    
    tasks = []
    
    # Track results dynamically
    # Primary image mapping: product_id -> local_path
    primary_results = {}
    # Secondary images mapping: product_id -> list of local_paths (ordered by index)
    secondary_results = {p['id']: [None] * len(p.get('images', [])) for p in products}
    
    # Pre-populate and find what needs downloading
    for p in products:
        p_id = p.get('id')
        primary_url = p.get('image')
        secondary_urls = p.get('images', [])
        
        # 1. Check primary image
        if primary_url:
            if not primary_url.startswith('http'):
                primary_results[p_id] = primary_url
            else:
                ext = os.path.splitext(primary_url.split('?')[0])[1] or '.jpg'
                if ext.lower() not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                    ext = '.jpg'
                
                webp_name = f"{p_id}_primary.webp"
                webp_path = os.path.join(assets_dir, webp_name)
                orig_name = f"{p_id}_primary{ext}"
                orig_path = os.path.join(assets_dir, orig_name)
                
                # Check if WebP or original already exists
                if HAS_PILLOW and os.path.exists(webp_path):
                    primary_results[p_id] = f"assets/products/{webp_name}"
                elif os.path.exists(orig_path):
                    primary_results[p_id] = f"assets/products/{orig_name}"
                else:
                    # Queue download
                    temp_name = f"{p_id}_temp{ext}"
                    temp_path = os.path.join(assets_dir, temp_name)
                    tasks.append((
                        p_id, 
                        'primary', 
                        primary_url, 
                        temp_path, 
                        webp_path, 
                        orig_path, 
                        f"assets/products/{webp_name}", 
                        f"assets/products/{orig_name}"
                    ))
                    
        # 2. Check secondary images
        for idx, url in enumerate(secondary_urls):
            if not url.startswith('http'):
                secondary_results[p_id][idx] = url
            else:
                ext = os.path.splitext(url.split('?')[0])[1] or '.jpg'
                if ext.lower() not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                    ext = '.jpg'
                    
                webp_name = f"{p_id}_{idx}.webp"
                webp_path = os.path.join(assets_dir, webp_name)
                orig_name = f"{p_id}_{idx}{ext}"
                orig_path = os.path.join(assets_dir, orig_name)
                
                if HAS_PILLOW and os.path.exists(webp_path):
                    secondary_results[p_id][idx] = f"assets/products/{webp_name}"
                elif os.path.exists(orig_path):
                    secondary_results[p_id][idx] = f"assets/products/{orig_name}"
                else:
                    # Queue download
                    temp_name = f"{p_id}_{idx}_temp{ext}"
                    temp_path = os.path.join(assets_dir, temp_name)
                    tasks.append((
                        p_id, 
                        ('secondary', idx), 
                        url, 
                        temp_path, 
                        webp_path, 
                        orig_path, 
                        f"assets/products/{webp_name}", 
                        f"assets/products/{orig_name}"
                    ))
                    
    print(f"Already cached: {sum(1 for x in primary_results.values() if x) + sum(sum(1 for y in list_val if y) for list_val in secondary_results.values())} images.")
    print(f"Queued for download: {len(tasks)} images.")
    
    if not tasks:
        print("No new downloads required. Updating products.json with current local mappings...")
    else:
        print(f"Starting concurrent downloads with 16 threads...")
        downloaded_count = 0
        success_count = 0
        
        # Download concurrently using 16 threads
        with ThreadPoolExecutor(max_workers=16) as executor:
            future_to_task = {executor.submit(process_download_task, t): t for t in tasks}
            
            for future in as_completed(future_to_task):
                p_id, image_type, local_path = future.result()
                downloaded_count += 1
                
                if local_path:
                    success_count += 1
                    if image_type == 'primary':
                        primary_results[p_id] = local_path
                    else:
                        # image_type is ('secondary', idx)
                        _, idx = image_type
                        secondary_results[p_id][idx] = local_path
                
                if downloaded_count % 10 == 0 or downloaded_count == len(tasks):
                    print(f"Progress: {downloaded_count}/{len(tasks)} downloads completed. ({success_count} succeeded)")
                    
    # Write back all results to products.json
    modified = False
    for p in products:
        p_id = p.get('id')
        
        # Primary
        if p_id in primary_results and primary_results[p_id]:
            if p.get('image') != primary_results[p_id]:
                p['image'] = primary_results[p_id]
                modified = True
                
        # Secondary
        if p_id in secondary_results:
            # Filter out any None values if they failed to download, keeping only valid local paths
            valid_secondaries = [url for url in secondary_results[p_id] if url]
            if p.get('images') != valid_secondaries:
                p['images'] = valid_secondaries
                modified = True
                
    if modified:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=4, ensure_ascii=False)
        print("products.json updated successfully with local assets!")
    else:
        print("No changes made to products.json.")

if __name__ == '__main__':
    main()
