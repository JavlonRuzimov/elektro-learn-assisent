import sys
import os
import json
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))
from api import ElektroLearnClient

client = ElektroLearnClient()

# 1. Check user answer history or stats
try:
    stats = client.base_client.get("/progress/stats")
    print("Progress stats:", stats)
except Exception as e:
    print("Progress stats error:", e)

# 2. Check all levels from progress overview
prog = client.progress.get_progress()
print("\n=== LEVELS OVERVIEW ===")
for l in prog.levels:
    print(f"Level {l.order_index}: {l.title} (ID: {l.id}, Completed: {l.is_completed}, Locked: {l.is_locked})")

# 3. Check if any level has uncompleted theories
for l in prog.levels:
    try:
        detail = client.progress.get_level_detail(l.id)
        for t in detail.theories:
            if t.answered_questions < t.total_questions:
                print(f"  Unfinished theory in Level {l.order_index}: {t.title} ({t.answered_questions}/{t.total_questions})")
    except Exception as e:
        print(f"  Error reading level {l.order_index}:", e)

# 4. Check calendar days - see if past days have status or answers
try:
    cal = client.daily_plan.get_calendar()
    print("\n=== CALENDAR DAYS SUMMARY ===")
    working_days = [d for d in cal.get("days", []) if not d.get("isDayOff")]
    print(f"Total working days in month: {len(working_days)}")
    for d in working_days[:10]:
        print(f"  Date: {d.get('date')} | Goal: {d.get('goal')}")
except Exception as e:
    print("Calendar error:", e)
