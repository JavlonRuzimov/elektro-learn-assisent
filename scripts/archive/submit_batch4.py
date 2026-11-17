from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("1c904160-0f60-40eb-ab77-c2f63a74ae6c", "c284c3f8-f7d5-45c3-9467-850f3ab78764", "Kabel liniyasining muhofaza zonasida..."),
    ("ad789671-0a8c-4fd0-ba1d-54823feac108", "54742e62-52e6-4f99-b6d6-fa9ca438657e", "Ish joyini tayyorlovchi shaxs..."),
    ("1f29b15b-66aa-4a2e-8b75-0c79e1652e2e", "7139360a-396f-46ac-a450-8b04e55b044f", "Qanday xodim ish rahbari bo'lishi..."),
    ("303ad782-eada-40b8-8df3-b44cc8bc99aa", "48eaba8d-6673-45f9-9cf4-221cba8ea61a", "Elektrostantsiya va podstantsiya...")
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
