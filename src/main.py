import os
import sys
from block_markdown import markdown_to_html_node
from textnode import TextNode, TextType

def copy_directory(src, dest):
    # we want to write a recursive copy function that first deletes all existing files in the destination directory and then copy all files, subdirectories, nested files, etc. And also log out each file path that is copied for debugging
    if os.path.exists(dest):
        for root, dirs, files in os.walk(dest, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.rmdir(dir_path)
                print(f"Deleted directory: {dir_path}")
    os.makedirs(dest, exist_ok=True)
    for root, dirs, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, relative_path)
        os.makedirs(dest_dir, exist_ok=True)
        for name in files:
            src_file = os.path.join(root, name)
            dest_file = os.path.join(dest_dir, name)
            with open(src_file, 'rb') as fsrc:
                with open(dest_file, 'wb') as fdst:
                    fdst.write(fsrc.read())
            print(f"Copied file: {src_file} to {dest_file}")
            
def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError("No title found in markdown")

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    # read markdown at from_path
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    # read template at template_path
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    # convert markdown to html node
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', content)
    
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    # write to dest_path and create directories as needed
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template)

def generate_page_recursive(basepath, from_path, template_path, dest_path):
    if os.path.isdir(from_path):
        for entry in os.listdir(from_path):
            entry_from_path = os.path.join(from_path, entry)
            entry_dest_path = os.path.join(dest_path, entry)
            generate_page_recursive(basepath, entry_from_path, template_path, entry_dest_path)
    elif from_path.endswith('.md'):
        dest_file_path = dest_path[:-3] + '.html'  # change .md to .html
        generate_page(basepath,from_path, template_path, dest_file_path)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    copy_directory('static', 'public')
    generate_page_recursive(basepath, 'content', 'template.html', 'docs')
    
if __name__ == "__main__":
    main()