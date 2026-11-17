import json

with open('data/m5_analyzed.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

unmatched = []
for item in items:
    if not item['clause'] or not item['snippet']:
        unmatched.append(item)

print(f"Total unmatched/no clause: {len(unmatched)}")
for item in unmatched:
    print(f"Q{item['num']}: {item['prompt']} (Clause: {item['clause']})")
    for opt in item['options']:
        print(f"   [{opt['id']}] {opt['optionText']}")
