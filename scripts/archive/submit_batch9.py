from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("ee2e6b29-bd6b-4fd0-971b-8be1bf13732f", "f5166905-4f96-4b90-bc06-bed91689ecc9", "Rasmiylashtirilgan naryad (ishga qoyuvchiga va ish bajaruvchiga)"),
    ("b8282e58-8ab8-45f3-8bed-453f7999a6c6", "03d492cd-765c-46d7-b823-d7cef08aecd7", "Ish bajaruvchi ketganda orniga kim qoladi (ish rahbari, ishga qoyuvchi yoki naryad berish huquqiga ega bolgan xodim)"),
    ("893e37ad-1455-460a-9947-35842dacc974", "22dc6a42-4157-4299-a5f5-2abbfd55afe8", "1000V kontaktlari korinmaydigan kommutatsion apparatlar (chiquvchi shinalarda kuchlanish yoqligini tekshirish)"),
    ("fb802b15-38a1-462b-b963-b90927def16c", "82231c90-2042-401e-a199-42bc40aa8fb0", "Naryad matniga tuzatishlar (man qilinadi)")
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
