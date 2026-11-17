from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("5ba8b1fa-2511-490b-b9cf-c713ed43d59f", "fd80c0ef-1d7b-4813-8a49-1ca9fe049f2d", "Daraxtlar simlarga aganasa (8 m gacha yaqinlashish taqiqlanadi)"),
    ("3128a57e-a5c7-40ce-825e-0641170cd9da", "ebe73cfa-802c-4cb3-ba2e-3d06b671a346", "II - V guruhlarni olish uchun xodim bilishi kerak (toliq 4 ta talab)"),
    ("8e358768-7df8-41bd-adbe-16bf693ce679", "3283b5e5-eb70-4be5-aabe-1c2cedb1c536", "Ishonch qanday hosil qilinadi (shaxsan korish, tezkor jurnaldagi yozuvlar, sxema...)"),
    ("03b97992-9ca0-4d6c-b585-543905206779", "e0a27659-09ed-40f1-a1f3-82500776d8a8", "Naryad yoki farmoyish beruvchining javobgarligi (ishni xavfsiz bajarish mumkinligini belgilaydi)")
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
