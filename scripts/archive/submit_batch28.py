from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("2949c201-7b83-4285-a870-d76e29c0ccff", "1d71d0e9-87ed-4901-a864-033d522c957d", "Xodimga qachon I guruh beriladi (ushbu elektr qurilmada elektr xavfsizligi bo'yicha yo'riqnoma olib...)"),
    ("3f21954f-91b5-4927-9eb5-f555c1eba68b", "52e5d326-cdcd-4cc4-bcd1-6cdd76806bd8", "18 yoshga to'lmagan shaxslarga nechanchi guruh berilishi mumkin (II guruhdan yuqori guruh berishga ruxsat etilmaydi)"),
    ("bee4c2d4-c441-4d91-a5d5-87cfd082b145", "3d477e18-0d6c-49b2-a132-90806d565b30", "I guruhga ega brigada azosi tayanchga chiqishi mumkinmi (er sathidan 3 metrgacha... bo'lgan balandlikga mumkin)"),
    ("e550e078-0c7b-49bd-ac58-9a17e07ee115", "f384fb63-5e46-4d50-9181-08f9aa645a7d", "Chirigan va qurigan daraxtlarni ag'natishdan oldin nima qilish kerak (mahkamligini tekshirish kerak)")
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
