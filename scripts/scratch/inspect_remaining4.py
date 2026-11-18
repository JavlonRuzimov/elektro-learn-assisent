import json
import sys
import os
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))

from api import ElektroLearnClient

client = ElektroLearnClient()
THEORY_ID = "007a32c2-6b88-44eb-8444-3bb7e831142f"

prog = client.progress.get_theory_questions(THEORY_ID)
print(f"Test 5: answered={prog.get('answered_count')}, remaining={prog.get('remaining_count')}, total={prog.get('total_questions')}")

for i, q in enumerate(prog.get("questions", [])):
    print(f"\n[{i+1}] ID: {q.id}")
    print(f"Prompt: {q.prompt}")
    for o in q.options:
        print(f"  Option: [{o.id}] {o.option_text}")
