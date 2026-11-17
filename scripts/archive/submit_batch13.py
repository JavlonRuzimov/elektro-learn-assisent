from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("bc671edb-4234-4ca7-af19-7d7bfa6d1c37", "fd200b45-b74f-45f1-9592-47eb6f5b5d4a", "Daraxtlarni ag'natish (man etiladi)"),
    ("7ead8108-0030-4eae-9e68-9d0b36dd3f6d", "f069d0a3-8f74-44cd-948f-ab65a900d09e", "Naryadning 1-jadvaliga nimalar yozilmaydi (almashlab ulashlar jadvalga yozilmaydi)"),
    ("812ed18c-ff83-481c-b7b0-aa2cb4b03b55", "510af3c1-22ec-4968-a011-5275f551fd62", "Ruxsat olmasdan tarmoqqa ulash (tezkor-tamirlash xodimlaridan bolgan ishga qoyuvchiga)"),
    ("f9caef69-ae6c-480c-a73d-473f03275f48", "0a91e86e-5bf2-4ea7-a2b7-f9eb84fc70c8", "Nechta naryad yoki farmoyish (navbatma-navbat birdaniga bir necha)")
]

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

for qid, opt_id, desc in submits:
    print(f"\nSubmitting: {desc}")
    res = client.post("/progress/answer", data={
        "questionId": qid,
        "selectedOptionId": opt_id,
        "source": "LESSON"
    })
    is_cor = res.get("isCorrect")
    print(f"  Result: {is_cor} | Hearts: {res.get('hearts', {}).get('heartsCount')}")
    if not is_cor:
        print("  STOPPING ON ERROR!")
        break
    kb.setdefault('questions', {})[qid] = {
        'correctOptionId': opt_id,
        'verified': True,
        'note': desc
    }
    time.sleep(1.2)

with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(kb, f, indent=2, ensure_ascii=False)

print("\nKnowledge base saved. Total questions in KB:", len(kb.get('questions', {})))
