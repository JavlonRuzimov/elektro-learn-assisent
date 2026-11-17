from api import ElektroLearnClient

client = ElektroLearnClient()
level4_id = "ea8b4c9c-5e96-43fd-b54e-a58fce05717a"
detail = client.progress.get_level_detail(level4_id)

for idx, t in enumerate(detail.theories, 1):
    print(f"\n==========================================")
    print(f"MODULE {idx}: {t.title} (ID: {t.id})")
    print(f"Progress: {t.answered_questions}/{t.total_questions}")
    print(f"==========================================")
    q_data = client.progress.get_theory_questions(t.id, mode="continue")
    questions = q_data.get("questions", [])
    print(f"Yuklangan savollar soni: {len(questions)}")
    for q in questions:
        print(f"\n[Savol ID: {q.id}] {q.prompt}")
        for opt in q.options:
            print(f"   [{opt.id}] {opt.option_text}")

