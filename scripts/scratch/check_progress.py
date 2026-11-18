import sys
import os
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))
from api import ElektroLearnClient

client = ElektroLearnClient()
prog = client.progress.get_progress()

print(f"Total XP: {prog.total_xp} | Completed levels count: {prog.completed_levels}")
for l in prog.levels:
    print(f"Level {l.order_index}: {l.title} | Completed={l.is_completed} | Locked={l.is_locked} | ID={l.id}")
