import time
import random
from typing import Optional, Callable, List
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase
from agent.solver import QuestionSolver
from models.schemas import Question, AnswerResult

class AgentRunner:
    def __init__(
        self,
        client: ElektroLearnClient,
        kb: Optional[KnowledgeBase] = None,
        delay_min: float = 1.5,
        delay_max: float = 3.0,
        logger: Optional[Callable[[str], None]] = None
    ):
        self.client = client
        self.kb = kb or KnowledgeBase()
        self.solver = QuestionSolver(self.kb)
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.log = logger or print

    def _sleep_pacing(self):
        sleep_time = random.uniform(self.delay_min, self.delay_max)
        time.sleep(sleep_time)

    def submit_single_question(
        self,
        question: Question,
        theory_content: Optional[str] = None,
        source: str = "LESSON"
    ) -> AnswerResult:
        """Bitta savolni yechish va yuborish, to'g'ri javobni bazaga yozish"""
        self.log(f"\n[Savol]: {question.prompt}")

        if question.type == "SINGLE_CHOICE":
            opt_id, conf, reason = self.solver.solve_single_choice(question, theory_content)
            selected_opt = next((o for o in question.options if o.id == opt_id), None)
            opt_title = selected_opt.option_text if selected_opt else opt_id
            self.log(f"  -> Tanlov: '{opt_title[:50]}' (Ishonch: {int(conf*100)}%, {reason})")

            # Human-like delay
            self._sleep_pacing()

            res = None
            for attempt in range(3):
                try:
                    res = self.client.progress.submit_answer(question.id, opt_id, source=source)
                    break
                except Exception as e:
                    self.log(f"  [!] Qayta urinish ({attempt+1}/3): {e}")
                    time.sleep(3)

            if not res:
                return AnswerResult(is_correct=False)

            # Natijani tekshirish va bilimlar bazasiga saqlash
            correct_id = res.correct_option_id or (opt_id if res.is_correct else None)
            if correct_id:
                correct_opt = next((o for o in question.options if o.id == correct_id), None)
                correct_text = correct_opt.option_text if correct_opt else ""
                self.kb.record_answer(question.id, question.prompt, correct_id, correct_text)

            if res.is_correct:
                self.log(f"  [+] TO'G'RI! (+{res.xp_earned} XP)")
            else:
                self.log(f"  [-] Noto'g'ri. Server to'g'ri javobi: '{correct_text[:40]}' (Bazaga yozildi)")

            return res

        elif question.type == "MATCHING":
            pairs = self.solver.solve_matching(question)
            self._sleep_pacing()
            res = None
            for attempt in range(3):
                try:
                    res = self.client.progress.submit_matching(question.id, pairs, source=source)
                    break
                except Exception as e:
                    self.log(f"  [!] Qayta urinish ({attempt+1}/3): {e}")
                    time.sleep(3)

            if not res:
                return AnswerResult(is_correct=False)

            status_text = "TO'G'RI" if res.is_correct else "Noto'g'ri"
            self.log(f"  [Moslashtirish natijasi]: {status_text}")
            return res

        else:
            self.log(f"  [!] Noma'lum savol turi: {question.type}")
            return AnswerResult(is_correct=False)

    def complete_daily_plan(self):
        """Bugungi kunlik rejani to'liq bajarish"""
        self.log("\n=== KUNLIK REJANI BAJARISH BOSHLANDI ===")
        today = self.client.daily_plan.get_today()
        self.log(f"Bugungi holat: {today.answered_count}/{today.target_questions} ({today.completion_percent}%)")

        if today.completed or today.completion_percent >= 100:
            self.log("Bugungi reja allaqachon 100% bajarilgan!")
            return today

        while True:
            try:
                self.client.auth.send_heartbeat()
            except Exception:
                pass

            question = self.client.daily_plan.get_next_question()
            if not question:
                self.log("Boshqa savol topilmadi yoki reja yakunlandi.")
                break

            res = self.submit_single_question(question, source="DAILY_PLAN")

            today = self.client.daily_plan.get_today()
            self.log(f"Progress: {today.answered_count}/{today.target_questions} ({today.completion_percent}%)")

            if today.completed or today.completion_percent >= 100:
                self.log("Tabriklaymiz! Bugungi kunlik reja 100% yakunlandi!")
                break

        return today

    def complete_theory_questions(self, theory_id: str, theory_title: str, theory_content: str):
        """Berilgan nazariya savollarini yechish (continue va retry)"""
        self.log(f"\n--- Nazariya: '{theory_title}' savollari yechilmoqda ---")
        self.kb.record_theory(theory_id, theory_title, theory_content)

        max_loops = 20
        loop = 0
        while loop < max_loops:
            loop += 1
            try:
                q_data = self.client.progress.get_theory_questions(theory_id, mode="continue")
            except Exception as e:
                self.log(f"  [!] Savollarni olishda xatolik: {e}, 3 soniya kutilmoqda...")
                time.sleep(3)
                continue

            questions: List[Question] = q_data.get("questions", [])

            if not questions or q_data.get("is_module_complete"):
                self.log(f"'{theory_title}' bo'yicha barcha savollar yechildi (isModuleComplete=True).")
                break

            self.log(f"  Qolgan savollar soni: {len(questions)}")
            for q in questions:
                try:
                    self.client.auth.send_heartbeat()
                except Exception:
                    pass
                self.submit_single_question(q, theory_content=theory_content, source="LESSON")

        # Retry bosqichi (agar to'liq 100% bo'lmagan bo'lsa)
        try:
            q_data = self.client.progress.get_theory_questions(theory_id, mode="continue")
            if not q_data.get("is_module_complete") and q_data.get("answered_count", 0) < q_data.get("total_questions", 1):
                self.log(f"'{theory_title}' uchun xatolarni tuzatish (retry rejimi)...")
                retry_data = self.client.progress.get_theory_questions(theory_id, mode="retry")
                retry_questions = retry_data.get("questions", [])
                for q in retry_questions:
                    self.submit_single_question(q, theory_content=theory_content, source="LESSON")
        except Exception as e:
            self.log(f"  [!] Retry bosqichida ogohlantirish: {e}")

    def complete_active_level(self, level_id: str):
        """Daraja ichidagi barcha nazariyalarni bosqichma-bosqich 100% bajarish"""
        self.log(f"\n=======================================================")
        self.log(f"  DARAJA (LEVEL: {level_id}) BAJARISH BOSHLANDI")
        self.log(f"=======================================================")
        level = self.client.progress.get_level_detail(level_id)
        self.log(f"Level nomi: {level.title}")
        self.log(f"Nazariyalar soni: {len(level.theories)}")

        for t in level.theories:
            self.log(f"\n>> Mavzu: '{t.title}' ({t.answered_questions}/{t.total_questions} yechilgan)")
            if not t.is_complete:
                self.complete_theory_questions(t.id, t.title, t.content)
            else:
                self.log("Bu mavzu allaqachon 100% yechilgan.")

        self.log(f"\n=======================================================")
        self.log(f"  DARAJA ({level.title}) BO'YICHA ISH YAKUNLANDI")
        self.log(f"=======================================================")

    def complete_all_levels(self):
        """Barcha ochiq darajalarni birin-ketin 100% bajarib, yangi darajalarni ochish"""
        self.log("\n=======================================================")
        self.log("      BARCHA LEVEL-LARNI 100% BAJARISH BOSHLANDI       ")
        self.log("=======================================================")

        while True:
            try:
                prog = self.client.progress.get_progress()
            except Exception as e:
                self.log(f"Progress olishda xatolik: {e}, 3 soniya kutilmoqda...")
                time.sleep(3)
                continue

            target_level = None
            for lvl in prog.levels:
                if not lvl.is_locked and (not lvl.is_completed or lvl.completion_percent < 100):
                    target_level = lvl
                    break

            if not target_level:
                self.log("\n[!] Barcha ochiq darajalar 100% yakunlandi!")
                break

            self.log(f"\n[>>>] Yangi maqsadli daraja: {target_level.title}")
            self.log(f"      Hozirgi progress: {target_level.completion_percent}% ({target_level.correct_answers_count} to'g'ri)")
            self.complete_active_level(target_level.id)

            # Yangilangan progressni tekshirish
            time.sleep(2)
            try:
                updated_prog = self.client.progress.get_progress()
                updated_lvl = next((l for l in updated_prog.levels if l.id == target_level.id), None)
                if updated_lvl:
                    self.log(f"\n[Natija]: {updated_lvl.title} -> {updated_lvl.completion_percent}%")
            except Exception:
                pass

        self.log("\n=======================================================")
        self.log("         BARCHA DARAJALAR TO'LIQ YAKUNLANDI!           ")
        self.log("=======================================================")
