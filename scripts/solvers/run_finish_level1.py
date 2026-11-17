import time
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase
from agent.solver import QuestionSolver

client = ElektroLearnClient()
kb = KnowledgeBase()
solver = QuestionSolver(kb)

level_id = "3ad50502-c9bf-462d-ba09-c870e96bd361"
detail = client.progress.get_level_detail(level_id)

print(f"=== {detail.title} NI 100% YAKUNLASH BOSHLANDI ===")

for t in detail.theories:
    print(f"\n>> Mavzu: {t.title} ({t.answered_questions}/{t.total_questions})")
    if t.is_complete:
        print("  Allaqaqon 100% bajarilgan.")
        continue

    # Get remaining questions
    q_data = client.progress.get_theory_questions(t.id, mode="continue")
    questions = q_data.get("questions", [])
    print(f"  Qolgan savollar: {len(questions)} ta")

    for q in questions:
        opt_id, conf, reason = solver.solve_single_choice(q, t.content)
        opt_text = next((o.option_text for o in q.options if o.id == opt_id), "")
        print(f"\n[Savol]: {q.prompt}")
        print(f"  Tanlangan javob: '{opt_text[:50]}' (Ishonch: {conf*100}%)")

        # Pacing
        time.sleep(2)

        res = client.progress.submit_answer(q.id, opt_id, source="LESSON")
        if res.is_correct:
            print(f"  [+] TO'G'RI! (+{res.xp_earned} XP, Hearts: {res.hearts})")
        else:
            print(f"  [-] Noto'g'ri! Server to'g'ri ID: {res.correct_option_id}")
            # Agar noto'g'ri bo'lsa darhol to'xtatamiz
            exit(1)

        time.sleep(1.5)

print("\n=== TEKSHIRUV: LEVEL 1 NATIJASI ===")
prog = client.progress.get_progress()
lvl1 = next((l for l in prog.levels if l.id == level_id), None)
if lvl1:
    print(f"Level nomi: {lvl1.title}")
    print(f"Holati: {'TUGALLANDI (100%)' if lvl1.is_completed else f'{lvl1.completion_percent}%'}")
    print(f"To'g'ri javoblar: {lvl1.correct_answers_count}/{lvl1.attempts_count}")

print("\nBarcha darajalar holati:")
for l in prog.levels:
    lock = "Qulf 🔒" if l.is_locked else "Ochiq 🔓"
    print(f"  - [{lock}] {l.title} ({l.completion_percent}%)")

