import os
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

def main():
    copy_directory('static', 'public')
    
if __name__ == "__main__":
    main()