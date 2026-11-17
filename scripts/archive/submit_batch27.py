from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("0a217065-0750-4a5a-a480-7709114cc5ce", "73bda61c-a502-4081-b963-a824302fd71a", "Ilgakli tortqi ishlatilganda (ximoya qulflari bilan taminlanishi shart)"),
    ("6915e17b-44ba-4389-82f4-bff8c566f3dc", "4123a7c4-329b-4011-b9f6-e20d2f3ae5c9", "Ishga qoyuvchiga satriga (tezkor-tamirlash xodimlaridan... Navbatchi deb yoziladi)"),
    ("c690b97e-21f1-4a95-b127-53261ed656f6", "985ad0f6-2f3d-476f-99f8-915d9dd25098", "Ruxsat olmasdan tarmoqqa ulash huquqi qayerda yoziladi (Alohida korsatmalar satrida)"),
    ("74970d3b-7d6b-4c61-af72-3e63ad5549c6", "588df932-bc62-492c-b513-593e0a8b392a", "Ish joyini tayyorlashga va ishga qoyishga ruxsat etuvchi shaxs javobgarligi (uskunani ochirish va yerga ulash choralarining yetarliligi...)")
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
