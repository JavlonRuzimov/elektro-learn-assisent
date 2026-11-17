import requests
import re
from config import Config

token = Config.get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": Config.USER_AGENT
}

# 1. Frontend bundle ni o'rganamiz
js_url = f"{Config.WEB_URL}/assets/index-DGWZSvMV.js"
js = requests.get(js_url, headers=headers).text

print("--- Frontendda uchragan /theories va /questions API lari ---")
for m in re.finditer(r'["\'](/[^"\']*(?:theories|questions|exams|quizzes|levels)[^"\']*)["\']', js):
    print(f"Endpoint: {m.group(1)}")

# Context around questions API call
print("\n--- Context around /questions API call ---")
for m in re.finditer(r'/theories/[^/]+/questions', js):
    idx = m.start()
    print(js[max(0, idx-150):min(len(js), idx+250)])
    print("="*60)
