from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("e23b5ff6-1b02-4831-9fed-ddeffcbfa6ef", "ab8279ae-c452-46fa-95f8-8345b4d528e2", "Bevosita ish joyini tayyorlash kommutatsiya apparatlari naryadning 1-jadvalga kiritiladimi (kiritilishi shart)"),
    ("6d123c51-bd2e-4ff3-9ca1-fa9882077b13", "8a13b1e9-5f3f-4949-a8e1-2369eb7f9641", "Brigada azolariga ishga qoyuvchidan tashqari yana kim yoriqnoma beradi (ish bajaruvchi ham yoriqnoma berishi shart)"),
    ("fb802b15-38a1-462b-b963-b90927def16c", "82231c90-2042-401e-a199-42bc40aa8fb0", "Naryad matniga tuzatishlar kiritish mumkinmi (man qilinadi)"),
    ("834a3e57-18ec-44aa-bd03-f357b4763e5c", "32e2f4d9-4193-4cfc-9c8a-07d93c82e099", "Ish bajaruvchiga ishga qoyuvchi vazifasi tayinlangan hollarda naryadning nusxasi kimda qoladi (naryad beruvchida qoladi)")
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
