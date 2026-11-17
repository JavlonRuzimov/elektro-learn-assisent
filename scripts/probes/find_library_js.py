import requests
import re
from config import Config

token = Config.get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": Config.USER_AGENT
}

js_url = f"{Config.WEB_URL}/assets/index-DGWZSvMV.js"
js = requests.get(js_url, headers=headers).text

# 1. Search for texts from screenshot
search_words = ["819", "34-002", "34-524", "audiokitoblar", "Kutubxona", "library", "Hujjatlar"]
for w in search_words:
    matches = list(re.finditer(re.escape(w), js, re.IGNORECASE))
    print(f"Word '{w}': {len(matches)} matches")
    for m in matches[:5]:
        start = max(0, m.start() - 150)
        end = min(len(js), m.end() + 150)
        print(f"--- Context for '{w}' ---")
        print(js[start:end])
        print("--------------------------")

