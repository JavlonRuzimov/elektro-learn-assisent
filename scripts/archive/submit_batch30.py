from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("c3c2cf6e-3008-4aaf-9d86-eb2f574fb09e", "42c81f75-fa0d-43e6-9fe5-472d37ffde24", "Ushlab turuvchi izolyatsiyalovchi osmada ishlaganda ximoya kamari arqoni qaerga mahkamlanadi (traversga mahkamlanishi shart)"),
    ("3d5240b1-2ab0-4ffc-bc8f-2d23a707c128", "89410ab8-2591-431c-9630-c1d6af9290d7", "Ishdagi tanaffus vaktida naryad kimda qoladi (ish bajaruvchida kuzatuvchida qoladi)"),
    ("61677d8c-96e7-4e45-a8e4-e01e3081150a", "23487668-377c-45d9-b6b0-23aefe2b98d9", "HLlariga javobgar ijrochilarni ishga qoyishda erga ulagich (har bir brigada ishlayotgan uchastkaga bittadan erga ulagichni ornatishi shart)"),
    ("d190804c-a0bb-48ab-9e32-9dbe16a2594c", "556539dd-0cfe-49fd-9d10-595a0b8330d4", "Farmoyish boyicha ishga qoyish qaerda rasmiylashtiriladi (tezkor jurnalda yoki naryad va farmoyishlar boyicha...)")
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
