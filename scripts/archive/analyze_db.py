import json

path = r'C:/Users/Administrator/.gemini/antigravity/brain/d42ebc41-2709-4f6c-8d15-11d49c1faac2/.user_uploaded/media_1794819891410_73c599a9.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

levels = data.get('levels', [])

# Collect all questions by ID and prompt
all_q_by_id = {}
all_q_by_prompt = {}

for lvl in levels:
    lvl_name = lvl.get('title')
    order = lvl.get('orderIndex')
    for t in lvl.get('theories', []):
        t_name = t.get('title')
        for q in t.get('questions', []):
            qid = q.get('id')
            prompt = q.get('prompt', '').strip()
            if prompt in all_q_by_prompt:
                all_q_by_prompt[prompt].append((lvl_name, t_name, qid))
            else:
                all_q_by_prompt[prompt] = [(lvl_name, t_name, qid)]

duplicates = {k: v for k, v in all_q_by_prompt.items() if len(v) > 1}
print(f"Total unique prompts: {len(all_q_by_prompt)}")
print(f"Prompts appearing in multiple places: {len(duplicates)}")
for p, locs in list(duplicates.items())[:5]:
    print(f"\nPrompt: {p[:80]}...")
    for loc in locs:
        print(f"  Level: {loc[0]} | Theory: {loc[1]}")
