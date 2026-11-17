import json
from autopilot import VERIFIED_ANSWERS

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb.get('questions', {})
synced = 0

with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    l8_theories = json.load(f)

all_q_map = {}
for t in l8_theories:
    for q in t.get('questions', []):
        all_q_map[q['id']] = q

for qid, opt_id in VERIFIED_ANSWERS.items():
    if qid not in kb_q:
        q_obj = all_q_map.get(qid)
        prompt = q_obj.get('prompt') if q_obj else "Unknown prompt"
        opt_text = "Verified from autopilot"
        if q_obj:
            for o in q_obj.get('options', []):
                if o['id'] == opt_id:
                    opt_text = o['optionText']
                    break
        kb_q[qid] = {
            "correct_option_id": opt_id,
            "prompt": prompt,
            "option_text": opt_text
        }
        synced += 1

print(f"Synced {synced} entries from VERIFIED_ANSWERS to knowledge_base.json!")
with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)
