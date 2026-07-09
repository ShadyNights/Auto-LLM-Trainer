import shutil
import os

dir_path = r"d:\Traveler LLM\src\ui\styles"
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
