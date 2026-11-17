from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("946f1c52-1138-48c8-b745-d73f51928924", "0d83c57b-2acc-4824-b709-121063d292f1", "1000V farmoyishda ish bajaruvchining ketishi (ruxsat etiladi)"),
    ("fb6bddeb-c4a1-4f16-b02c-c8d0af789643", "6a832149-32ff-4a2a-a1f3-bd2d7584e554", "Tayanchlarni mustahkamlash zaruriyati (ish rahbari yoki ish bajaruvchi)"),
    ("28719133-ac94-48ca-8585-582479d8b73f", "bb65878a-a8e3-4359-9b9f-8007faeb17a7", "1000V yuqori brigadani boshqa ish joyiga otkazish (ishga qoyuvchi amalga oshiradi)"),
    ("a7fd1233-3f23-430c-8766-72c5aa06cd55", "e7072d08-a127-43c1-8855-db9dcf4697c8", "Jurnalni saqlash muddati (oxirgi yozuvdan song 6 oy)")
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
