from api.client import BaseClient
import json

client = BaseClient()
qid = "8d813f1e-fc72-41be-bf8a-631e6a244be1"
opt_id = "6f2b4a9d-e186-4b03-9771-2f2aaf3fb07b"

print(f"Submitting verified answer for QID={qid}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "LESSON"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
