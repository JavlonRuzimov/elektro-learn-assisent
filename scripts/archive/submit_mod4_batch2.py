from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("2f048341-47ad-450f-8ce3-aaf24fc695d0", "e285b4b5-5f91-4d4b-ba7f-02129e0e4b2c", "Kirish yoriqnomasi qaerda rasmiylashtiriladi (kirish yoriqnomasini qayd qilish jurnalida)"),
    ("d832856b-104b-4d0e-8946-c5541bd7ca87", "cf2a75b8-4c1d-48c4-a5fc-c6853d10f09d", "Qaysi toifadagi xodimlar stajerlikdan otishlari kerak (tezkor va tezkor-tamirlash xodimlari stajyorlikdan otishi kerak)"),
    ("35d6893e-d9e9-48d0-b6e0-1a34a34315a4", "7b4d3bcf-7a12-4042-befe-0b65ab7f3ed8", "Xodimlarning malakasini oshirishni tashkil etish javobgarligi (xodimlar bolimi boshligiga)"),
    ("d264bfb2-b683-4e4e-a0e7-e73e7c8e2501", "4e6a5937-17c9-4549-b7a7-083a69f0d81c", "Xodimlar qaysi qoidalardan bilim sinovidan otishlari kerak (texnik ekspluatatsiya qilish, xavfsizlik texnikasi, yongin xavfsizligi qoidalari hamda mehnatni muhofaza qilishga oid...)")
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
