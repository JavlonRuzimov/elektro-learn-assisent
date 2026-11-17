import sys
import os
sys.path.insert(0, os.path.abspath("."))
import json
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

with open("data/all_500_questions.json", "r", encoding="utf-8") as f:
    all_500 = json.load(f)

flat_500 = []
for mod in all_500:
    flat_500.extend(mod.get("questions", []))

print(f"Total flat 500 questions: {len(flat_500)}")

theory_id = "62ff9db9-4545-4944-9a7b-27de8e31b522"
q_data = client.progress.get_theory_questions(theory_id, mode="continue")
questions = q_data["questions"]

print(f"\nTest 1 questions in current batch: {len(questions)}")
for idx, q in enumerate(questions, 1):
    print(f"\n================ Q{idx} ================")
    print(f"ID: {q.id}")
    print(f"Prompt: {q.prompt}")
    print("Options:")
    for o in q.options:
        print(f"  [{o.id}] {o.option_text}")
    
    # Check match in flat_500
    p_lower = q.prompt.strip().lower()
    matches = [x for x in flat_500 if p_lower in x.get("prompt", "").strip().lower() or x.get("prompt", "").strip().lower() in p_lower]
    if matches:
        print(f"  >>> Found {len(matches)} match in 500 database:")
        for m in matches:
            print(f"      500 ID: {m.get('id')}")
            print(f"      500 Prompt: {m.get('prompt')}")
            for opt in m.get("options", []):
                print(f"        opt: [{opt.get('id')}] {opt.get('text')}")
    else:
        print("  >>> No match in all_500_questions")
