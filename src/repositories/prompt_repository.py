import os
import hashlib
from typing import Optional, Dict

class PromptRepository:
    def __init__(self, prompts_dir: str = "prompts/travel"):
        self.prompts_dir = prompts_dir

    def get_prompt_text(self, version_name: str) -> Optional[str]:
        filepath = os.path.join(self.prompts_dir, f"{version_name}.md")
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def get_checksum(self, version_name: str) -> Optional[str]:
        text = self.get_prompt_text(version_name)
        if text is None:
            return None
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
