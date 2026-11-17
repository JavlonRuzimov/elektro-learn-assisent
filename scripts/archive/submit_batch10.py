from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("c2321701-e549-46dc-8214-6bd0e25f6573", "b5326b68-a6a3-48b7-9474-891694e5d5a2", "Sim va trosslarni tortishda (traversda yoki travers ostidagi ustunlarda turish taqiqlanadi)"),
    ("3c182f8b-9d8d-44d7-9f21-c372e3a91b88", "25fe1fc7-a007-45a4-98b2-4795661df3f7", "Ishga qoyish naryadda qanday rasmiylashtiriladi (naryadning har ikki nusxasida rasmiylashtiriladi)"),
    ("69d75047-2def-4179-a636-047fa9c9bc57", "cd6800b7-f691-4f22-ae39-35518bc2217a", "Naryad beruvchi orindoshlik yo'li bilan (ish raxbari va maxalliy navbatchisiz elektr qurilmalarda ishga qoyuvchi)"),
    ("0dded3b0-ec9c-41f7-a2a4-152e307f5707", "25c40649-6108-4bb8-96da-8119c489df22", "Tezkor-tamirlash ishga qoyuvchiga 1-jadval 2-ustuni (ochirish va erga ulashni yozib qoyadi)")
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
