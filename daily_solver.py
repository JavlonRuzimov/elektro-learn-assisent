import time
from typing import Dict, Any, Tuple
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase
from library_searcher import LibraryKnowledge
from autopilot import VERIFIED_ANSWERS, choose_answer

class DailyPlanSolver:
    def __init__(self):
        self.client = ElektroLearnClient()
        self.kb = KnowledgeBase()
        self.library = LibraryKnowledge()

    def get_profile_info(self) -> Dict[str, Any]:
        """Foydalanuvchi profili, energiya va reyting ma'lumotlarini olish"""
        try:
            me = self.client.base_client.get('/progress/me')
            user = me.get('user', {})
            hearts = me.get('hearts', {})
            prog = self.client.progress.get_progress()
            
            return {
                "name": user.get('name', 'Noma\'lum'),
                "email": user.get('email', ''),
                "hearts": hearts.get('heartsCount', 0),
                "max_hearts": hearts.get('maxHearts', 5),
                "total_xp": prog.total_xp,
                "badge": prog.badge_label,
                "completed_levels": prog.completed_levels,
                "total_levels": len(prog.levels)
            }
        except Exception as e:
            return {"error": str(e)}

    def check_daily_plan_status(self) -> Dict[str, Any]:
        """Kunlik reja holatini tekshirish"""
        try:
            plan = self.client.daily_plan.get_today()
            return {
                "is_plan_day": plan.is_plan_day,
                "target_questions": plan.target_questions,
                "answered_count": plan.answered_count,
                "correct_count": plan.correct_count,
                "completion_percent": plan.completion_percent,
                "completed": plan.completed
            }
        except Exception as e:
            return {"error": str(e)}

    def solve_daily_plan(self, progress_callback=None) -> Dict[str, Any]:
        """
        Bugungi 10 ta kunlik reja savollarini to'liq yechish.
        progress_callback(current, total, prompt, is_correct) orqali xabar uzatadi.
        """
        plan = self.client.daily_plan.get_today()
        if not plan.is_plan_day:
            return {"status": "NO_PLAN_TODAY", "message": "Bugun dam olish kuni, kunlik reja belgilanmagan."}

        if plan.completed or plan.completion_percent >= 100:
            return {"status": "ALREADY_COMPLETED", "message": "Bugungi kunlik reja allaqachon 100% bajarilgan (+100 XP olingan)!"}

        total_target = plan.target_questions or 10
        solved_count = plan.answered_count
        results = []

        while solved_count < total_target:
            # Heartbeat
            try:
                self.client.auth.send_heartbeat()
            except Exception:
                pass

            question = self.client.daily_plan.get_next_question()
            if not question:
                break

            opt_id, source_reason = choose_answer(question)
            if not opt_id:
                return {
                    "status": "STOPPED",
                    "message": f"Savol bazada topilmadi: '{question.prompt[:70]}...'. Taxmin qilish taqiqlangani sababli to'xtatildi.",
                    "details": results
                }
            opt_text = next((o.option_text for o in question.options if o.id == opt_id), opt_id)

            time.sleep(1.5)
            try:
                res = self.client.progress.submit_answer(question.id, opt_id, source="DAILY_PLAN")
            except Exception as e:
                time.sleep(3)
                try:
                    res = self.client.progress.submit_answer(question.id, opt_id, source="DAILY_PLAN")
                except Exception as e2:
                    return {"status": "ERROR", "message": f"Savol topshirishda xatolik: {e2}"}

            if res.is_correct:
                VERIFIED_ANSWERS[question.id] = opt_id
                self.kb.record_answer(question.id, question.prompt, opt_id, opt_text)
                results.append({"prompt": question.prompt, "is_correct": True, "opt": opt_text})
            else:
                correct_id = res.correct_option_id
                correct_text = next((o.option_text for o in question.options if o.id == correct_id), correct_id)
                if correct_id:
                    VERIFIED_ANSWERS[question.id] = correct_id
                    self.kb.record_answer(question.id, question.prompt, correct_id, correct_text)
                results.append({"prompt": question.prompt, "is_correct": False, "opt": opt_text, "correct": correct_text})

            solved_count += 1
            if progress_callback:
                progress_callback(solved_count, total_target, question.prompt, res.is_correct)

            time.sleep(1.2)

        # Qayta tekshirish
        time.sleep(1)
        final_plan = self.client.daily_plan.get_today()
        return {
            "status": "SUCCESS",
            "solved": solved_count,
            "total": total_target,
            "correct_count": final_plan.correct_count,
            "completion_percent": final_plan.completion_percent,
            "bonus_xp": 100 if final_plan.completed else 0,
            "details": results
        }
