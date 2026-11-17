import json

with open('data/m5_matched.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for item in items:
    score = item['best_score']
    runner_score = item['runner_up'][0] if item['runner_up'] else 0
    diff = score - runner_score
    print(f"Q{item['num']:02d}: Score={score:.2f}, Diff={diff:.2f} | Best: {item['best_text'][:60]}")
