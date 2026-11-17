from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("9dfd69f3-33c4-4237-8a49-8afc9bb3cfff", "347904bd-0ce1-46f0-96c7-fbe94d6fb39a", "Ishga qoyishdan oldin nima qiladi (qanday choralar korilganini aniqlashi va shaxsan kozdan kechirishi)"),
    ("5c171857-4a18-49ae-91ec-e4d125ad92a7", "fb339e6f-9b6c-4369-8f3a-a8e47ff49b32", "Naryad necha nusxada (ikki nusxada, telefon yoki radio orqali uch nusxada)"),
    ("70c07beb-f4fe-476d-bdd8-523ff94978f4", "4ff470a7-dce0-442f-b064-a99907be912c", "Yozma korsatma bilan beriladigan huquqlar (naryad, farmoyish berish, ish rahbari, ish bajaruvchi, ishga qoyuvchi)"),
    ("a2807d10-305e-4705-9f85-5a517a182289", "8a7f5d19-da23-4f98-b979-2b99758174b7", "Ish butunlay tugatildi qatoriga (vaqt va sanani korsatib imzo qoyadi)")
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
