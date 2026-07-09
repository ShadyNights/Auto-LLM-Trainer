import os

src_dir = r"d:\Traveler LLM\src"
for root, dirs, files in os.walk(src_dir):
    if "__pycache__" in root:
        continue
    init_file = os.path.join(root, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            pass
        print(f"Created {init_file}")
