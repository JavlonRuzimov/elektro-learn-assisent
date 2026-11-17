from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("d3b0db96-0d48-495d-9490-525fca246687", "bd1aa5ca-8bf0-4e9f-b15d-ae47d4246e3b", "FVV kelgunga qadar yonginni ochirishga kim rahbarlik qiladi (obektning smena boshligi tashkilot rahbari yonginni ochirishga rahbarlik qiladi)"),
    ("79581d4c-50b4-4466-af49-8d6c3c2f4f0a", "82f61ff1-fa7c-449c-9b80-77f1810dcd2d", "Kongilli yonginni ochirish drujinasi nima uchun tashkil etiladi (tashkilotlarda yonginga qarshi rejimni yaxshilash, birlamchi vositalar...)"),
    ("871e488f-8639-4c6a-b95f-dfc87b337dcd", "748427f7-5ecf-4c84-8bad-357da6023b9c", "Yonginni ochirish tezkor varaqalarini kim tasdiqlaydi (tezkor varaqalar bosh muhandis tomonidan tasdiqlanadi)"),
    ("70c6683c-8e5f-4942-a725-6abcbeba232d", "f5edabff-3e64-41ec-8552-fe7975b1ad11", "FVV birinchi bolinmasi kelgandan keyin kim rahbar (ushbu bolinmaning navbatchi smena boshligi yonginni ochirish rahbari hisoblanadi)")
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
