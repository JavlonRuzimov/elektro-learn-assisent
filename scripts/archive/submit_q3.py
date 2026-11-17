from api.client import BaseClient
import json

client = BaseClient()
qid = "5ac80a0c-0ce8-426f-b011-533f1d07f294"
opt_id = "aa3a2494-5738-4c46-a29e-11d7bcc5c851" # 19-band

print(f"Submitting verified answer for QID={qid}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "LESSON"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
