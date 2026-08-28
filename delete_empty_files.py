import os

def main():
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'products')
    if not os.path.exists(target_dir):
        print("Directory does not exist.")
        return
        
    deleted_count = 0
    failed_count = 0
    
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            path = os.path.join(root, f)
            try:
                if os.path.exists(path) and os.path.getsize(path) == 0:
                    os.remove(path)
                    print(f"Removed: {f}")
                    deleted_count += 1
            except Exception as e:
                print(f"Failed to remove {f}: {e}")
                failed_count += 1
                
    print(f"Cleanup complete. Deleted: {deleted_count}, Failed: {failed_count}")

if __name__ == '__main__':
    main()
