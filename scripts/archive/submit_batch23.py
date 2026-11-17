from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("eb171fd8-4351-4643-bbd6-1b94ffa8cbdc", "8f1ec73d-6552-46b0-a1c5-01b618d6a697", "Ish joyini tayyorlash va ishga qoyishga ruxsat (amalga oshiruvchiga va ishga qoyuvchiga shaxsan, telefon, radio, chopar yoki oraliq podstantsiya)"),
    ("01a8120e-9ec4-4be4-b671-1f7c709b145c", "39d7a160-e010-46d1-bf05-d5a9de10f7b0", "Naryadga joy yetishmasa (naryad beruvchining imzosi bilan qoshimcha naryad)"),
    ("874a189f-90ab-49e6-b526-46e7d88c7d66", "5d3463bd-c849-4bdf-a800-bfc6a4109bb0", "Topshiriladi satriga (uskunaning nomi, ulanmalari hamda ishning mazmuni)"),
    ("8b21a3fb-b36f-482b-bd08-d30f47b2a321", "21be9870-c267-4910-8bdd-d98a057142d8", "V guruhni olish uchun (har bir band talablarining kelib chiqishini aniq bilishi)")
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
