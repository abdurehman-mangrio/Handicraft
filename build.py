import os
import re

def compile_file(src_path, templates_dir):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all <!-- INCLUDE: filename --> patterns
    pattern = r'<!--\s*INCLUDE:\s*([^\s]+)\s*-->'
    
    def replace_include(match):
        filename = match.group(1).strip()
        filepath = os.path.join(templates_dir, filename)
        if os.path.exists(filepath):
            # Recursively compile in case templates contain includes
            return compile_file(filepath, templates_dir)
        else:
            print(f"Warning: Template {filepath} not found.")
            return match.group(0)
            
    compiled_content = re.sub(pattern, replace_include, content)
    return compiled_content

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    templates_dir = os.path.join(current_dir, 'templates')
    dest_dir = current_dir # Output to root folder
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory {src_dir} does not exist.")
        return
        
    print("Compiling pages...")
    for filename in os.listdir(src_dir):
        if filename.endswith('.html'):
            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(dest_dir, filename)
            
            print(f"- Compiling {filename} -> {dest_path}")
            compiled_html = compile_file(src_path, templates_dir)
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(compiled_html)
                
    print("Layout preprocessor compilation completed successfully!")

if __name__ == '__main__':
    main()
