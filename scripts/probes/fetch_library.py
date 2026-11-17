import requests
import json
from config import Config

token = Config.get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": Config.USER_AGENT
}

r = requests.get(f"{Config.BASE_URL}/library-documents", headers=headers)
print("Status:", r.status_code)
if r.status_code == 200:
    docs = r.json()
    print(f"Total documents: {len(docs)}")
    with open("data/library_documents.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    for d in docs:
        print(f"- [{d.get('id')}] {d.get('title')} ({d.get('fileType')}, {d.get('fileSize')} bytes) -> {d.get('fileUrl')}")
else:
    print(r.text)

