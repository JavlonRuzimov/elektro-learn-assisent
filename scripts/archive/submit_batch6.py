from api.client import BaseClient
import time
import json

client = BaseClient()

submits = [
    ("4d30f829-898d-4a9a-b286-6282ebdbc5b5", "0bf4fdbe-2ce4-46c5-bca0-38e58ef8fbca", "Kesilayotgan daraxtni..."),
    ("039d7189-2191-4d4b-b54e-07c7608fa941", "4fd132ed-34f7-41a7-a19b-d63ca086757f", "Qachon ish rahbari yoki tamirlash..."),
    ("26abac3a-b2a0-41a1-b183-ae53dda0cb66", "e80494c9-7697-4ab9-8844-4dbaea29289e", "Ish kuni tugashi tufayli..."),
    ("b8a6285a-9848-48aa-9847-91a11072e604", "55c6d61e-71f6-4dc1-8086-3c4f1e155749", "Ish bajaruvchi raxbarlik...")
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
