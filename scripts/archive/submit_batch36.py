from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("2a9a37a9-5652-4643-ac6d-f8d0cb635208", "3aa6ba45-95fd-4fc4-830a-0dd52095bb13", "Tayanchning yuqori qismigacha boyash ishlarini kim amalga oshirishi mumkin (II guruhga ega brigada azosi bajarishi mymkin)"),
    ("21ba94e6-41cc-4465-b432-ee4665d30d45", "9cf226ea-e71e-4af7-9320-8e35b077d5e3", "Kelgusi kuni brigada ishni boshlashdan oldin (plakatlar tosiqlar bayroqchalar butunligi erga ulagichlar ishonchliligi)"),
    ("8a5ae3bd-0667-4390-9a90-37cae10dcdf5", "2bc91074-b9e0-4e37-9074-47229fac1d57", "Ish jarayonida brigada azolari ustidan nazorat kimga yuklanadi (ish bajaruvchiga kuzatuvchiga yuklanadi)"),
    ("2d844e28-1141-4ced-95ce-09c0e8df9b50", "4483d72d-fd3e-435b-97cd-2ae58403eafb", "Kim ish joyini tayyorlashga va ishga qoyishga ruxsat etuvchi shaxs bolishi mumkin (IV guruh navbatchi, korxona korsatmasi boyicha mamuriy-texnik)")
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
