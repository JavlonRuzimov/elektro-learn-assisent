from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("79a21e0d-fe24-4127-81ca-98c5b2ca9a24", "9f6766b8-4ebd-4fa1-ac49-14be935c8881", "Dublyorlikdan kimlar va qaysi holatlarda otadi (tezkor va tezkor-tamirlash xodimlari birlamchi bilim sinovidan otganda, uzoq tanaffusdan song...)"),
    ("aceae0e1-2173-4cb9-be84-3c99eb530c53", "361d53a5-1ef8-4178-af76-85bcceafeb4e", "Xodimning dublyorlikdan otishiga ruxsatni kim beradi (korxona yoki tarkibiy bolinma raxbari buyruq yoki farmoyishi bilan)"),
    ("f2e7a02d-4d88-4cfd-8227-3b34875b6136", "22fa9956-2b88-4690-8967-8ba838450a5f", "Birlamchi takroriy va rejadan tashqari yoriqnomalar (xodimning bevosita rahbari)"),
    ("83dbd172-1d9b-4dd8-bbf6-9950208b91cc", "e266c457-ecfa-4953-8fc8-074f0f661e0a", "Bilim sinovini qayd qilish jurnali qancha muddat saqlanadi (jurnal bilim sinovi komissiyasida 10 yil saqlanadi)")
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
