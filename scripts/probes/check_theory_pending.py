from api.client import BaseClient
import json

client = BaseClient()
with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)
kb_q = kb.get('questions', {})

t_id = '54778b29-a10e-4fb9-8b80-b4c36bc4d6dc'
data = client.get(f'/theories/{t_id}/questions', params={'mode': 'continue'})
questions = data.get('questions', [])
print(f"Retrieved {len(questions)} questions:")
for q in questions:
    qid = q.get('id')
    prompt = q.get('prompt')
    is_known = qid in kb_q
    print(f"\nID: {qid} | Known in KB: {is_known}")
    print(f"Prompt: {prompt}")
    if is_known:
        print(f"Verified Answer in KB: {kb_q[qid]['option_text']}")
    else:
        print("Options available:")
        for o in q.get('options', []):
            print(f"  - [{o['id']}] {o['optionText']}")
