from api.client import BaseClient
import json

client = BaseClient()
qid = "31561321-a9eb-433b-88b7-ba35efbbc723"
opt_id = "9a93cdb0-351c-4bae-a027-145226a13b2b" # 71-band

print(f"Submitting verified answer for QID={qid}...")
res = client.post("/progress/answer", data={
    "questionId": qid,
    "selectedOptionId": opt_id,
    "source": "LESSON"
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
