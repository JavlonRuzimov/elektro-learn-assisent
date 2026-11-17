import requests
import re
from config import Config

url = "https://elektrolearn-mobile.uzbekistonmet.uz/assets/index-DGWZSvMV.js"
js = requests.get(url, headers={"User-Agent": Config.USER_AGENT}).text

# Find all /api or path patterns
endpoints = re.findall(r'["\'](/(?:api/|auth/|progress/|theories/|daily-plan/|leaderboard/|exam/|certificates/|users/)[^"\']*)["\']', js)
print("Endpoints found in frontend JS:")
for ep in sorted(set(endpoints)):
    print(f"  {ep}")

# Search for any references to hearts or NO_HEARTS_LEFT
print("\nContext around NO_HEARTS_LEFT:")
for m in re.finditer(r'NO_HEARTS_LEFT', js):
    start = max(0, m.start() - 200)
    end = min(len(js), m.end() + 200)
    print(js[start:end])
    print("-" * 50)

