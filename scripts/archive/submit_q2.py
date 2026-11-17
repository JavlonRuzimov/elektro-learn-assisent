from api.client import BaseClient
import json

client = BaseClient()
qid = "4cfbf0e7-7124-4c88-a7af-12241f3a7611"
opt_id = "f333793a-318f-4b2a-a01c-4d409dbd3948"

print(f"Submitting verified answer for QID={qid}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "LESSON"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
