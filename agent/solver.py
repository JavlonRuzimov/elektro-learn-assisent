import re
from typing import Optional, Tuple, List, Dict
from models.schemas import Question, QuestionOption
from agent.knowledge_base import KnowledgeBase

def transliterate_to_latin(text: str) -> str:
    """O'zbek kirill yozuvini lotin yozuviga o'girish"""
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ц': 's', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': "'",
        'ы': 'i', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ў': "o'", 'ғ': "g'", 'қ': 'q',
        'ҳ': 'h'
    }
    res = []
    text_lower = text.lower()
    for c in text_lower:
        res.append(mapping.get(c, c))
    return "".join(res)

def normalize_text(text: str) -> str:
    """Har xil apostroflar, tinish belgilari va ortiqcha bo'shliqlarni tozalash"""
    # Kirill bo'lsa lotinga o'giramiz
    text = transliterate_to_latin(text)
    # Apostroflar va belgilarni tekislash
    text = re.sub(r"['’`ʼ\"]", "", text)
    # Harflar va raqamlar qoldirish
    text = re.sub(r"[^\w\s]", " ", text)
    # Bo'shliqlarni normallashtirish
    return re.sub(r"\s+", " ", text).strip().lower()

class QuestionSolver:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def solve_single_choice(
        self,
        question: Question,
        theory_content: Optional[str] = None
    ) -> Tuple[str, float, str]:
        """
        SINGLE_CHOICE savoliga eng to'g'ri variantni topish.
        Qaytaradi: (selected_option_id, confidence, reason)
        """
        # 1. Bilimlar bazasidan tekshirish (100% ishonch)
        known_id = self.kb.get_known_answer(question.id)
        if known_id:
            for opt in question.options:
                if opt.id == known_id:
                    return opt.id, 1.0, f"Bilimlar bazasidan tasdiqlangan: '{opt.option_text[:40]}...'"

        if not question.options:
            return "", 0.0, "Variantlar mavjud emas"

        # 2. Nazariya matni bo'yicha qidirish
        if theory_content:
            norm_theory = normalize_text(theory_content)
            norm_prompt = normalize_text(question.prompt)

            best_opt = None
            max_score = -1.0
            best_reason = ""

            # Nazariyadan savol mavzusiga eng yaqin jumlani topish
            prompt_words = [w for w in norm_prompt.split() if len(w) > 3]

            for opt in question.options:
                opt_text = opt.option_text.strip()
                if not opt_text:
                    continue
                norm_opt = normalize_text(opt_text)

                # Aniq to'liq jumla bormi?
                if norm_opt in norm_theory:
                    return opt.id, 0.98, f"Nazariya matnida so'zma-so'z mos keldi: '{opt_text[:35]}...'"

                # So'zlar kesishuvini hisoblash
                opt_words = [w for w in norm_opt.split() if len(w) > 2]
                if not opt_words:
                    continue

                matched_words = [w for w in opt_words if w in norm_theory]
                match_ratio = len(matched_words) / len(opt_words)

                # Agar variantdagi raqamlar nazariyada aynan mavjud bo'lsa
                opt_numbers = re.findall(r'\d+', norm_opt)
                num_score = 0.0
                if opt_numbers:
                    matched_nums = [n for n in opt_numbers if n in norm_theory]
                    num_score = len(matched_nums) / len(opt_numbers)

                # Umumiy ball
                total_score = (match_ratio * 0.7) + (num_score * 0.3)

                if total_score > max_score:
                    max_score = total_score
                    best_opt = opt
                    best_reason = f"Nazariyaga moslik: {int(match_ratio*100)}%"

            if best_opt and max_score > 0.4:
                return best_opt.id, min(0.95, 0.6 + max_score * 0.3), best_reason

        # 3. Fallback: variantlar ichida eng to'liq va aniq tushuntirish berilgani
        sorted_opts = sorted(question.options, key=lambda o: len(o.option_text), reverse=True)
        chosen = sorted_opts[0]
        return chosen.id, 0.3, "Hevristik tahlil (batafsil variant)"

    def solve_matching(self, question: Question) -> List[Dict[str, str]]:
        """
        MATCHING (moslashtirish) savoliga javob juftliklarini tuzish.
        """
        pairs = []
        for opt in question.options:
            pairs.append({
                "leftOptionId": opt.id,
                "rightOptionId": opt.id
            })
        return pairs
