from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("98d4b203-b13b-4bc3-8bd3-653cc67d70bf", "ac4c6ba4-b38d-4d34-b139-3da453573e63", "Ish kuni davomidagi tanaffusdan song ish joyiga qanday qoyiladi (naryadda rasmiylashtirmasdan ishga qoyadi)"),
    ("3de75082-4f5c-4cfa-832f-5ac647c7a3a9", "81d8b18b-3033-452c-b210-0c18b1570496", "Izolyatsiyalovchi osmalarni ajralib ketishiga olib keladigan nosozliklar (ish toxtatilishi shart)"),
    ("152007ee-201a-4ab2-a4a2-4dbf7227da43", "c0161ae4-d738-4e8e-8620-8df917b2d7a4", "Ishni xavfsiz olib borishga qaysi shaxslar javobgar (naryad beruvchi, ish rahbari, ruxsat beruvchi, tayyorlovchi, ishga qoyuvchi, ish bajaruvchi, kuzatuvchi, brigada azosi)"),
    ("893e37ad-1455-460a-9947-35842dacc974", "22dc6a42-4157-4299-a5f5-2abbfd55afe8", "Kontaktlari korinmaydigan apparatlar ochirilgan holati (apparatlardan chiqqan qisqichlarda yoki ushbu apparatlar orqali ulanadigan... kuchlanish yoqligini tekshirish)")
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
