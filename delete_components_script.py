import os

file_to_delete = r"d:\Traveler LLM\src\ui\components.py"
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Deleted {file_to_delete}")
