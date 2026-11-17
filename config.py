# ElektroLearn Configuration

import os
from dataclasses import dataclass

@dataclass
class Config:
    BASE_URL: str = "https://elektrolearn-mobile.uzbekistonmet.uz/api"
    WEB_URL: str = "https://elektrolearn-mobile.uzbekistonmet.uz"
    DEFAULT_TOKEN: str = ""
    USER_AGENT: str = "Mozilla/5.0 (Linux; Android 14; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    TIMEOUT: int = 30

    @classmethod
    def get_token(cls) -> str:
        # Check environment variable first, then fallback to configured default
        token = os.environ.get("ELEKTROLEARN_TOKEN", "").strip()
        if not token:
            # Check local .env file if exists
            if os.path.exists(".env"):
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("ELEKTROLEARN_TOKEN="):
                            token = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
        return token if token else cls.DEFAULT_TOKEN

