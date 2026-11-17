import json
from api.client import BaseClient

client = BaseClient()
qid = "e9cb7b98-7a44-4110-8909-9a0b49ccb950"
opt_id = "7f0500db-e9eb-48b5-aa9f-43b77cd230f0"

print(f"Submitting DAILY_PLAN answer for qid={qid}, opt_id={opt_id}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "DAILY_PLAN"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
