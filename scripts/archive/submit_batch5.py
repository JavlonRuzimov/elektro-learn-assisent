from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("c81c4a4e-b48e-45cd-b760-68eca56cfbf3", "89a928ff-4634-4da5-a05e-7ba2e13bb5c5", "Noelektrotexnik xodimlar..."),
    ("fcdad520-b683-41b2-8b13-0a5b2ddaa273", "841a17f0-4c10-476e-817c-676400ab6ebd", "Tayanchning detallarini..."),
    ("284bc2ef-922b-433c-85c7-2af870f3a3bf", "ed958b12-e08e-4eac-b24c-b9f92f269499", "Brigada azolari soni..."),
    ("a6baefcd-75b9-4d13-a874-5b1e2d77ff57", "39bdca65-d3af-4991-abbf-5592d9597d58", "Daraxtni to'liq kesmasdan...")
]

for qid, opt_id, desc in submits:
    print(f"\nSubmitting LESSON answer for: {desc}")
    print(f"  QID={qid}, OPT_ID={opt_id}")
    time.sleep(1.5)
    res = client.post("/progress/answer", data={
        "questionId": qid,
        "selectedOptionId": opt_id,
        "source": "LESSON"
    })
    print("  Result isCorrect:", res.get("isCorrect"))
    print("  XP Earned:", res.get("xpEarned"))
    print("  Hearts:", res.get("hearts"))
