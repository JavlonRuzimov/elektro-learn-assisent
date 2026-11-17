from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("368a0798-812a-463f-ad24-fbaa9a97f45a", "962b61cb-6dbd-4fe4-b6b8-2e479a0aedba", "Ish toliq tugagandan keyin tarmoqqa ulash (ish joyini tayyorlashga va ishga qoyishga ruxsat bergan yoki almashtirgan...)"),
    ("dc9b4eec-a7e4-4d31-8bed-b6adc8b61aca", "20106801-4237-49f4-9a77-d0d11176f855", "Ish joyini tayyorlash talab qilinmaydigan ishlarda 1-jadvalga (Talab qilinmaydi deb yozib qoyiladi)"),
    ("bdd5c399-5311-4357-a01e-259a2f46905c", "98b37acc-9021-4998-917b-15d96286bc6c", "Kuchlanish ostida quyidagilar qoldi satriga (tamirlanayotgan va ish joyi yaqinidagi qoshni ulanmalarning...)"),
    ("c6805f44-523d-4c7a-b762-871b832a77cc", "2e434a83-79b5-4bf1-846e-0f910ace0788", "Naryad va farmoyishlar boyicha ishlarni hisobga olib borish (naryad va farmoyishlarni xisobga olish jurnalida)")
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
