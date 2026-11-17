from api import ElektroLearnClient

client = ElektroLearnClient()
level5_id = "f15546e6-82ac-4d89-ad78-b9ef37009aea"
detail = client.progress.get_level_detail(level5_id)

print(f"LEVEL 5: {detail.title}")
print(f"Jami modullar soni: {len(detail.theories)}")

for idx, t in enumerate(detail.theories, 1):
    print(f"\n==========================================")
    print(f"MODULE {idx}: {t.title} (ID: {t.id})")
    print(f"Savollar soni: {t.answered_questions}/{t.total_questions} (Tugallangan: {t.is_complete})")
    print(f"==========================================")
    q_data = client.progress.get_theory_questions(t.id, mode="continue")
    questions = q_data.get("questions", [])
    print(f"Yuklangan savollar soni: {len(questions)}")
    for q in questions:
        print(f"\n[Savol ID: {q.id}] {q.prompt}")
        for opt in q.options:
            print(f"   [{opt.id}] {opt.option_text}")

