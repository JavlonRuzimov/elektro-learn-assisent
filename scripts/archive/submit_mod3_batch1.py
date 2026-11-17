from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("ec5b077b-0f36-4abc-aa37-b8470f4b1b77", "48d748de-bf24-4d30-b427-8cc8680016e4", "Tezkor-chiqish brigadasi avtomobillarida ot ochirgich (har birining ogirligi 5 kg dan kam bolmagan kamida tortta karbonat kislotali va kukunli)"),
    ("dd219aac-123d-4bbb-acb7-b67cf7c6f5fa", "3c8aacf0-7ab9-4977-9705-679b17e73a28", "Toliq ogirligi 15 kg va undan ortiq bolgan ot ochirgichlar (poldan 1,0 m dan kop bolmagan balandlikda)"),
    ("ef005130-d960-4afd-9ee8-9d9479360dc1", "3debd0ce-59eb-4ea9-a20b-5bd552633d17", "Kuchlanish ostida bolgan uskunadagi yonginni qaysi turdagi ot ochirgichlar bilan (karbonat kislotali, kukunli, xladonli)"),
    ("f02984fe-27ca-4c33-bec5-511d050d95e1", "93a31af6-6a23-4d47-9bcb-bfdf2c1d13ba", "Tsexlar laboratoriyalar bolimlar yongin xavfsizligi holati uchun kim javobgar (rahbarlari, bolmagan vaqtda esa vazifasini bajaruvchi shaxslar)")
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
