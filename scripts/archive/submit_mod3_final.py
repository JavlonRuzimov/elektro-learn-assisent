from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("fe15c9db-e8e7-420f-a4db-4e0a2429c012", "19f18eaf-c100-4892-971e-085bfba40847", "Yongin-texnik komissiyasi nima maqsadda tashkil etiladi (boshqaruv xodimlari va mamuriy-texnik xodimlarning yonginlarning oldini olish va yonginga qarshi himoya boyicha...)"),
    ("49557bee-7e87-48dd-b9dd-a8466ed44f89", "f1ff2c2f-2a08-4ae0-988e-06534a332034", "0.4 kVgacha kuchlanish ostidagi uskunadagi yonginni nima bilan (yonginni qol stvollaridan purkaladigan suv oqimi bilan ochirishga ruxsat beriladi)"),
    ("06e8aeb8-f0f0-4460-8678-d7d10d20836d", "8932148a-80d5-4184-8586-d5b7d2354e52", "Yongin xavfsizligi boyicha yoriqnomalar qancha muddatda qayta korib chiqiladi (TEQQda belgilangan muddatlarda qayta korib chiqiladi)"),
    ("c3a9083b-b093-4fd8-92f6-7da9c580db3e", "fa319f41-19bd-4597-b143-620edd0c98ac", "Yongin xavfsizligi boyicha kirish yoriqnomasini kim otkazadi (muhandis-inspektor, u yoq bolganda tarkibiy bolinma boshligi)")
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
    hearts = res.get('hearts', {}).get('heartsCount')
    print(f"  Result: {is_cor} | Hearts: {hearts}")
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
