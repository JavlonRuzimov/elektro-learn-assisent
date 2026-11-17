from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("4e3647d2-8259-4665-adce-c2c361783367", "57c4bba8-29d7-4030-9c20-c5328221bf2c", "Ish rahbarining uzluksiz nazorati (Alohida korsatmalar satrida)"),
    ("6fa09ff4-7e80-430a-b52f-ae0b3abd2e43", "b84339fb-44c9-4a7a-afd1-719ec819f5c9", "Himoya kamarining arqoni (traversga yoki mo'ljallangan moslamaga)"),
    ("e8f81699-6101-42a6-bb5e-65432090ca17", "e5673685-5bf2-495c-8d59-41b871fc2556", "HLda Kuchlanish ostida quyidagilar qoldi (Alohida korsatmalar qatorida korsatilgan tok otkazuvchi qismlar)"),
    ("33f30c0e-e144-45b2-ab94-38f6bdb6a662", "e49ea1ad-07ac-4ae0-91c8-4cf35ae48a82", "Ish boshlansin va Ish tugatilsin (sanasi hamda vaqti korsatiladi)")
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
