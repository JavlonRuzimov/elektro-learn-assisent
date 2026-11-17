from api.client import BaseClient
import time

client = BaseClient()

submits = [
    ("8655eca2-b635-416b-9a58-357fdfed9423", "30b7e53b-6c28-4198-bda2-acd373f6c683", "Uskunalarni ekspluatatsiya qilish bo'yicha yo'riqnomalarga..."),
    ("bf0744b0-6b28-4886-95f1-42f01106198a", "4b8fc48b-dc8d-4cc6-84ec-31a13db9394f", "Yuqori turuvchi tezkor xodimning farmoyishi...")
]

for qid, opt_id, desc in submits:
    print(f"\nSubmitting LESSON answer for: {desc}")
    time.sleep(1.5)
    res = client.post("/progress/answer", data={
        "questionId": qid,
        "selectedOptionId": opt_id,
        "source": "LESSON"
    })
    print("  Result isCorrect:", res.get("isCorrect"))
    print("  XP Earned:", res.get("xpEarned"))
    print("  Hearts:", res.get("hearts"))
