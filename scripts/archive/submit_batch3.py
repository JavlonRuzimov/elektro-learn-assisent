from api.client import BaseClient
import json

client = BaseClient()
qid = "6f9d9e97-b1d5-476d-adc8-785a9bfad98a"
opt_id = "57497f6b-8024-40f3-8c44-7862886d47d9" # 8-band: Tayinlanmaydi

print(f"Submitting verified answer for QID={qid}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "LESSON"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
