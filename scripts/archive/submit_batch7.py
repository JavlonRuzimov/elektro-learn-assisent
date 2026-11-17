from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("a21a263c-32d3-45a8-aaf5-e3dade977f83", "cb70d9eb-69db-4a66-bb01-238c0292b2cb", "Farmoyish bilan ish bajarilayotganda..."),
    ("b1c2af2e-1049-4842-84c8-a3b9d382739b", "8266dbfe-9830-47c2-8f61-988d35c73e59", "Ish jarayonida brigada azolaridan biri..."),
    ("e14adf92-dda5-4713-a2d2-6d0a0227d964", "1fb24c3b-a874-4a8a-a2ee-8e9ea7e5525a", "Naryadning 3-jadvaliga nima yoziladi?"),
    ("2e7e3d5b-896b-41df-bd69-92407be2c48e", "c6653c71-8932-438d-aa78-cefed3afe77d", "Qaysi xolatda kuzatuvchi tayinlanishi kerak?")
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
