from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("ad4454e9-fabd-4608-a100-c959894ad591", "309b4a9c-101c-43c2-b5f0-7309cbcabbf8", "Yongin xavfsizligi har bir xodimning majburiyatlari (qoidalarni aniq bilishi va amal qilishi, yonginga qarshi tadbirlarni bajarishi...)"),
    ("4295fac2-e9fd-4eaf-b273-b98ba080d9d0", "126cc395-04d2-46fd-8cca-d552d7252929", "10 kV gacha kuchlanish ostidagi uskunada yonginni (karbonat kislotali ot ochirgichlar bilan ochirish mumkin)"),
    ("d26c7649-dffb-43ba-8768-ed40a3692965", "d0790504-13b2-4e39-8800-ca03ef283a2b", "Transformatorlar ostidagi shagal qancha muddatda yuvilishi kerak (kuchli kirlanganda, odatda bahor va kuzda)"),
    ("e796d71f-f3f6-466b-9dbd-33b069bbec46", "e9e55f61-ea28-41b8-b72c-060c8bc1b56f", "0.4 kV gacha kuchlanish ostidagi uskunada yonginni (xladonli ot ochirgich bilan ochirish mumkin)")
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
