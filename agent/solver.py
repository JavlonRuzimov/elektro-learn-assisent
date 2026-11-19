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

class SmartSolver:
    """
    Ko'p bosqichli to'liq avtonom aqlli savol yechuvchi:
    1-bosqich: Tasdiqlangan ID bo'yicha (VERIFIED_ANSWERS va KB ID)
    2-bosqich: Bilimlar bazasi matn / semantik mosligi (514+ tasdiqlangan savollar)
    3-bosqich: Kutubxona qoidalari va me'yoriy hujjatlar matnidan chuqur qidirish (15 ta rasmiy hujjat)
    4-bosqich: Me'yoriy testlar umumlashtiruvchi qonuniyati (masalan: 'a, b va v', 'barcha javoblar to'g'ri')
    5-bosqich: Eng batafsil va to'liq texnik variant
    """
    def __init__(self, kb: Optional[KnowledgeBase] = None, library = None):
        self.kb = kb or KnowledgeBase()
        if library is None:
            try:
                from library_searcher import LibraryKnowledge
                self.library = LibraryKnowledge()
            except Exception:
                self.library = None
        else:
            self.library = library

    def find_best_answer(self, question: Question) -> Tuple[str, str, bool]:
        """
        Eng to'g'ri variantni topadi.
        Qaytaradi: (selected_option_id, reason, is_known_in_kb)
        """
        if not question.options:
            return "", "Variantlar mavjud emas", False

        # 1. Aniq ID bo'yicha tekshirish
        try:
            from autopilot import VERIFIED_ANSWERS
        except Exception:
            VERIFIED_ANSWERS = {}

        known_id = VERIFIED_ANSWERS.get(question.id) or self.kb.get_known_answer(question.id)
        if known_id:
            for opt in question.options:
                if opt.id == known_id:
                    return opt.id, "Bilimlar bazasidan tasdiqlangan ID (100%)", True

        # 2. Savol matni bo'yicha KB dan qidirish (514+ savollar)
        kb_match = self.kb.find_by_prompt(question.prompt, question.options)
        if kb_match:
            opt_id, opt_text, score, reason = kb_match
            return opt_id, f"{reason} (Ishonch: {int(score*100)}%)", True

        # 3. Rasmiy kutubxona hujjatlaridan qidirish
        lib_opt_id = None
        lib_score = 0.0
        lib_reason = ""
        if self.library:
            try:
                lib_opt_id, lib_score, lib_reason = self.library.solve_question(question)
                if lib_opt_id and lib_score >= 0.40:
                    return lib_opt_id, f"{lib_reason}", False
            except Exception as e:
                pass

        # 4. Me'yoriy testlar umumlashtiruvchi variantlar qonuniyati
        # O'zbekiston MET testlarida agar ushbu variantlar bo'lsa 95% hollarda to'g'ri javob bo'ladi
        collective_patterns = [
            'barcha javoblar', 'hamma javoblar', 'barchasi to', 'yuqoridagilarning barchasi',
            'a b va v', 'a b va g', 'a b va d', 'a va b javoblar', 'a va v javoblar'
        ]
        for opt in question.options:
            t = opt.option_text.lower()
            cleaned = re.sub(r'[^a-z0-9\s]', ' ', t)
            s_clean = ' '.join(cleaned.split())
            if any(p in s_clean for p in collective_patterns):
                return opt.id, f"Me'yoriy qonuniyat (Umumlashtiruvchi variant: '{opt.option_text}')", False

        # 5. Agar kutubxonada pastroq bo'lsa ham moslik chiqqan bo'lsa
        if lib_opt_id:
            return lib_opt_id, f"Kutubxona yaqin mosligi: {lib_reason}", False

        # 6. Fallback: eng batafsil va mukammal texnik variant
        sorted_opts = sorted(question.options, key=lambda o: len(o.option_text.strip()), reverse=True)
        chosen = sorted_opts[0]
        return chosen.id, f"Hevristik tahlil (Batafsil texnik variant: '{chosen.option_text[:40]}...')", False

