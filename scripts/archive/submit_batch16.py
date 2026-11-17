from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("b26a3d6b-549b-44b3-ab9a-cc18e05a2f46", "aaf0fda0-a450-4ae2-911b-4294bd48bf04", "Navbatchi bolmaganda farmoyish kimga beriladi (togridan-togri ish bajarayotgan shaxsga)"),
    ("8b4c7837-fcd1-4913-9bc3-bbd215e58a40", "3fe28f1a-a982-43a7-a3f7-d37a7bc7a3b0", "Farmoyishning muddati qancha (bajaruvchilar ish kunining davomiyligi)"),
    ("814e9ce2-c3dd-4e1e-bfff-1b78c3aca184", "42f6f715-5018-436a-8d13-1f42246d5b7e", "QMT uchastkasida yerga ulagichni kim ornatadi (ekspluatatsiya korxonasining ishga qoyuvchisi)"),
    ("e5cc174a-a5fa-4fdb-88b1-bd64ad8c934f", "ecb97704-14f3-4d48-8806-dc1f1c765e0f", "Ish joyini tayyorlash qachon toxtatiladi (choralarning togriligi va yetarliligiga shubha bolganda)")
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
