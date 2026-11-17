from typing import Any, Dict, List
from api.client import BaseClient

class LeaderboardAPI:
    def __init__(self, client: BaseClient):
        self.client = client

    def get_global(self, limit: int = 50) -> Any:
        """Umumiy reyting (/leaderboard/global)"""
        return self.client.get("/leaderboard/global", params={"limit": limit})

    def get_organization(self, limit: int = 50) -> Any:
        """Tashkilot bo'yicha reyting (/leaderboard/organization)"""
        return self.client.get("/leaderboard/organization", params={"limit": limit})

