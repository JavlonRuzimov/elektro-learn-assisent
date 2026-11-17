from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("1b702a4b-8d4d-44fb-a444-579c2bcdc26a", "1bec52ab-b711-421a-970d-fac0261ede11", "Kabellarni teshish zarurati bolsa kim bajaradi (naryad boyicha ekspluatatsiya qiluvchi korxona xodimlaridan tayinlangan ishga qoyuvchi)"),
    ("69ab8b32-c2bd-47ec-97c2-34704ac3002c", "a7120fa1-fc36-4f70-9e33-3715143410f2", "Ishga qoyish qaysi vaqtda amalga oshiriladi (ish joyining tayyorligi tekshirilgandan song amalga oshiriladi)"),
    ("9cdac0ce-245f-40c1-9606-ff44e1defb4c", "cb16ac44-82b4-4830-9cb3-3f087692c322", "Zarb bilan ishlaydigan mashina va mexanizmlar kabel trassalarida (5 metrdan kam masofada)"),
    ("88093ca6-651a-4a56-87de-1600797560a8", "5b3b37e1-ef88-40bb-83df-4deaa801acbf", "Naryad necha kun saqlanadi (30 sutka davomida saqlanishi shart)")
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
