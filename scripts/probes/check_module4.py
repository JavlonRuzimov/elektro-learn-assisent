from api.client import BaseClient
import json

THEORY_ID = "fce33f9f-1d2b-4926-a4e0-603181cd998f"

client = BaseClient()
res = client.get(f"/theories/{THEORY_ID}/questions?mode=continue")

with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

known = kb.get("questions", {})
questions = res.get("questions", [])

print(f"Server questions count: {len(questions)}")
print(f"Answered count: {res.get('answeredCount')}")
print(f"Remaining count: {res.get('remainingCount')}")

for i, q in enumerate(questions, 1):
    qid = q["id"]
    in_kb = qid in known
    print(f"\n--- Question {i} ---")
    print(f"QID: {qid} | In KB: {in_kb}")
    print(f"Prompt: {q['prompt']}")
    print("Options:")
    for opt in q.get("options", []):
        opt_id = opt.get("id")
        text = opt.get("optionText") or opt.get("text")
        mark = " (KB ANSWER)" if in_kb and known[qid].get("correctOptionId") == opt_id else ""
        print(f"  - [{opt_id}] {text}{mark}")
