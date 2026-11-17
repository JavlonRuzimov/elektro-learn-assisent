from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("380a8648-f4e1-4fac-83d5-4a31c8c675f5", "e5de3ea4-5d9b-4b7b-8d56-6bfe4dfdff3e", "Ish kuni tugashi tufayli tanaffus (ish joyidan chiqariladi, plakatlar olinmaydi)"),
    ("f728930b-27ba-47e2-a759-315078588b61", "dd922f13-4a49-4a4b-bb44-16ff274c222d", "Daraxtlarni agnatishdan oldin (ish joyi tozalanishi shart)"),
    ("b5ad1ccc-8cf8-416c-a4d1-a3079b52483f", "275b875a-7366-45ae-b570-9a4e4032ac26", "Naryadni olgandan keyin ishga qoyuvchi (kozdan kechirishi va ruxsat berganga xabar berishi)"),
    ("47f56795-e573-4b0d-8cad-1da9e9786214", "0f13ea39-ed43-4c10-97bc-8cdedf2fc6b3", "Naryad faqat ikki nusxada yozilishi (ish bajaruvchi bir vaqtning ozida ishga qoyuvchi bolganda)")
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
