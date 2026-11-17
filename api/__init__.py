from .client import BaseClient, APIError
from .auth import AuthAPI
from .progress import ProgressAPI
from .daily_plan import DailyPlanAPI
from .leaderboard import LeaderboardAPI
from .exam import ExamAPI

class ElektroLearnClient:
    def __init__(self, token: str = None, base_url: str = None):
        self.base_client = BaseClient(token=token, base_url=base_url)
        self.auth = AuthAPI(self.base_client)
        self.progress = ProgressAPI(self.base_client)
        self.daily_plan = DailyPlanAPI(self.base_client)
        self.leaderboard = LeaderboardAPI(self.base_client)
        self.exam = ExamAPI(self.base_client)

    def set_token(self, token: str):
        self.base_client.set_token(token)

__all__ = [
    "ElektroLearnClient",
    "BaseClient",
    "APIError",
    "AuthAPI",
    "ProgressAPI",
    "DailyPlanAPI",
    "LeaderboardAPI",
    "ExamAPI",
]

