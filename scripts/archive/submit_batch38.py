from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("8cdd1732-c859-4e97-acd0-682d0fa31083", "a4bee865-90ff-4c2a-8f8d-0dc90dc89481", "Kop zanjirli izolyatsiyalovchi osmalarda ximoya kamari arqoni (izolyatorlarning ish olib borilamayotgan shodalarining biriga maxkamlashga)"),
    ("9ffda8d5-d38a-4210-a044-14f6cfcaea4c", "468c0e16-b340-40ab-a139-e3db4047d265", "Daraxtning aganayotganligi togʻrisida ishchilarni kim ogohlantirishi kerak (arrakash boshqa ishchilarni oldindan ogohlantirishi shart)"),
    ("a007844e-db9c-49f4-8c31-b1f10f61e1ef", "d9626d90-336f-467b-9ea5-8b64b01c6bbd", "Kuzatuvchi EX boyicha nechanchi guruh bolishi kerak (III guruhga ega bolishi kerak)"),
    ("dc6ee87b-f75e-45fb-bff1-51ff6d01a5b0", "055fe028-5e0d-4435-a740-b75087cacdc0", "Farmoyish kimga beriladi (ish bajaruvchiga va ishga qoyuvchiga yoki ish joyini tayorlashga va ishga qoyishga ruxsat beruvchiga)")
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
