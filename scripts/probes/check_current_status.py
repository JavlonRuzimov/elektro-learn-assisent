from api.client import BaseClient
import json

client = BaseClient()
me = client.get('/progress/me')
hearts = me.get('hearts', {})
levels = me.get('levels', [])
daily = client.get('/mobile/daily-plan/today')

print('=== HEARTS ===')
print(f"Count: {hearts.get('heartsCount')} / {hearts.get('maxHearts')}")
print(f"Next Regen: {hearts.get('nextRegenAt')}")
print(f"Last Regen: {hearts.get('lastHeartRegenAt')}")

print('\n=== USER & XP ===')
print(f"Total XP: {me.get('totalXp')}")
print(f"Badge: {me.get('badge')}")

print('\n=== DAILY PLAN ===')
print(f"Answered: {daily.get('answeredCount')} / 10")
print(f"Correct: {daily.get('correctCount')}")
print(f"Wrong: {daily.get('wrongCount')}")
print(f"Completed: {daily.get('completed')}")

print('\n=== LEVELS ===')
for l in levels:
    order = l.get('orderIndex')
    title = l.get('title')
    pct = l.get('completionPercent')
    cor = l.get('correctAnswersCount')
    att = l.get('attemptsCount')
    done = l.get('isCompleted')
    locked = l.get('isLocked')
    print(f"Level {order}: \"{title}\" -> {pct}% | To'g'ri: {cor} (Urinishlar: {att}) | Done: {done} | Locked: {locked}")

# Check Level 8 theory breakdown
lvl8_id = 'f15546e6-82ac-4d89-ad78-b9ef37009aea'
try:
    l8_det = client.get(f'/progress/level/{lvl8_id}')
    theories = l8_det.get('theories', [])
    print('\n=== LEVEL 8 THEORIES BREAKDOWN ===')
    for t in theories:
        t_title = t.get('title')
        ans = t.get('answeredQuestionsCount')
        tot = t.get('totalQuestionsCount')
        cor = t.get('correctAnswersCount')
        pct = t.get('progress')
        print(f"  - {t_title[:45]}: {cor}/{tot} to'g'ri ({ans} yechilgan, {pct}%)")
except Exception as e:
    print('Level 8 detail error:', e)
