import sys
import os
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient

client = ElektroLearnClient()
prog = client.base_client.get("/progress/me")
print("totalXp in progress/me:", prog.get("totalXp"))
print("Badge:", prog.get("badge"))

total_correct = 0
for lvl in prog.get("levels", []):
    c = lvl.get("correctAnswersCount", 0)
    total_correct += c
    print(f"Level {lvl.get('orderIndex')}: {lvl.get('title')} -> Correct: {c}/{lvl.get('attemptsCount')} ({lvl.get('completionPercent')}%)")

print("Sum of correct answers across all levels:", total_correct)

# Check daily plan history or streak
dp = client.daily_plan.get_today()
print("\nDaily Plan Today:", dp.correct_count, "/", dp.daily_goal_correct, "Done:", dp.completed)
