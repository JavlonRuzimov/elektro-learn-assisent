import sys, os
sys.path.insert(0, os.path.abspath('.'))
from api import ElektroLearnClient

client = ElektroLearnClient()
level_id = 'f15546e6-82ac-4d89-ad78-b9ef37009aea'
detail = client.progress.get_level_detail(level_id)
theories = detail.theories

for idx, m in enumerate(theories):
    t_id = m.id
    t_title = m.title
    t_q = client.progress.get_theory_questions(t_id, mode='continue')
    tot = t_q.get('total_questions')
    ans = t_q.get('answered_count')
    rem = t_q.get('remaining_count')
    comp = t_q.get('is_module_complete')
    print(f"Module {idx+1}: {t_title}")
    print(f"  ID: {t_id}")
    print(f"  Progress: {ans}/{tot} (Remaining: {rem}) | Complete: {comp}")
