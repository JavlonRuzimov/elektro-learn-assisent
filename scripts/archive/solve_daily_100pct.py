from api.client import BaseClient
import time
import json

client = BaseClient()

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb.get('questions', {})
print(f"Loaded knowledge base with {len(kb_q)} questions.")

daily = client.get('/mobile/daily-plan/today')
correct = daily.get('correctCount', 0)
answered = daily.get('answeredCount', 0)
completed = daily.get('completed', False)

print(f"Daily Plan initial: {correct}/10 correct ({answered} answered), completed={completed}")

attempts = 0
max_attempts = 150

while correct < 10 and not completed and attempts < max_attempts:
    attempts += 1
    resp = client.get('/mobile/daily-plan/next-question')
    if resp.get('done') or resp.get('exhausted'):
        print("Daily plan done or exhausted.")
        break
        
    q = resp.get('question')
    if not q:
        time.sleep(1)
        continue
        
    qid = q.get('id')
    prompt = q.get('prompt', '')
    
    # Check if known in KB
    known_entry = kb_q.get(qid)
    if not known_entry:
        # Skip to next question without answering
        time.sleep(0.3)
        continue
        
    correct_opt_id = known_entry.get('correct_option_id') or known_entry.get('correctOptionId')
    
    # Ensure correct_opt_id is present in current options
    opt_ids = [opt.get('id') for opt in q.get('options', [])]
    if correct_opt_id not in opt_ids:
        print(f"Option ID {correct_opt_id} not in options for QID={qid}, skipping.")
        time.sleep(0.3)
        continue
        
    print(f"\n[Attempt {attempts}] Found 100% verified question in KB!")
    print(f"  Prompt: {prompt[:65]}...")
    print(f"  Submitting option: {correct_opt_id}")
    
    time.sleep(1.2)
    res = client.post('/progress/answer', data={
        'questionId': qid,
        'selectedOptionId': correct_opt_id,
        'source': 'DAILY_PLAN'
    })
    
    is_cor = res.get('isCorrect')
    hearts = res.get('hearts', {}).get('heartsCount')
    xp = res.get('xpEarned')
    print(f"  Result: isCorrect={is_cor} | Hearts={hearts} | XP={xp}")
    
    if not is_cor:
        print("  CRITICAL: Server returned False for known answer! Halting!")
        break
        
    time.sleep(1.0)
    daily = client.get('/mobile/daily-plan/today')
    correct = daily.get('correctCount', 0)
    answered = daily.get('answeredCount', 0)
    completed = daily.get('completed', False)
    print(f"  Daily Plan Progress: {correct}/10 correct ({answered} answered)")

print("\n=== FINAL DAILY PLAN STATUS ===")
final_daily = client.get('/mobile/daily-plan/today')
print(f"Correct: {final_daily.get('correctCount')}/10 | Answered: {final_daily.get('answeredCount')} | Completed: {final_daily.get('completed')}")
