from api import ElektroLearnClient
client = ElektroLearnClient()
prog = client.progress.get_progress()
for lvl in prog.levels:
    print(f"Level {lvl.order_index}: {lvl.title} -> {lvl.completion_percent}% ({lvl.correct_answers_count} to'g'ri)")

