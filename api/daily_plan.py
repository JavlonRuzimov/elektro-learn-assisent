from typing import Dict, Any, Optional
from api.client import BaseClient
from models.schemas import DailyPlan, Question

class DailyPlanAPI:
    def __init__(self, client: BaseClient):
        self.client = client

    def get_today(self) -> DailyPlan:
        """Bugungi kunlik reja holati (/mobile/daily-plan/today)"""
        data = self.client.get("/mobile/daily-plan/today")
        return DailyPlan.from_dict(data)

    def get_next_question(self) -> Optional[Question]:
        """Kunlik reja uchun navbatdagi savolni olish (/mobile/daily-plan/next-question)"""
        data = self.client.get("/mobile/daily-plan/next-question")
        q_data = data.get("question") if isinstance(data, dict) else None
        if q_data:
            return Question.from_dict(q_data)
        return None

    def get_calendar(self, month: Optional[str] = None) -> Any:
        """Kunlik reja taqvimi (/mobile/daily-plan/calendar)"""
        params = {"month": month} if month else {}
        return self.client.get("/mobile/daily-plan/calendar", params=params)

