import os
import json
from typing import Dict, Any, Optional

class KnowledgeBase:
    def __init__(self, storage_path: str = "data/knowledge_base.json"):
        self.storage_path = storage_path
        self.data: Dict[str, Any] = {
            "questions": {},  # question_id -> { "correct_option_id": ..., "prompt": ..., "option_text": ... }
            "theories": {},   # theory_id -> { "title": ..., "content": ... }
        }
        self.load()

    def load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                pass

    def save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def record_answer(self, question_id: str, prompt: str, correct_option_id: str, option_text: str = ""):
        if not question_id or not correct_option_id:
            return
        self.data["questions"][question_id] = {
            "correct_option_id": correct_option_id,
            "prompt": prompt,
            "option_text": option_text
        }
        self.save()

    def get_known_answer(self, question_id: str) -> Optional[str]:
        q = self.data["questions"].get(question_id)
        if q:
            return q.get("correct_option_id") or q.get("correctOptionId")
        return None

    def record_theory(self, theory_id: str, title: str, content: str):
        self.data["theories"][theory_id] = {
            "title": title,
            "content": content
        }
        self.save()

    def get_theory_content(self, theory_id: str) -> str:
        t = self.data["theories"].get(theory_id)
        if t:
            return t.get("content", "")
        return ""

