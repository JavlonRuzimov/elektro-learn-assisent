from typing import Any, Dict, Optional
from api.client import BaseClient

class ExamAPI:
    def __init__(self, client: BaseClient):
        self.client = client

    def get_next(self) -> Any:
        """Navbatdagi imtihon (/exams/live/me/next)"""
        return self.client.get("/exams/live/me/next")

    def get_history(self) -> Any:
        """Imtihonlar tarixi (/exams/live/me/history)"""
        return self.client.get("/exams/live/me/history")

    def validate_qr(self, qr_token: str) -> Any:
        """QR kodni tekshirish (/exams/live/validate-qr)"""
        return self.client.post("/exams/live/validate-qr", data={"qrToken": qr_token})

    def get_session_state(self, session_id: str) -> Any:
        """Imtihon sessiyasi holati (/exams/live/session/{session_id}/state)"""
        return self.client.get(f"/exams/live/session/{session_id}/state")

    def verify_code(self, session_id: str, code: str) -> Any:
        """Imtihon kodini tasdiqlash (/exams/live/session/{session_id}/verify-code)"""
        return self.client.post(f"/exams/live/session/{session_id}/verify-code", data={"code": code})

    def start_section(self, session_id: str, section: str) -> Any:
        """Bo'limni boshlash (/exams/live/session/{session_id}/start-section)"""
        return self.client.post(f"/exams/live/session/{session_id}/start-section", data={"section": section})

    def answer(self, session_id: str, payload: Dict[str, Any]) -> Any:
        """Imtihon savoliga javob berish (/exams/live/session/{session_id}/answer)"""
        return self.client.post(f"/exams/live/session/{session_id}/answer", data=payload)

    def submit_section(self, session_id: str, section: str) -> Any:
        """Bo'limni topshirish (/exams/live/session/{session_id}/submit-section)"""
        return self.client.post(f"/exams/live/session/{session_id}/submit-section", data={"section": section})

    def report_tab_switch(self, session_id: str) -> Any:
        """Vkladka almashish faolligi (/exams/live/session/{session_id}/tab-switch)"""
        return self.client.post(f"/exams/live/session/{session_id}/tab-switch", data={})

