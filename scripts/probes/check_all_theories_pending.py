from api.client import BaseClient
import json

client = BaseClient()
with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)
kb_q = kb.get('questions', {})

with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    l8_theories = json.load(f)

print("Checking Level 8 theories for questions known in KB that are pending on server:")
all_pending_known = []
for t in l8_theories:
    t_id = t.get('theoryId')
    t_title = t.get('title')
    try:
        data = client.get(f'/theories/{t_id}/questions', params={'mode': 'continue'})
        server_q = data.get('questions', [])
        known = [q for q in server_q if q['id'] in kb_q]
        print(f"\nTheory: {t_title[:45]}")
        print(f"  Total on server: {len(server_q)} | Answered: {data.get('answeredCount')} | Known in KB: {len(known)}")
        for q in known:
            all_pending_known.append((q, t_id, kb_q[q['id']]))
            print(f"    - [{q['id']}] {q['prompt'][:60]}...")
    except Exception as e:
        print(f"Theory {t_title[:30]} error: {e}")

print(f"\nTOTAL pending questions in Level 8 with 100% verified answers in KB: {len(all_pending_known)}")
