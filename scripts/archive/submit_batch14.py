from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("eb5939ca-8014-4e05-b0a5-f03e9b72535e", "5c9a7b0a-b535-47f0-8cc5-64637dca18ac", "Ish bajaruvchi EX guruhi (1000V yuqori IV guruh, 1000V gacha III guruh)"),
    ("4471737d-cea3-4ee4-b839-aac83fcb7a47", "6d9c218c-63cd-44db-8094-73a6f9742ed0", "Avariya holatida chiqarilgan uskunani tarmoqqa ulash (mumkin)"),
    ("02d918eb-64e4-4c73-bf1a-75024c0fbcee", "01099594-6873-45ea-9d2a-90c46b5a9f80", "Alohida korsatmalar satriga nima yoziladi (to'liq variant)"),
    ("6269035d-2c9f-4083-a332-85b4d3332af1", "0b06b0df-f067-4854-bf99-d8dbbeceef5f", "Naryad boyicha ishga qoyish qaerda amalga oshiriladi (bevosita ish joyida)")
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
