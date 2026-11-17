from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("19e10db5-d116-4dd0-bfcc-7ff07e7fcfb9", "38c20289-6f28-4eef-b680-9bec50a0259c", "Mahalliy navbatchisi bolmagan va uyda navbatchilik qiladigan elektr qurilmalarda jurnal yuritiladimi (yuritilmaydi)"),
    ("7531b2f7-9a99-426a-8138-572c0680e23f", "3a69160b-c7e8-4cf3-9100-416bad045e67", "Podstantsiyalar va KLda 1-jadvalga nima yoziladi (1-ustunda kommutatsiya apparatlari... 2-ustunda apparatlar ulanmalar uskunalarning nomlari va erga ulagichlar...)"),
    ("fef585a0-714f-4786-b4c8-b6a165671032", "450748f7-1e2b-4c2d-8c41-1d7d98e51dfe", "Brigadani nechta naryad bilan ishga qoyshga ruxsat beriladi (faqat bitta naryad bilan)"),
    ("4da7e975-a537-496f-9719-1c93e3457d3b", "b6aea940-0d99-424e-b0d3-8ec75e7a9de8", "Bir tomonlama tortishga moljallanmagan tayanchlar (agdarilib tushmasligi uchun oldindan mahkamlangan bolishi shart)")
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
