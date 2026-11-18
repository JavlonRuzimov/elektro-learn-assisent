import os
import json
import time
from typing import Optional, Dict, Any

class ExamMonitor:
    """O'zbekiston MET rasmiy malaka/attestatsiya imtihonlarini monitoring qiluvchi modul"""

    def __init__(self, client, state_file: str = "data/last_exam.json"):
        self.client = client
        self.state_file = state_file

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_state(self, state: Dict[str, Any]):
        os.makedirs(os.path.dirname(self.state_file) or ".", exist_ok=True)
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def check_for_new_exam(self) -> Optional[Dict[str, Any]]:
        """
        Yangi e'lon qilingan imtihonni aniqlash.
        Agar yangi imtihon chiqsa va u oldin bildirilmagan bo'lsa,
        imtihon ma'lumotlarini qaytaradi.
        """
        try:
            res = self.client.exam.get_next()
            if not isinstance(res, dict):
                return None

            next_exam = res.get("next")
            if not next_exam:
                return None

            exam_id = str(
                next_exam.get("id") or
                next_exam.get("examId") or
                next_exam.get("sessionId") or
                next_exam.get("title") or
                "unknown_exam"
            )

            state = self._load_state()
            last_id = state.get("last_notified_exam_id")

            if exam_id != last_id:
                state["last_notified_exam_id"] = exam_id
                state["last_notified_at"] = time.time()
                state["exam_details"] = next_exam
                self._save_state(state)
                return next_exam

            return None
        except Exception as e:
            print(f"[ExamMonitor] Imtihon tekshirishda xatolik: {e}")
            return None

    def get_current_status(self) -> Dict[str, Any]:
        """Qo'lda tekshirish uchun hozirgi imtihon holati"""
        try:
            res = self.client.exam.get_next()
            if isinstance(res, dict) and res.get("next"):
                return {"has_exam": True, "exam": res.get("next")}
            return {"has_exam": False, "exam": None}
        except Exception as e:
            return {"has_exam": False, "error": str(e)}

    @staticmethod
    def format_exam_alert(exam: Dict[str, Any]) -> str:
        """Imtihon haqida chiroyli Telegram xabarnomasi"""
        title = exam.get("title") or exam.get("name") or "Rasmiy Malaka Imtihoni"
        scheduled_at = exam.get("scheduledAt") or exam.get("startTime") or exam.get("date") or "Tez orada"
        duration = exam.get("durationMinutes") or exam.get("duration") or "Standart"
        total_questions = exam.get("totalQuestions") or exam.get("questionsCount") or "Belgilanmagan"
        status = exam.get("status") or "E'LON QILINDI"

        text = (
            f"🚨 <b>DIQQAT: YANGI MALAKA IMTIHONI E'LON QILINDI!</b> 📝\n\n"
            f"🏢 <b>Tashkilot:</b> «O‘zbekiston MET» AJ\n"
            f"📋 <b>Imtihon nomi:</b> <b>{title}</b>\n"
            f"📅 <b>Belgilangan vaqt:</b> {scheduled_at}\n"
            f"⏳ <b>Ajratilgan vaqt:</b> {duration} daqiqa\n"
            f"❓ <b>Savollar soni:</b> {total_questions} ta\n"
            f"📌 <b>Holati:</b> {status}\n\n"
            f"⚠️ <i>Tayyorgarlik ko'rish uchun botdagi bilimlar bazasidan yoki modullardan foydalanishingiz mumkin!</i>"
        )
        return text
