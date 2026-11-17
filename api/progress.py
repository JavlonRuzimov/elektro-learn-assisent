from typing import Dict, Any, List, Optional
from api.client import BaseClient
from models.schemas import (
    ProgressOverview,
    LevelDetail,
    Theory,
    Question,
    AnswerResult
)

class ProgressAPI:
    def __init__(self, client: BaseClient):
        self.client = client

    def get_progress(self) -> ProgressOverview:
        """Foydalanuvchining umumiy progressi va barcha darajalar (/progress/me)"""
        data = self.client.get("/progress/me")
        return ProgressOverview.from_dict(data)

    def get_level_detail(self, level_id: str) -> LevelDetail:
        """Berilgan darajaning batafsil nazariya (theories) ro'yxati (/progress/level/{level_id})"""
        data = self.client.get(f"/progress/level/{level_id}")
        return LevelDetail.from_dict(data)

    def get_theory(self, theory_id: str) -> Theory:
        """Bitta nazariya ma'lumotlarini olish (/theories/{theory_id})"""
        data = self.client.get(f"/theories/{theory_id}")
        return Theory.from_dict(data)

    def get_theory_questions(self, theory_id: str, mode: str = "continue") -> Dict[str, Any]:
        """
        Nazariya bo'yicha savollarni olish (/theories/{theory_id}/questions).
        mode: 'continue' yoki 'retry'
        """
        data = self.client.get(f"/theories/{theory_id}/questions", params={"mode": mode})
        # Parse questions if present
        raw_questions = data.get("questions", [])
        questions = [Question.from_dict(q) for q in raw_questions]
        return {
            "mode": data.get("mode", mode),
            "total_questions": data.get("totalQuestions", len(questions)),
            "answered_count": data.get("answeredCount", 0),
            "remaining_count": data.get("remainingCount", 0),
            "is_module_complete": data.get("isModuleComplete", False),
            "questions": questions,
            "raw": data
        }

    def submit_answer(
        self,
        question_id: str,
        selected_option_id: str,
        source: str = "LESSON"
    ) -> AnswerResult:
        """
        Oddiy tanlovli (SINGLE_CHOICE) savolga javob yuborish (/progress/answer).
        source: 'LESSON' yoki 'DAILY_PLAN'
        """
        payload = {
            "questionId": question_id,
            "selectedOptionId": selected_option_id,
            "source": source
        }
        res = self.client.post("/progress/answer", data=payload)
        return AnswerResult.from_dict(res)

    def submit_matching(
        self,
        question_id: str,
        pairs: List[Dict[str, str]],
        source: str = "LESSON"
    ) -> AnswerResult:
        """
        Moslashtirish (MATCHING) savoliga javoblarni yuborish (/progress/matching).
        pairs: [{'leftOptionId': '...', 'rightOptionId': '...'}, ...]
        """
        payload = {
            "questionId": question_id,
            "pairs": pairs,
            "source": source
        }
        res = self.client.post("/progress/matching", data=payload)
        return AnswerResult.from_dict(res)

    def get_certificates(self) -> Any:
        """Mening sertifikatlarim (/certificates/me)"""
        return self.client.get("/certificates/me")

