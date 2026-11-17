import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Check energy
me = client.base_client.get("/progress/me")
hearts = me.get("hearts", {})
cur_hearts = hearts.get("heartsCount", 0)
print(f"Current hearts: {cur_hearts}/5")
if cur_hearts <= 0:
    print("No hearts available. Stopping safely.")
    sys.exit(0)

# Verified answers map
VERIFIED_ANSWERS = {
    # 1. Ximoya vositalarini qayd qilish jurnali qancha muddatda va kim tomonidan nazorat qilinishi kerak?
    "3397d8c7-572f-4ebf-b310-c95ce8e2caef": "f417052c-044c-4f87-a2f8-bc2f084da557",
    # 2. Energetika ob’ektlarini normal ekspluatatsiya kilish uchun kim javobgar?
    "d09f0590-76d2-4b48-ae92-e52ba53457cf": "d5175f53-e48e-40fc-b6eb-9dfb566ea9a8",
    # 3. Havo elektr uzatish tarmoqlarini gabaritlari qanday asboblar yordamida o‘lchanadi?
    "d24614af-3daf-4e98-8984-b4632ce32c7b": "421d5540-cca3-4b42-80c2-d9cba235037f",
    # 4. Texnologik sxemalar (chizmalar) qancha muddatda tekshirilishi kerak?
    "62579c02-53bc-4de1-8af0-db8d5bca9ba7": "172d67c2-0840-4269-bb01-1c7546cf8a21"
}

theory_id = "62ff9db9-4545-4944-9a7b-27de8e31b522"
q_data = client.progress.get_theory_questions(theory_id, mode="continue")
questions = q_data["questions"]

print(f"Loaded {len(questions)} remaining questions in current batch")

for idx, q in enumerate(questions, 1):
    opt_id = VERIFIED_ANSWERS.get(q.id)
    if not opt_id:
        print(f"Question {q.id} not in VERIFIED_ANSWERS! Stopping to prevent heart loss.")
        break
    
    # Find option text
    opt_text = ""
    for opt in q.options:
        if opt.id == opt_id:
            opt_text = opt.option_text
            break
            
    print(f"\nSubmitting Q{idx}: {q.prompt[:60]}...")
    print(f"  Selected: [{opt_id}] {opt_text[:60]}...")
    
    res = client.progress.submit_answer(
        question_id=q.id,
        selected_option_id=opt_id,
        source="LESSON"
    )
    
    print(f"  Result: Correct={res.is_correct}, CorrectOpt={res.correct_option_id}, Hearts={res.hearts}")
    
    # Record to Knowledge Base immediately
    if res.is_correct:
        kb.record_answer(
            question_id=q.id,
            prompt=q.prompt,
            correct_option_id=opt_id,
            option_text=opt_text
        )
        print("  -> Saved to knowledge_base.json")
    else:
        print("  -> WARNING: Answer was NOT correct! Halting execution.")
        break
        
    time.sleep(2.5)

# Check next batch or progress
q_next = client.progress.get_theory_questions(theory_id, mode="continue")
print(f"\nAnswered: {q_next.get('answered_count')}/{q_next.get('total_questions')}, Remaining: {q_next.get('remaining_count')}")
me_after = client.base_client.get("/progress/me")
print("Hearts after batch:", me_after.get("hearts"))
