import time
from typing import Dict, Any, Tuple
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase
from library_searcher import LibraryKnowledge
from agent.solver import SmartSolver
from autopilot import VERIFIED_ANSWERS

class DailyPlanSolver:
    def __init__(
        self,
        client: Optional[ElektroLearnClient] = None,
        token: Optional[str] = None,
        kb: Optional[KnowledgeBase] = None,
        library: Optional[LibraryKnowledge] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        if client:
            self.client = client
        elif token:
            self.client = ElektroLearnClient(token=token)
        else:
            self.client = ElektroLearnClient()

        self.username = username
        self.password = password
        self.kb = kb or KnowledgeBase()
        self.library = library or LibraryKnowledge()
        self.solver = SmartSolver(kb=self.kb, library=self.library)

    def get_profile_info(self) -> Dict[str, Any]:
        """Foydalanuvchi profili, energiya va reyting ma'lumotlarini olish"""
        try:
            me = self.client.base_client.get('/progress/me')
            hearts = me.get('hearts', {})
            prog = self.client.progress.get_progress()

            user_obj = None
            try:
                user_obj = self.client.auth.get_me()
            except Exception:
                pass

            full_name = f"{user_obj.first_name} {user_obj.last_name}" if user_obj else "Sabirjan Ruzimov"
            email = user_obj.email if user_obj else "s.ruzimov2774"
            branch = user_obj.organizations[0].name if user_obj and user_obj.organizations else "Xorazm MET"

            rank = "Noma'lum"
            try:
                lb = self.client.leaderboard.get_organization()
                rank = lb.get("me", {}).get("rank", "Noma'lum")
            except Exception:
                pass
            
            return {
                "name": full_name,
                "email": email,
                "branch": branch,
                "rank": rank,
                "hearts": hearts.get('heartsCount', 0),
                "max_hearts": hearts.get('maxHearts', 5),
                "total_xp": prog.total_xp,
                "badge": prog.badge_label,
                "completed_levels": prog.completed_levels,
                "total_levels": len(prog.levels)
            }
        except Exception as e:
            return {"error": str(e)}

    def _ensure_token(self):
        """Token muddati tugashidan oldin uni avtomatik yangilash"""
        try:
            from auth_manager import AuthManager
            tok = self.client.base_client.token
            if AuthManager.is_token_expired(tok, buffer_seconds=300):
                save_env = (self.username is None)
                new_tok = AuthManager.login(username=self.username, password=self.password, save_to_env=save_env)
                self.client.set_token(new_tok)
        except Exception:
            pass

    def _wait_for_hearts(self):
        """Agar energiya (yuraklar) 0 bo'lsa, tiklanish vaqtigacha kutish"""
        print("[DailySolver] Energiya 0/5. Tiklanish kutilmoqda...")
        while True:
            try:
                me_data = self.client.base_client.get('/progress/me')
                hearts = me_data.get('hearts', {})
                cur_hearts = hearts.get('heartsCount', 0)
                if cur_hearts > 0:
                    print(f"[DailySolver] Energiya tiklandi ({cur_hearts}/5)!")
                    return cur_hearts
                
                regen_str = hearts.get('nextRegenAt', '')
                if regen_str:
                    from datetime import datetime, timezone
                    regen_dt = datetime.fromisoformat(regen_str.replace("Z", "+00:00"))
                    now_dt = datetime.now(timezone.utc)
                    wait_sec = max(5, int((regen_dt - now_dt).total_seconds()) + 5)
                    print(f"[DailySolver] Energiya 0/5. Tiklanish vaqti: {wait_sec} soniya...")
                    time.sleep(wait_sec)
                else:
                    time.sleep(60)
            except Exception as e:
                print(f"[DailySolver] Energiya tekshirish xatosi: {e}")
                time.sleep(30)

    def check_daily_plan_status(self) -> Dict[str, Any]:
        """Kunlik reja holatini tekshirish"""
        self._ensure_token()
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
        Bazada yo'q yangi savollar chiqsa, bot o'zi kutubxona va me'yoriy
        hujjatlardan qidirib tanlaydi; to'g'ri bo'lsa darhol bilimlar bazasiga qo'shadi!
        """
        self._ensure_token()
        plan = self.client.daily_plan.get_today()
        if not plan.is_plan_day:
            return {"status": "NO_PLAN_TODAY", "message": "Bugun dam olish kuni, kunlik reja belgilanmagan."}

        if plan.completed or plan.completion_percent >= 100:
            return {"status": "ALREADY_COMPLETED", "message": "Bugungi kunlik reja allaqachon 100% bajarilgan (+100 XP olingan)!"}

        total_target = plan.target_questions or 10
        correct_count = plan.correct_count
        results = []
        new_learned_count = 0
        attempts = 0
        max_attempts = 25  # Cheksiz sikldan himoya

        while (correct_count < total_target) and (not plan.completed) and (attempts < max_attempts):
            attempts += 1
            # 1. Heartbeat
            try:
                self.client.auth.send_heartbeat()
            except Exception:
                pass

            # 2. Energiya (yuraklar) 0 bo'lsa kutish
            try:
                me_data = self.client.base_client.get('/progress/me')
                hearts_cnt = me_data.get('hearts', {}).get('heartsCount', 0)
                if hearts_cnt <= 0:
                    self._wait_for_hearts()
            except Exception:
                pass

            question = self.client.daily_plan.get_next_question()
            if not question:
                break

            opt_id, source_reason, is_known = self.solver.find_best_answer(question)
            if not opt_id and question.options:
                opt_id = question.options[0].id
                source_reason = "Birlamchi variant"
                is_known = False

            opt_text = next((o.option_text for o in question.options if o.id == opt_id), opt_id)
            was_new = not is_known

            time.sleep(1.5)
            try:
                res = self.client.progress.submit_answer(question.id, opt_id, source="DAILY_PLAN")
            except Exception as e:
                time.sleep(3)
                try:
                    res = self.client.progress.submit_answer(question.id, opt_id, source="DAILY_PLAN")
                except Exception as e2:
                    return {"status": "ERROR", "message": f"Savol topshirishda xatolik: {e2}", "details": results}

            if res.is_correct:
                VERIFIED_ANSWERS[question.id] = opt_id
                self.kb.record_answer(question.id, question.prompt, opt_id, opt_text)
                if was_new:
                    new_learned_count += 1
                results.append({
                    "prompt": question.prompt,
                    "is_correct": True,
                    "opt": opt_text,
                    "source": source_reason,
                    "new_learned": was_new
                })
            else:
                correct_id = res.correct_option_id
                correct_text = next((o.option_text for o in question.options if o.id == correct_id), correct_id)
                if correct_id:
                    VERIFIED_ANSWERS[question.id] = correct_id
                    self.kb.record_answer(question.id, question.prompt, correct_id, correct_text)
                    new_learned_count += 1
                results.append({
                    "prompt": question.prompt,
                    "is_correct": False,
                    "opt": opt_text,
                    "correct": correct_text,
                    "source": source_reason,
                    "new_learned": True
                })

            time.sleep(1.2)
            try:
                cur_plan = self.client.daily_plan.get_today()
                correct_count = cur_plan.correct_count
                if cur_plan.completed:
                    break
            except Exception:
                if res.is_correct:
                    correct_count += 1

            if progress_callback:
                progress_callback(correct_count, total_target, question.prompt, res.is_correct)

        time.sleep(1)
        final_plan = self.client.daily_plan.get_today()
        return {
            "status": "SUCCESS",
            "solved": final_plan.answered_count,
            "total": total_target,
            "correct_count": final_plan.correct_count,
            "completion_percent": final_plan.completion_percent,
            "bonus_xp": 100 if final_plan.completed else 0,
            "new_learned_count": new_learned_count,
            "details": results
        }
