import requests
import re

headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get("https://lex.uz/uz/search/nat?title=711-son", headers=headers)
print("Status:", r.status_code)
links = re.findall(r'/docs/\d+', r.text)
print("Links:", list(set(links))[:5])
for l in list(set(links))[:3]:
    doc_text = requests.get(f"https://lex.uz{l}", headers=headers).text
    if "Energetika" in doc_text:
        print(f"FOUND: https://lex.uz{l}")
        # Search for yo'riqnoma
        matches = re.findall(r'([^.\n]*?yo[\'’‘`]?riqnoma[^.\n]*?tasdiqlan[^.\n]*)', doc_text, re.IGNORECASE)
        for m in matches:
            print("MATCH:", m.strip())

