import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient

client = ElektroLearnClient()
me = client.base_client.get('/progress/me')
hearts = me.get('hearts', {})
print(f"User: {me.get('user', {}).get('firstName')} {me.get('user', {}).get('lastName')}")
print(f"Energy (hearts): {hearts.get('hearts')}/{hearts.get('maxHearts')}, next regen: {hearts.get('nextRegenAt')}")
print(f"Total XP: {me.get('stats', {}).get('totalScore')}")

print("\n--- Levels ---")
for lvl in me.get('levels', []):
    print(f"Level {lvl.get('levelNumber')}: {lvl.get('title')} (Status: {lvl.get('status')}, Passed: {lvl.get('isPassed')})")
    if lvl.get('levelNumber') == 8:
        detail = client.progress.get_level_detail(lvl.get('id'))
        print(f"  Level 8 theories ({len(detail.theories)} modules):")
        for i, t in enumerate(detail.theories):
            print(f"    {i+1}. {t.title}: {t.answered_questions}/{t.total_questions} questions (ID: {t.id}, is_completed: {t.is_completed})")
