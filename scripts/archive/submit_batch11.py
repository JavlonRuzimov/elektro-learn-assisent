from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("20db6a11-b300-474f-92a2-1051125b42f3", "3b011d94-02c8-4658-9c77-66c7209cc855", "Tarmoqqa ulashdan oldin (vaqtinchalik tosiqlarni olishi, doimiy tosiqni tiklashi)"),
    ("8c612a3f-96d9-4bb0-ae4e-03ded14d8080", "6687d28c-5da3-415a-a955-55d7675fc596", "Brigada azosi nimaga javob beradi (a,b va g javoblar togri)"),
    ("092ca6d0-06cf-441d-84bb-c7d42f51da16", "36550f27-e6ac-4eed-95fd-180b23ccfd5d", "Shinalarni ajratishni (III guruhga mansub tamirlash xodimi)"),
    ("54541821-ee96-4fef-be8b-6d332c693897", "225b99ac-cae7-4e87-96b1-8a30164ed223", "Ish bajaruvchi nimaga javob beradi (ish joyi muvofiqligi, yoriqnoma, himoya vositalari...)")
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
