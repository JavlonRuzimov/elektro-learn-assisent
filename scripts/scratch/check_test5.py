import sys
import os
sys.path.insert(0, os.path.abspath("."))
import json
from api.client import ElektroLearnClient

client = ElektroLearnClient()
client.load_session()

theory_id = "007a32c2-6b88-44eb-8444-3bb7e831142f"
user_info = client.auth.get_user()
print("User:", user_info.get("first_name"), user_info.get("last_name"), "Hearts:", user_info.get("hearts"), "XP:", user_info.get("xp"))

level_id = "7577259e-4295-4d5f-a504-69626ac29587"
level_detail = client.progress.get_level_detail(level_id)
for t in level_detail.get("theories", []):
    if t.get("id") == theory_id:
        print(f"Theory 5: completed_count={t.get('completed_count')}, total_count={t.get('total_count')}")

questions = client.theory.get_questions(theory_id)
print(f"Total questions returned: {len(questions)}")
for i, q in enumerate(questions):
    print(f"Q{i+1}: ID={q.get('id')} | Text={q.get('question_text')}")
