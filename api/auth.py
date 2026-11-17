from typing import Dict, Any, Optional
from api.client import BaseClient
from models.schemas import UserProfile

class AuthAPI:
    def __init__(self, client: BaseClient):
        self.client = client

    def get_me(self) -> UserProfile:
        """Joriy foydalanuvchi ma'lumotlarini olish (/auth/me)"""
        data = self.client.get("/auth/me")
        return UserProfile.from_dict(data)

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Yangi access token olish (/auth/refresh)"""
        return self.client.post("/auth/refresh", data={"refreshToken": refresh_token})

    def login(self, login: str, password: str) -> Dict[str, Any]:
        """Login qilish (/auth/login)"""
        return self.client.post("/auth/login", data={"login": login, "email": login, "password": password})

    def send_heartbeat(self) -> None:
        """Foydalanuvchi faolligini bildirish (/user-activity/heartbeat)"""
        self.client.post("/user-activity/heartbeat")

    def logout(self, refresh_token: str) -> None:
        """Tizimdan chiqish (/auth/logout)"""
        self.client.post("/auth/logout", data={"refreshToken": refresh_token})

