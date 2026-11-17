from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("59b8c4ba-f5e7-42c4-a368-6a166925f039", "e66f437b-e2aa-4009-a2fa-cbc89d7a2ed7", "Naryad necha kunga uzaytirilishi mumkin (15 kalendar kun)"),
    ("3f82eaf5-cc4f-4ef3-9bca-d711e59ed630", "5a4a2532-4a08-4783-8c88-15113d5d19dd", "Ishga qoyuvchi ishga qoyishdan oldin (texnik choralarning bajarilganligiga ishonch)"),
    ("61c05773-2e24-40c1-8b51-07c744fadda9", "f1a16194-79b7-4dad-ad68-8dc84d069948", "Ish bajaruvchi ish joyidan ketganda (brigadani ish joyidan chiqarishi shart)"),
    ("2cd50295-3615-4918-83eb-39929a6ba0cd", "0b6c78a7-946d-4b1a-9feb-0af9a552ccd5", "Tayanchga chiqish (mustahkam va chidamli ekanligiga ishonch)")
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
