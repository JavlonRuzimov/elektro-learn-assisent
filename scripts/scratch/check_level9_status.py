import sys
import os
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))
from api import ElektroLearnClient

client = ElektroLearnClient()
level_id = "7577259e-4295-4d5f-a504-69626ac29587"
lvl = client.progress.get_level_detail(level_id)
print(f"Level: {lvl.title} (Order: {lvl.order_index})")
for t in lvl.theories:
    print(f"  {t.title} ({t.id}): {t.answered_questions}/{t.total_questions} | Complete: {t.is_complete}")

me = client.base_client.get("/progress/me")
print(f"\nTotal XP: {me.get('totalXp')}")
print(f"Hearts: {me.get('hearts')}")
