from api.client import BaseClient
import json

client = BaseClient()
with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    l8_theories = json.load(f)

for idx, t in enumerate(l8_theories):
    t_id = t.get('theoryId')
    t_title = t.get('title')
    try:
        data = client.get(f'/theories/{t_id}/questions', params={'mode': 'continue'})
        server_q = data.get('questions', [])
        ans_count = data.get('answeredCount')
        if not server_q:
            continue
        print(f"\n=======================================================")
        print(f"MODULE {idx+1}: {t_title}")
        print(f"Theory ID: {t_id} | Answered: {ans_count}")
        print(f"=======================================================")
        for q_idx, q in enumerate(server_q):
            print(f"\n  Q{q_idx+1}: [{q['id']}] {q['prompt']}")
            for opt in q.get('options', []):
                opt_text = opt.get('text') or opt.get('optionText') or opt.get('content') or opt.get('label')
                print(f"      - [{opt['id']}] {opt_text}")
    except Exception as e:
        print(f"Error {t_title}: {e}")
