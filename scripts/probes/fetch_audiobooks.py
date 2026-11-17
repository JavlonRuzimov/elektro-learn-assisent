import requests
import json
from config import Config

token = Config.get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": Config.USER_AGENT
}

r = requests.get(f"{Config.BASE_URL}/audio-books", headers=headers)
print("Audio-books Status:", r.status_code)
if r.status_code == 200:
    books = r.json()
    print(f"Total audio-books: {len(books)}")
    for b in books:
        print(f"- [{b.get('id')}] {b.get('title')} ({len(b.get('chapters', []))} chapters)")

