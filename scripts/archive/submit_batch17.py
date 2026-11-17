from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("e74aefd1-2c3f-4f90-9132-56cd74bc76ab", "dd323e29-3d20-4c55-8ece-879cec0cf95e", "Ajratgichlar ochirilgandan song (ochganligi korilishi va shuntlovchi tutashtirgichlar yoqligi)"),
    ("6a13ea1d-2fc4-422e-8efb-278c14b07671", "58777800-a4ff-4f65-8f9b-771241def4d0", "Naryad tarifi (toliq maxsus blankdagi topshiriq)"),
    ("7679cbba-59b2-4f35-9b71-9a6c720696ec", "02478755-46d3-49a3-b46f-799106a95935", "Navbatchi brigada tarkibiga (tezkor jurnalga yozib qoyilib)"),
    ("6c116d00-ac95-4c79-9e74-9f3e8c78803e", "bc893197-425e-4453-b358-3ec3484da82f", "Ish rahbari tayyorlikni kim bilan tekshiradi (ishga qoyuvchi bilan birga yoki mustaqil)")
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
