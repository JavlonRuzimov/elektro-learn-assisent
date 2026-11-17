from api import ElektroLearnClient

client = ElektroLearnClient()
level3_id = "a6a784c7-b454-4d3c-af92-3d2dab7f0f30"
detail = client.progress.get_level_detail(level3_id)
t = detail.theories[0]
q_data = client.progress.get_theory_questions(t.id, mode="continue")
print(f"Jami savollar: {len(q_data.get('questions', []))}")
for q in q_data.get("questions", []):
    print(f"\n[Q_ID: {q.id}] {q.prompt}")
    for opt in q.options:
        print(f"   [{opt.id}] {opt.option_text}")

