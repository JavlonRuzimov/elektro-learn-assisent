from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("c6d3da40-fa42-43f6-93f5-cd98be96bc71", "b6212f59-9903-49e0-a292-68c2c2e16586", "Yonginga qarshi suv taminlash tizimi quvurlari qaysi rangga boyaladi (qizil rangga)"),
    ("f4159c1a-b287-46eb-b568-058c4b7a6129", "8e086407-7147-493d-ac50-3a3038688508", "Tashkilot hududining tashqi tarafidagi qurigan otlar masofasi (3 metr kenglikda tozalangan bolishi kerak)"),
    ("98dff556-6ce5-4249-9636-b9c8f335b5b6", "6798cf8d-ee66-43f5-9380-f1ac00dda197", "Yonginga qarshi suv quvuri sxemasi kim tomonidan tasdiqlanadi (bosh muhandis tomonidan)"),
    ("bf18057f-eed9-472f-a5c8-34274c8131e4", "c201a559-08bf-4d54-8b93-a16db2fd02f6", "Yongin xavfsizligi boyicha yoriqnomalar kim tomonidan tasdiqlanadi (tashkilotning raxbari)")
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
