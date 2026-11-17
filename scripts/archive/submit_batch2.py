from api.client import BaseClient
import json

client = BaseClient()
qid = "51dddb1f-038a-4303-b4ef-2b4be209d71f"
opt_id = "5d21ef39-65ce-449f-b0e6-5b81595024d2" # 132-band

print(f"Submitting verified answer for QID={qid}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "LESSON"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
