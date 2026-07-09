import shutil
import os

pages_dir = r"d:\Traveler LLM\src\ui\pages"
if os.path.exists(pages_dir):
    shutil.rmtree(pages_dir)
    print(f"Deleted {pages_dir}")
