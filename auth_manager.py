import os
import time
import json
import base64
import requests
from urllib.parse import urlparse, parse_qs
from typing import Optional, Tuple
from config import Config

class AuthManager:
    """ElektroLearn va Energo ID orqali avtomatik login va token boshqaruvchisi"""

    BASE_URL = Config.BASE_URL
    OAUTH_LOGIN_URL = "https://cabinetid.uzbekistonmet.uz/api/oauth/login"
    OAUTH_APPROVE_URL = "https://cabinetid.uzbekistonmet.uz/api/oauth/approve"

    @classmethod
    def get_credentials(cls) -> Tuple[str, str]:
        """Login va parolni .env yoki Config dan olish"""
        login = os.environ.get("ELEKTROLEARN_LOGIN", "").strip()
        password = os.environ.get("ELEKTROLEARN_PASSWORD", "").strip()

        if not login or not password:
            if os.path.exists(".env"):
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ELEKTROLEARN_LOGIN="):
                            login = line.split("=", 1)[1].strip().strip('"').strip("'")
                        elif line.startswith("ELEKTROLEARN_PASSWORD="):
                            password = line.split("=", 1)[1].strip().strip('"').strip("'")

        # Standart foydalanuvchi ma'lumotlari
        login = login or "s.ruzimov2774"
        password = password or "11111111"
        return login, password

    @classmethod
    def is_token_expired(cls, token: Optional[str] = None, buffer_seconds: int = 120) -> bool:
        """Token muddati tugaganligini (yoki tugashiga oz qolganligini) tekshirish"""
        token = token or Config.get_token()
        if not token:
            return True
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return True
            payload_b64 = parts[1]
            # Base64 padding
            payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
            payload_json = base64.urlsafe_b64decode(payload_b64.encode("utf-8")).decode("utf-8")
            data = json.loads(payload_json)
            exp = data.get("exp", 0)
            return time.time() >= (exp - buffer_seconds)
        except Exception:
            return True

    @classmethod
    def update_env_file(cls, new_token: str):
        """Yangi tokenni .env faylida saqlash"""
        env_path = ".env"
        lines = []
        token_found = False

        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("ELEKTROLEARN_TOKEN="):
                        lines.append(f"ELEKTROLEARN_TOKEN={new_token}\n")
                        token_found = True
                    else:
                        lines.append(line)

        if not token_found:
            lines.insert(0, f"ELEKTROLEARN_TOKEN={new_token}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        os.environ["ELEKTROLEARN_TOKEN"] = new_token
        Config.DEFAULT_TOKEN = new_token

    @classmethod
    def login(cls, username: Optional[str] = None, password: Optional[str] = None) -> str:
        """Energo ID OAuth orqali to'liq avtomatik kirish va yangi token olish"""
        u, p = cls.get_credentials()
        username = username or u
        password = password or p

        # 1. Authorize URL olish
        res = requests.get(f"{cls.BASE_URL}/auth/energo-id/authorize-url?client=web", timeout=15)
        if res.status_code != 200:
            raise RuntimeError(f"Authorize URL olishda xatolik: {res.status_code} {res.text}")

        auth_info = res.json()
        auth_url = auth_info["authorizeUrl"]
        parsed = urlparse(auth_url)
        qs = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        # 2. Login so'rovi
        login_payload = {
            "client_id": qs.get("client_id"),
            "redirect_uri": qs.get("redirect_uri"),
            "state": qs.get("state"),
            "scope": qs.get("scope"),
            "login": username,
            "password": password,
            "client_ip": qs.get("client_ip"),
            "ip": qs.get("ip")
        }
        if "code_challenge" in qs:
            login_payload["code_challenge"] = qs["code_challenge"]
            login_payload["code_challenge_method"] = qs.get("code_challenge_method", "S256")

        r_login = requests.post(cls.OAUTH_LOGIN_URL, json=login_payload, timeout=15)
        if r_login.status_code not in [200, 201]:
            raise RuntimeError(f"Energo ID ga kirishda xatolik ({r_login.status_code}): {r_login.text}")

        login_data = r_login.json()
        consent_token = login_data.get("consentToken")
        if not consent_token:
            raise RuntimeError(f"ConsentToken olinmadi: {login_data}")

        # 3. Approve (ruxsat berish)
        approve_payload = {"consent_token": consent_token}
        r_app = requests.post(cls.OAUTH_APPROVE_URL, json=approve_payload, timeout=15)
        if r_app.status_code not in [200, 201]:
            raise RuntimeError(f"Approve xatoligi ({r_app.status_code}): {r_app.text}")

        app_data = r_app.json()
        redirect_url = app_data.get("redirectUrl")
        if not redirect_url:
            raise RuntimeError(f"Redirect URL topilmadi: {app_data}")

        # 4. Code va State ni ajratib olish
        parsed_redirect = urlparse(redirect_url)
        redirect_qs = {k: v[0] for k, v in parse_qs(parsed_redirect.query).items()}
        code = redirect_qs.get("code")
        state = redirect_qs.get("state")
        if not code:
            raise RuntimeError(f"OAuth code olinmadi: {redirect_url}")

        # 5. ElektroLearn da token ga almashtirish (exchange)
        exchange_payload = {
            "code": code,
            "state": state,
            "client": "web"
        }
        r_ex = requests.post(f"{cls.BASE_URL}/auth/energo-id/exchange", json=exchange_payload, timeout=15)
        if r_ex.status_code not in [200, 201]:
            raise RuntimeError(f"Token exchange xatoligi ({r_ex.status_code}): {r_ex.text}")

        token_data = r_ex.json()
        new_token = token_data.get("data", {}).get("accessToken")
        if not new_token:
            raise RuntimeError(f"Yangi accessToken topilmadi: {token_data}")

        # .env va xotirani yangilash
        cls.update_env_file(new_token)
        return new_token

    @classmethod
    def get_valid_token(cls) -> str:
        """Token muddati tugagan bo'lsa avtomatik yangilab, toza tokenni qaytarish"""
        token = Config.get_token()
        if cls.is_token_expired(token):
            return cls.login()
        return token

if __name__ == "__main__":
    print("Mavjud token eskirganmi:", AuthManager.is_token_expired())
    token = AuthManager.get_valid_token()
    print("Hozirgi amaldagi token:", token[:40] + "...")
