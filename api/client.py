import time
import requests
from typing import Any, Dict, Optional
from config import Config

class APIError(Exception):
    def __init__(self, status_code: int, message: str, data: Any = None):
        super().__init__(f"API Error {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.data = data

class BaseClient:
    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None):
        self.base_url = (base_url or Config.BASE_URL).rstrip("/")
        self.token = token or Config.get_token()
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        try:
            from auth_manager import AuthManager
            if AuthManager.is_token_expired(self.token):
                self.token = AuthManager.login()
        except Exception:
            pass

        headers = {
            "User-Agent": Config.USER_AGENT,
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.session.headers.update(headers)

    def set_token(self, token: str):
        self.token = token
        self.session.headers["Authorization"] = f"Bearer {token}"

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        max_retries: int = 5,
        **kwargs
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        timeout = timeout or Config.TIMEOUT

        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    json=data,
                    timeout=timeout,
                    **kwargs
                )

                if response.status_code == 401:
                    # Token muddati tugagan bo'lsa, avtomatik login qilib yangi token olish
                    try:
                        from auth_manager import AuthManager
                        new_token = AuthManager.login()
                        self.set_token(new_token)
                        # Qayta urinish
                        response = self.session.request(
                            method=method.upper(),
                            url=url,
                            params=params,
                            json=data,
                            timeout=timeout,
                            **kwargs
                        )
                    except Exception as e:
                        raise APIError(401, f"Token eskirgan va login qilib bo'lmadi: {e}", response.text)

                try:
                    res_json = response.json()
                except Exception:
                    res_json = response.text

                if not response.ok:
                    err_msg = res_json.get("message", response.reason) if isinstance(res_json, dict) else str(res_json)
                    raise APIError(response.status_code, err_msg, res_json)

                return res_json

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    # Reset session connection pool
                    self.session = requests.Session()
                    self._setup_session()
                    continue
                raise APIError(0, f"Ulanish xatosi (Connection error): {str(e)}")
            except requests.exceptions.RequestException as e:
                raise APIError(0, f"So'rov xatosi (Request error): {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self.request("POST", endpoint, data=data, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self.request("PUT", endpoint, data=data, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self.request("PATCH", endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Any:
        return self.request("DELETE", endpoint, **kwargs)
