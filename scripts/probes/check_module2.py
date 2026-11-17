from api.client import BaseClient
import json

client = BaseClient()
t_id = 'f8888f56-bf87-4e67-b039-7009d07d2ff9' # Module 2: XTQ

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)
kb_q = kb.get('questions', {})

data = client.get(f'/theories/{t_id}/questions', params={'mode': 'continue'})
server_questions = data.get('questions', [])
print(f"Server questions count: {len(server_questions)}")
print(f"Answered count: {data.get('answeredCount')}")
print(f"Remaining count: {data.get('remainingCount')}")

for idx, q in enumerate(server_questions):
    qid = q.get('id')
    prompt = q.get('prompt')
    is_known = qid in kb_q
    print(f"\n--- Question {idx+1} ---")
    print(f"QID: {qid} | In KB: {is_known}")
    print(f"Prompt: {prompt}")
    if is_known:
        print(f"Verified Answer: {kb_q[qid]['option_text']}")
    else:
        print("Options:")
        for o in q.get('options', []):
            print(f"  - [{o['id']}] {o['optionText']}")
