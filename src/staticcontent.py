import os
import shutil


def copy_static_to_public(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        print(f"Deleting contents of {dest_dir}...")
        shutil.rmtree(dest_dir)
    
    os.makedirs(dest_dir, exist_ok=True)
    print(f"Created directory: {dest_dir}")
    
    _copy_directory_contents(source_dir, dest_dir)


def _copy_directory_contents(src, dst):
    if not os.path.exists(src):
        print(f"Source directory does not exist: {src}")
        return
    
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        
        elif os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            print(f"Created directory: {dst_path}")
            _copy_directory_contents(src_path, dst_path)