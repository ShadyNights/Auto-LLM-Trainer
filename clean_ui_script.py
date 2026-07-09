import shutil
import os

for p in [r"d:\Traveler LLM\src\ui\styles", r"d:\Traveler LLM\src\ui\design"]:
    if os.path.exists(p):
        try:
            shutil.rmtree(p)
            print(f"Removed {p}")
        except Exception as e:
            print(f"Failed to remove {p}: {e}")
