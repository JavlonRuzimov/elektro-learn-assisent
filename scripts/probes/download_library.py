import os
import json
import requests
from config import Config

token = Config.get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": Config.USER_AGENT
}

os.makedirs("data/library", exist_ok=True)

with open("data/library_documents.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

print(f"Yuklab olinadigan hujjatlar soni: {len(docs)}")

for idx, doc in enumerate(docs, 1):
    doc_id = doc.get("id")
    title = doc.get("title", f"doc_{idx}").strip()
    file_url = doc.get("fileUrl")
    
    # Tozalash
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-', '.')).strip()
    ext = os.path.splitext(file_url)[1] if file_url else ".bin"
    file_name = f"{idx:02d}_{safe_title}{ext}"
    local_path = os.path.join("data/library", file_name)

    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        print(f"[{idx}/{len(docs)}] Mavjud: {file_name}")
        continue

    full_url = f"{Config.WEB_URL}{file_url}"
    print(f"[{idx}/{len(docs)}] Yuklab olinmoqda: {title} -> {full_url}")
    try:
        res = requests.get(full_url, headers=headers, timeout=60)
        if res.status_code == 200:
            with open(local_path, "wb") as f_out:
                f_out.write(res.content)
            print(f"     Saqlandi: {local_path} ({len(res.content)} bayt)")
        else:
            print(f"     Xato ({res.status_code}): {full_url}")
    except Exception as e:
        print(f"     Yuklashda xato: {e}")

print("Barcha hujjatlarni yuklash yakunlandi!")

