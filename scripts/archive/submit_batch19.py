from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("04e585e3-a6ad-4bef-a72f-c5761cdeb351", "6f03dda1-3d7b-4428-8032-d0aac5ff14d6", "Kim ish joyini tayyorlovchi bolishi mumkin (navbatchi yoki tezkor-tamirlash xodimlari)"),
    ("c8e9cf77-9ea2-42f0-8a70-02e2a9498e8e", "4122b283-112d-4aae-8f7c-d6ea4ece6567", "Daraxt chopishdan oldin (agnayotgan daraxtlarning simlarga yaqinlashishi xavfli ekanligini ogohlantirish)"),
    ("baebec78-b5d3-4737-bdc0-cd299bd71190", "07971619-3f73-4a14-bc3b-11430a941120", "Kelgusi kunlarda ishga qoyish (ishga qoyuvchi yoki uning ruxsati bilan ish rahbari)"),
    ("8ad4f79f-f305-4975-93a9-cd4452d81b3e", "10715da7-3170-469d-8b41-ee227369cecd", "Kuzatuvchi nimaga javob beradi (joy muvofiqligi, erga ulagichlar, tokdan shikastlanish)")
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
