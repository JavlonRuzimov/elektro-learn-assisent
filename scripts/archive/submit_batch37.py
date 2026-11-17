from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("b21c37ce-1ebe-484d-afa9-6e94dc4c19da", "143adf5a-d6e5-45cf-9e62-6f59fe0ce53a", "Naryad muddatini uzaytirish ruxsatnomasi (telefon, radio yoki chopar orqali ishga qoyuvchiga, ish rahbariga yoki ish bajaruvchiga)"),
    ("87b266e9-8f2f-48c5-ab79-f39d5120af10", "f1289022-824c-4a27-9434-94dc25752d56", "Naryad yoki farmoyish berish huquqi kimga beriladi (V guruhga ega bolgan mamuriy-texnik xodimlarga beriladi)"),
    ("c99cf391-1ae8-438e-898a-79137f2ab3d2", "f5205bb5-1f87-4e27-acb4-5d8258f80bc5", "Brigadani boshqa ish joyiga otkazish qaerda rasmiylashtiriladi (naryadning 3-jadvalida rasmiylashtiriladi)"),
    ("9af5cf29-9496-4c67-9579-9e941eded7bc", "10060772-fcbc-400f-a61d-4ba1569a690d", "Ishni xavfsiz bajarish tashkiliy tadbirlar (javobgar shaxslarni tayinlash; naryad yoki farmoyish berish; ish joylarini tayyorlashga...)")
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
