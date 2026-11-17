from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("3221752a-21ad-4c48-bc67-4bb520f7c944", "51a6ea7a-234a-4e47-92d0-0da445f13ccb", "Qurigan otlarni tashkilot hududidan qancha masofada saqlash taqiqlanadi (100 metrdan kam masofada saqlash taqiqlanadi)"),
    ("24e7efa6-1714-4013-8fbb-18db442df36e", "97b2d27e-ce72-447b-a743-b519c9d48e28", "Yopiq taqsimlash qurilmalarida payvandlash (faqat yonginga qarshi zarur tadbirlar bajarilgandan song olib chiqish imkoni bolmagan uskunalarda)"),
    ("005cd2de-1b1e-48a2-a307-0a299c730d59", "b5b3ceb8-a3a7-43dd-9ecd-0e7471e8f7fd", "FVV qutqaruv bolinmalari kelgunga qadar yonginni ochirish rahbari nima tashkil etadi (barcha bandlar toliq)"),
    ("56fd6eef-8e8b-4ea9-bd34-4a0eba26b3bd", "42cc7f1a-53ca-4d94-8a7e-3cc1cb0c3e66", "Sigimi 0.5 m3 li qumli quti va belkuraklar qaerlarda ornatiladi (turbogeneratorlar moy tizimi nolli belgisi, transformatorlar va ochiqda ornatilgan moyli reaktorlar...)")
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
