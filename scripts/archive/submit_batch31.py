from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("81a20611-b042-44c2-b079-68a29784e499", "a7409e1d-f6b9-481d-a014-2ade0a3a3060", "Ishga qoyuvchi nechanchi guruh bolishi kerak (1000 Vdan yuqori IV guruh, 1000 Vgacha III guruh)"),
    ("2ad3bafe-7a07-4aa9-aa07-a6fb268d777f", "b59c0dde-3c8f-4624-b458-cc912c7cfc89", "Naryadni raqamlash tizimini kim belgilaydi (korxona rahbariyati tomonidan belgilanadi)"),
    ("c4e84f28-fcbc-44c1-b448-a5d9a7cd0487", "f2a0cb58-6ab0-4b11-a423-4bb14c0660af", "Avtomobil haydovchisi mexanizm mashinist kranchi 4-jadval (turi ham korsatilishi kerak)"),
    ("4bda78e1-c9ee-4738-bd8e-950380a41958", "f78d7be6-eb3d-41f3-8edc-4976a43dfbea", "Otish qiyin ob-havo noqulay qorongida HLni korikdan otkazish (II guruhga mansub ikki xodim tomonidan)")
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
