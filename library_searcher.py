import os
import glob
import re
from typing import List, Tuple, Optional
from models.schemas import Question, QuestionOption
from agent.solver import normalize_text

class LibraryKnowledge:
    def __init__(self, library_dir: str = "data/library_extracted"):
        self.library_dir = library_dir
        self.documents = [] # list of {"name": fname, "paragraphs": [norm_p1, norm_p2, ...]}
        self._load_corpus()

    def _load_corpus(self):
        txt_files = glob.glob(os.path.join(self.library_dir, "*.txt"))
        for fpath in txt_files:
            fname = os.path.basename(fpath)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Matnni paragraflarga (yoki 300-500 so'zli bo'laklarga) bo'lamiz
                raw_paras = [p.strip() for p in re.split(r'\n{2,}|\.\s{2,}', content) if len(p.strip()) > 30]
                norm_paras = [normalize_text(p) for p in raw_paras]
                
                self.documents.append({
                    "name": fname,
                    "raw_paras": raw_paras,
                    "norm_paras": norm_paras
                })
            except Exception as e:
                print(f"[!] Xato {fname}: {e}")
        print(f"[LibraryKnowledge] Yuklangan kutubxona hujjatlari: {len(self.documents)} ta")

    def find_relevant_paragraphs(self, prompt: str, top_k: int = 5) -> List[Tuple[str, str, float]]:
        """
        Savol matni bo'yicha eng yaqin bo'laklarni topish.
        Qaytaradi: [(doc_name, norm_para, score), ...]
        """
        norm_prompt = normalize_text(prompt)
        prompt_words = [w for w in norm_prompt.split() if len(w) > 3]
        if not prompt_words:
            return []

        scored_paras = []
        for doc in self.documents:
            doc_name = doc["name"]
            for norm_p in doc["norm_paras"]:
                # Prompt so'zlarining uchrashini hisoblash
                matches = sum(1 for w in prompt_words if w in norm_p)
                if matches >= 2: # Kamida 2 ta kalit so'z mos tushsa
                    score = matches / len(prompt_words)
                    scored_paras.append((doc_name, norm_p, score))

        scored_paras.sort(key=lambda x: x[2], reverse=True)
        return scored_paras[:top_k]

    def solve_question(self, question: Question) -> Tuple[Optional[str], float, str]:
        """
        Kutubxona hujjatlaridan qidirib eng mos variantni topadi.
        """
        if not question.options:
            return None, 0.0, "Variantlar mavjud emas"

        # 1. Savolga tegishli bo'laklarni topamiz
        relevant_paras = self.find_relevant_paragraphs(question.prompt, top_k=6)
        if not relevant_paras:
            return None, 0.0, "Kutubxonada tegishli mavzu topilmadi"

        best_opt_id = None
        best_score = -1.0
        best_reason = ""

        # Topilgan tegishli bo'laklar matnini birlashtiramiz
        combined_text = " ".join([p[1] for p in relevant_paras])
        best_doc = relevant_paras[0][0]

        for opt in question.options:
            opt_text = opt.option_text.strip()
            if not opt_text:
                continue
            norm_opt = normalize_text(opt_text)

            # 1. To'g'ridan-to'g'ri to'liq jumla tegishli bo'lakda bormi?
            if len(norm_opt) > 5 and norm_opt in combined_text:
                score = 2.0
                if score > best_score:
                    best_score = score
                    best_opt_id = opt.id
                    best_reason = f"Kutubxona matnida aniq jumla topildi ({best_doc})"
                continue

            # 2. Variant so'zlari mosligi
            opt_words = [w for w in norm_opt.split() if len(w) > 2]
            if not opt_words:
                continue

            matched_words = [w for w in opt_words if w in combined_text]
            word_ratio = len(matched_words) / len(opt_words)

            # Raqamlar tekshiruvi (agar variantda aniq raqam/yil/metr bo'lsa)
            opt_nums = re.findall(r'\d+', norm_opt)
            num_ratio = 0.0
            if opt_nums:
                matched_nums = [n for n in opt_nums if n in combined_text]
                num_ratio = len(matched_nums) / len(opt_nums)

            total_score = (word_ratio * 0.7) + (num_ratio * 0.3)
            if total_score > best_score and total_score > 0.4:
                best_score = total_score
                best_opt_id = opt.id
                best_reason = f"Kutubxonada yuqori moslik ({int(total_score*100)}%, {best_doc})"

        return best_opt_id, best_score, best_reason
