from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("ca6adc5f-7511-439c-b774-d7b688751231", "33fa4f84-9348-4f0c-bc4c-13e0948d39bb", "Yonginga qarshi qalqonlar qaerlarda qollaniladi (faqat yogoch-taxta omborlari, qurilish bazalari, xojalik omborlari, turar joylari yogochdan qurilgan vaqtinchalik uylarda...)"),
    ("049ee561-365f-4cc4-b843-d79d0f676677", "71e93a41-475a-4a83-82f0-456b5896db7a", "Yonginga qarshi holat uchun javobgar shaxs yozuvda nimalar korsatiladi (familiyasi ismi otasining ismi, lavozimi, telefon raqami, portlab-yonish xavfi toifasi, zonalarning toifalari)"),
    ("d067b56d-8d5b-4d88-a5a1-59a81d311a5e", "196a1088-bd6f-4e4d-98c1-09094d4cc9f1", "YOOʻR kuchlanish ostida bolgan energetik uskunadagi yonginni qachon ochirishga kirishishi mumkin (yozma ruxsat olganidan, tashkilot xodimlari bilan yongin bolinmalari shaxsiy tarkibiga yol-yoriq berilgandan...)"),
    ("7b981200-79a9-4fd6-8fb2-359469732cf3", "57634b92-01fc-44db-850e-b0a96140dca1", "Yongin ochogini birinchi bolib payqagan xodim (obektning smena boshligiga yoki tashkilot rahbariyatiga xabar berishi va mavjud yongin ochirish vositalari bilan...)")
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
