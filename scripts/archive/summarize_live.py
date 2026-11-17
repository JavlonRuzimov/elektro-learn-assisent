import json

with open('data/current_live_state.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for det in data.get('level_details', []):
    lvl = det.get('level', {})
    theories = det.get('theories', [])
    total_q = sum(t.get('totalQuestionsCount', 0) for t in theories)
    total_answered = sum(t.get('answeredQuestionsCount', 0) for t in theories)
    total_correct = sum(t.get('correctAnswersCount', 0) for t in theories)
    print(f"Level order {lvl.get('orderIndex')}: '{lvl.get('title')}'")
    print(f"   Theories: {len(theories)} | Questions: {total_q} | Answered: {total_answered} | Correct: {total_correct}")
    for t in theories:
        t_tot = t.get('totalQuestionsCount', 0)
        t_ans = t.get('answeredQuestionsCount', 0)
        t_cor = t.get('correctAnswersCount', 0)
        t_title = t.get('title')
        print(f"     - {t_title[:40]}: {t_cor}/{t_tot} to'g'ri ({t_ans} javob berilgan)")
