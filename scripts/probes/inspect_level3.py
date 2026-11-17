from api import ElektroLearnClient

client = ElektroLearnClient()
level3_id = "a6a784c7-b454-4d3c-af92-3d2dab7f0f30"
detail = client.progress.get_level_detail(level3_id)

print(f"=== Level 3: {detail.title} ===")
print(f"Mavzular soni: {len(detail.theories)}")

for idx, t in enumerate(detail.theories, 1):
    print(f"\n" + "="*50)
    print(f"{idx}-Mavzu: {t.title} (ID: {t.id})")
    print(f"Savollar: {t.answered_questions}/{t.total_questions}")
    print(f"Mavzu matni (Content):\n{t.content}")
    print("-" * 50)
    q_data = client.progress.get_theory_questions(t.id, mode="continue")
    questions = q_data.get("questions", [])
    print(f"Savollar soni: {len(questions)}")
    for q in questions:
        print(f"\n[Q_ID: {q.id}] {q.prompt}")
        for opt in q.options:
            print(f"   [{opt.id}] {opt.option_text}")

