import requests
import json
import re
from config import Config

token = Config.get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": Config.USER_AGENT
}

# 1. Frontend JS larni tekshiramiz library so'zi bo'yicha
main_html = requests.get(f"{Config.WEB_URL}/learn/library", headers=headers).text
js_files = re.findall(r'src=["\'](/assets/[^"\']+\.js)["\']', main_html)
print(f"JS files: {js_files}")

for js_path in js_files:
    js_content = requests.get(f"{Config.WEB_URL}{js_path}", headers=headers).text
    for m in re.finditer(r'["\'](/[^"\']*(?:library|document|book|file)[^"\']*)["\']', js_content, re.IGNORECASE):
        print(f"Found endpoint candidate in JS: {m.group(1)}")

# 2. To'g'ridan-to'g'ri API endpointlarni tekshirib ko'ramiz
candidates = [
    "/library",
    "/library/documents",
    "/library/books",
    "/library/files",
    "/documents",
    "/books",
    "/progress/library",
]

for c in candidates:
    try:
        r = requests.get(f"{Config.BASE_URL}{c}", headers=headers)
        print(f"GET {c} -> {r.status_code}")
        if r.status_code == 200:
            print(f"Data: {json.dumps(r.json(), ensure_ascii=False)[:300]}")
    except Exception as e:
        print(f"Error {c}: {e}")
