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

    def find_by_prompt(self, prompt: str, options: list):
        """
        Savol matni bo'yicha bazadagi mavjud savollar ichidan eng yaqinini qidiradi
        va uning tasdiqlangan javobini joriy variantlar bilan solishtirib topadi.
        Qaytaradi: (option_id, option_text, confidence, reason) yoki None
        """
        try:
            from agent.solver import normalize_text
        except Exception:
            return None

        norm_p = normalize_text(prompt)
        if not norm_p:
            return None

        best_q = None
        best_p_score = 0.0

        for qid, q in self.data.get("questions", {}).items():
            qp = q.get("prompt", "")
            if not qp:
                continue
            norm_qp = normalize_text(qp)
            if norm_p == norm_qp:
                best_q = q
                best_p_score = 1.0
                break

            w1 = set(norm_p.split())
            w2 = set(norm_qp.split())
            if w1 and w2:
                jaccard = len(w1 & w2) / len(w1 | w2)
                if jaccard > best_p_score:
                    best_p_score = jaccard
                    best_q = q

        if best_q and best_p_score >= 0.70:
            target_text = normalize_text(best_q.get("option_text", ""))
            if not target_text:
                return None

            best_opt = None
            best_o_score = 0.0

            for opt in options:
                opt_text = opt.option_text if hasattr(opt, "option_text") else opt.get("optionText", "")
                opt_id = opt.id if hasattr(opt, "id") else opt.get("id", "")
                cur_norm = normalize_text(opt_text)

                if cur_norm == target_text:
                    return opt_id, opt_text, 1.0, f"Bilimlar bazasi aniq mosligi: '{best_q.get('prompt')[:40]}...'"

                w1 = set(cur_norm.split())
                w2 = set(target_text.split())
                if w1 and w2:
                    j = len(w1 & w2) / len(w1 | w2)
                    if j > best_o_score:
                        best_o_score = j
                        best_opt = (opt_id, opt_text)

            if best_opt and best_o_score >= 0.40:
                return best_opt[0], best_opt[1], best_o_score, f"Bilimlar bazasi varianti mosligi ({int(best_o_score*100)}%)"

        return None


