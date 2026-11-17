from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("72ddbf4f-c8bf-43b1-9342-b1b23fb91a37", "702c9abd-a1aa-48b8-971f-7f095df6f0bb", "IV va V guruxni olish uchun xodim nimani bilishi kerak (elektr qurilmalarning joylashishini va ishni xavfsiz tashkil qilishni...)"),
    ("83b6ac87-ab08-48c1-ab84-f6a1a1af6dae", "9baa6832-37cd-407b-a57f-102c3cbf7369", "Podstantsiyalarda brigadani boshqa ish joyiga otkazish qachon rasmiylashtiriladi (bir taqsimlash qurilmasidan boshkasiga otkazishda)"),
    ("aa5a421b-36da-4d22-8e70-c38674c2a780", "87a75c93-c5a7-4002-904c-1beb855f5b5d", "Ish joyini tayorlash va ishga qoyish qachon amalga oshiriladi (navbatchi yoki vakolati bor shaxsdan ruxsat olgandan song)"),
    ("685d655d-0f37-4979-928c-bf7badcadbf8", "2ede468e-15c9-4c55-9176-c76e8282dcc1", "Naryadda elektr qurilmalarning nimasi korsatiladi (elektr qurilmalarining, ulanmalarning, uskunalarning dispetcherlik nomi)")
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
