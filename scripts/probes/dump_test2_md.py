import json

with open("data/test2_all_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

lines = ["# 9-Daraja: Test № 2 Savollari (40 ta)\n"]
for idx, q in enumerate(questions, 1):
    lines.append(f"### {idx}. {q['prompt']}")
    lines.append(f"**ID:** `{q['id']}`\n")
    lines.append("Variantlar:")
    for o in q['options']:
        lines.append(f"- `[{o['id']}]` {o['option_text']}")
    lines.append("\n---\n")

with open("data/test2_questions_list.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Written {len(questions)} questions to data/test2_questions_list.md")
