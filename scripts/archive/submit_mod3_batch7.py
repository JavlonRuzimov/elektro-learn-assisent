from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("100ef5cc-90d2-462f-9c74-fe2fe2c924ca", "432481d8-eb8d-46f5-bcd8-0cc3792f2af4", "Transformator ostidagi shagal qachon almashtiriladi (qalinligi 3 mm dan kam bolmagan qattiq chokindilar yoki osimliklar paydo bolganda va yuvish mumkin bolmagan hollarda)"),
    ("fad3eb41-f88d-41af-a310-a1ed3d6d7556", "64a7f9c5-2492-49e8-a50d-a951b88a2833", "Yonginni ochirish tezkor varaqalari nima maqsadda (oqilona harakatini taminlash va vaqtini qisqartirish maqsadida)"),
    ("372f0cd7-c48c-41ad-9483-48fecf5adcae", "e0d36d60-cd01-4aea-b904-1b0d447ff30d", "Yongin xavfsizligini taminlash masuliyati (tashkilotlar rahbarlariga masuliyat yuklatiladi)"),
    ("17cd86a2-a3ec-4336-980d-cf23f9293e3f", "8c49f355-434c-4683-8079-17526a7373a8", "Yongin-texnik minimumi mashgulotlari kimlar bilan (yongin xavfi yuqori bolgan ishlarni bajaradigan xodimlar bilan)")
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
