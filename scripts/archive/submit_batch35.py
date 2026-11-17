from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("f11a2795-7972-4993-ab18-d15e30bfe4a2", "cd1bdcbb-06d6-4804-a226-78caef8d6a8e", "II guruhga ega brigada azosi tayanchga qancha masofaga chiqishi mumkin (ochirilgan HL tayanchlarida yuqorisigacha, ochirilmaganda masofa 2 m qolguncha)"),
    ("250471f0-0a61-41ef-982e-62bb487d5ad1", "250f84f8-dd19-40fa-913a-476cfec8e2ab", "Muhofaza zonasidagi ishlarga QMT brigadasidan kimni ishga qoyadi (QMTning har bir brigadasidagi javobgar ijrochini ishga qoyishi shart)"),
    ("b9449c91-8d34-458d-8129-e5f37cebe12f", "15010e4e-29fb-4eef-8ca3-bcffc2ff91ba", "Kunning normal holatida havo liniyasini nechta xodim korikdan otkazishi mumkin (II guruhga mansub bir xodim tomonidan)"),
    ("89fa4446-2a40-4a1a-a362-b0fe1a5062ea", "061c57e5-d38c-40ea-b89f-79250bb3c89d", "Tayyorlangan ish joyiga kelgusi kunlarda qayta ishga qoyish (ishga qoyuvchi har ikkala nusxasida, ish bajaruvchi oz nusxasida)")
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
