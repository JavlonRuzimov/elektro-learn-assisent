import sys
import os
import json
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient

client = ElektroLearnClient()
t3 = client.progress.get_theory_questions('4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b')
for i, q in enumerate(t3['questions'], 1):
    print(f"\n--- Question {i} ---")
    print(f"ID: {q.id}")
    print(f"Prompt: {q.prompt}")
    print("Options:")
    for o in q.options:
        print(f"  [{o.id}] {o.option_text}")
