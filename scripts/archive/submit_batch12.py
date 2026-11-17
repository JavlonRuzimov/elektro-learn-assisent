from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("79ce9156-4201-4358-b8fe-d6cd607c4f42", "4ae104c7-9ca3-4c6e-928f-f12479c9f27d", "Brigada tarkibini ozgartirish (telefon, radio yoki chopar orqali)"),
    ("917435ec-1b1e-480b-a50e-445668efebbc", "b0824fe0-c09a-4f21-9e80-d6e3cc20ef38", "Ish rahbarining javobgarligi (barcha xavfsizlik choralarining bajarilishi va etarliligi)"),
    ("ac4750fa-e55b-4592-9d57-00059291c52a", "bc5b79c8-3442-4683-ab33-ea9d9e6def22", "Izolyatsiyalovchi osmalarda harakatlanish (a va v javoblar togri)"),
    ("18528da6-d0d5-40f6-8932-e9ed00f2a914", "78d4498c-61ea-4069-86f6-0cbb95a49b9c", "Ish kuni davomidagi tanaffus (ish joyidan chiqarilishi, eshik qulflab qoyilishi shart)")
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
