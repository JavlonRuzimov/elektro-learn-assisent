import requests
import re
from config import Config

headers = {"User-Agent": Config.USER_AGENT}
r = requests.get(Config.WEB_URL + "/learn", headers=headers)
print("Learn page status:", r.status_code)

scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)
print("Scripts found:", scripts)

for s in scripts:
    url = s if s.startswith("http") else Config.WEB_URL + s
    print(f"\nAnalyzing script: {url}")
    js_text = requests.get(url, headers=headers).text
    # Search for heart, energy, refill, buy, restore, bonus, ad, watch, xp
    keywords = ["heart", "energy", "refill", "restore", "regen", "/api/"]
    for kw in ["heart", "regen", "refill", "restore"]:
        matches = re.findall(r'[^;{}()]{0,40}' + kw + r'[^;{}()]{0,40}', js_text, re.IGNORECASE)
        if matches:
            print(f"  Keyword '{kw}' matches (sample 5):")
            for m in list(set(matches))[:5]:
                print(f"    - {m.strip()}")

    # Find all API endpoints mentioned in JS
    endpoints = re.findall(r'["\'](/api/[^"\']+)["\']', js_text)
    if endpoints:
        print(f"  Endpoints found in {s}:")
        for ep in sorted(set(endpoints)):
            print(f"    * {ep}")

