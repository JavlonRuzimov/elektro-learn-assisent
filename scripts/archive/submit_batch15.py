from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("f353a9ca-fbf2-4124-8795-e3b56efe297c", "4cc0297c-4c2b-49f2-966d-43745dd80f3d", "Ishga qoyuvchi nimaga javob beradi (korilgan xavfsizlik choralarining togriligi va etarliligi)"),
    ("19ceec0f-1246-4789-9818-d27561d98889", "595ab555-7de3-43ea-b0af-89b60d6ff882", "Tayanchlarni yiqitish va ornatish usullarini (ish rahbari, u tayinlanmagan bolsa naryad beruvchi)"),
    ("e90bbe91-6cde-45dc-ba5c-3ca92abf62f6", "d1fd4ec4-36c3-4032-b91b-01799ac7898e", "Ish jarayonida nazorat olib borish (xavfi koproq joyda turib)"),
    ("22f0278d-746e-4f5a-82a7-c53ac924a119", "ea2264d5-3ed8-4eda-bee0-b1808ae431be", "Ish toliq tugaganligi togrisida xabar berish (ishga qoyuvchiga, u yoq bolsa ruxsat berganga)")
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
