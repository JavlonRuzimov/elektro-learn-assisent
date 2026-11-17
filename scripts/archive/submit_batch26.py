from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("8856c5a9-b3ab-4768-abe8-3ac9f095b68f", "0e7cf07f-2474-4628-b9f2-20869ed121f7", "Naryadning Bolinma satriga (tuzilmaviy bolinmasi sex, xizmat, tuman...)"),
    ("4d373cc4-b944-4dcc-b38d-2b691dafa51b", "46707abb-d4e7-4dfe-953b-a6cd3723f68e", "KL muhofaza zonasida yer qazish (ishga qoyish huquqiga ega bolgan navbatchi xodim)"),
    ("ef708748-bde4-4d40-b027-5865d1d167cf", "76ba548d-42be-488f-8cf7-843f63ec59ff", "Orindoshlik asosida ish joyini tayyorlash (III guruh brigada azosi bilan)"),
    ("cc87edb5-0af5-442b-aa59-7e1e09225828", "a6655dd3-6080-41af-9406-3086313aaffc", "Yoriqnoma otkazish va ishga qoyish (ishga qoyuvchi va ish bajaruvchi imzosi bilan 3-jadvalda)")
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
