import json
import os
import re

CYRILLIC_TO_LATIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '',
    'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ў': 'o', 'қ': 'q',
    'ғ': 'g', 'ҳ': 'h'
}

def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = text.lower()
    t = re.sub(r"[‘ʼʻ\'`\"]", "", t)
    for c, l in CYRILLIC_TO_LATIN.items():
        t = t.replace(c, l)
    return t

class KBSearcher:
    def __init__(self, kb_path="data/knowledge_base.json", all_500_path="data/all_500_questions.json"):
        self.kb_path = kb_path
        self.all_500_path = all_500_path
        self.kb_data = {}
        self.all_500 = []
        self._load()

    def _load(self):
        if os.path.exists(self.kb_path):
            try:
                with open(self.kb_path, "r", encoding="utf-8") as f:
                    self.kb_data = json.load(f).get("questions", {})
            except Exception:
                self.kb_data = {}
        if os.path.exists(self.all_500_path):
            try:
                with open(self.all_500_path, "r", encoding="utf-8") as f:
                    self.all_500 = json.load(f)
            except Exception:
                self.all_500 = []

    def _resolve_option_text(self, qid, opt_id, current_text):
        if current_text and not current_text.startswith("Verified"):
            return current_text

        # Search all_500
        for th in self.all_500:
            for q in th.get("questions", []):
                if q.get("id") == qid:
                    for o in q.get("options", []):
                        if o.get("id") == opt_id:
                            return o.get("optionText") or o.get("text") or current_text
        return current_text

    def search(self, query: str, limit: int = 3):
        self._load()
        q_norm = normalize_text(query)
        q_words = [w for w in re.sub(r"[^a-z0-9]", " ", q_norm).split() if len(w) > 2]
        if not q_words:
            return []

        scored = []
        seen_prompts = set()

        for qid, qdata in self.kb_data.items():
            prompt = qdata.get("prompt", "")
            if not prompt:
                continue

            clean_prompt = prompt.strip().lower()
            if clean_prompt in seen_prompts:
                continue

            opt_id = qdata.get("correctOptionId") or qdata.get("correct_option_id")
            opt_text = self._resolve_option_text(qid, opt_id, qdata.get("option_text", ""))

            p_norm = normalize_text(prompt)
            o_norm = normalize_text(opt_text)

            score = 0
            # Exact phrase bonus
            if q_norm in p_norm:
                score += 15
            elif q_norm in o_norm:
                score += 10

            # Token scores
            for w in q_words:
                if w in p_norm:
                    score += 4
                if w in o_norm:
                    score += 2

            if score > 0:
                seen_prompts.add(clean_prompt)
                scored.append({
                    "qid": qid,
                    "prompt": prompt,
                    "answer": opt_text or "To'g'ri javob tasdiqlangan",
                    "score": score
                })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]
