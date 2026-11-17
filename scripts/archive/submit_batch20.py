from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("bdd27619-ef98-423d-a8c6-008880c28db6", "e2bb70ed-29e3-4e80-8991-3889e75bb95e", "Ish toliq tugagani naryad kimga topshiriladi (ishga qoyuvchiga, amaldagi naryadlar jildiga)"),
    ("db64b264-8d03-43e1-aed3-8f0748b61e61", "4a8a076f-5d71-4fff-9220-fe27b32bf78e", "Naryad sanasi qanday yoziladi (avval kun, keyin oy, yilning oxirgi ikki soni)"),
    ("f2c92924-29c6-48ca-a820-5c47375716f9", "4f3643c1-7f55-4231-94b4-2e74b59e1af3", "HLda 1-jadvalga nima yoziladi (1-ustun liniya nomi, 2-ustun kommutatsiya apparatlari va tayanchlar)"),
    ("a417f1a2-497b-48f7-9f1c-974709c6398b", "1d528c99-0f8c-46ad-b7d4-60db503427cc", "Elektr qurilmani ishga tushirish ruxsati (barchasidan ish toliq tugagani haqida xabar olingandan song)")
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
