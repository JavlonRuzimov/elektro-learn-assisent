import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Second batch of verified questions for Test 3
BATCH2_TEST3 = {
    # 1. Hushsiz odam tanasida kanday o‘zgarishlar bo‘ladi?
    "91028322-9570-4267-b279-31b1eaca3926": "7c88de56-7a37-458f-91d4-d67dd48b9ddf",
    # 2. Maqsadli (joriy) yo‘riqnoma qanday xollarda o‘tkaziladi?
    "88e4964f-e5fd-4fc1-b2c8-74af2e27cfee": "e5d5e873-347b-431d-a200-5af5afcb6ca6",
    # 3. Izolyatsiyalovchi shtangalar nima uchun ishlatiladi?
    "062ea0d2-c6b3-437c-911d-9046a4ab5e2d": "fe21672a-9e8d-4e3e-9a58-25469596627e",
    # 4. Ishga qo‘yuvchi nimaga javob beradi?
    "ec100775-f46e-4df8-824d-8d07c56a89ca": "12c25962-6d8a-41ff-b086-a9639e033c71",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH2_TEST3.items():
    print(f"\nSubmitting answer for QID: {qid} with Option: {opt_id}...")
    res = client.progress.submit_answer(
        question_id=qid,
        selected_option_id=opt_id,
        source="LESSON"
    )
    print(f"Result: is_correct={res.is_correct}, hearts={res.hearts}")
    if res.is_correct:
        print("-> To'g'ri!")
        kb.record_answer(qid, f"Test 3 Q {qid}", opt_id, f"Option {opt_id}")
    else:
        print(f"-> XATO! To'g'ri javob: {res.correct_option_id}")
        break
    time.sleep(2.0)

prog = client.progress.get_theory_questions(theory_id)
print(f"\nTest 3 Status: {prog['answered_count']}/{prog['total_questions']} answered.")
