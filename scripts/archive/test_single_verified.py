from api.client import BaseClient
import json

client = BaseClient()
qid = "ef9b05c9-bc0a-4862-915f-cf5efff54d7b"
opt_id = "8ab48fbd-82dd-4047-92f0-fe7f91161198" # 1 ta (PUE 2.5)

print(f"Submitting verified answer for QID={qid}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "LESSON"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
