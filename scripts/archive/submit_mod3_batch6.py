from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("c9255f22-73cb-4e8a-b21b-b0970fa21ec3", "e1ad5854-0704-48e7-b908-2cce1755610d", "1 kV gacha kuchlanish ostida uskunada yonginni (kukunli ot ochirgichlar bilan ochirish mumkin)"),
    ("a6411283-dc96-4853-9eef-929055ce4ef8", "32f6870d-0230-432d-acbc-a1ffcfb69786", "Tashkilot rahbari tavsiyalarni qancha muddatda eshitadi (kamida 6 oyda bir marta eshitadi)"),
    ("5f19dc00-5e6a-4e39-8c1b-c6ba1e26a2c0", "adb8a814-2df9-43d3-96e4-985fd3a33f4f", "Yonginni ochirish tezkor varaqalari qachon qayta tasdiqlanadi (bosh muhandis yoki tegishli tsex rahbari ozgarganda)"),
    ("cd705e74-f7a8-4051-bde6-f35ecea42932", "95330d9c-696c-4d83-9f86-f7a42448b752", "0.4 kV gacha kuchlanish ostida uskunalarda xavfsiz masofa (5 metrdan kam bolmagan masofa)")
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
        print("  STOPPING ON ERROR! Heart lost!")
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
