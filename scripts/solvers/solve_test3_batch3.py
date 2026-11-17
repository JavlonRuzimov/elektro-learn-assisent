import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Third batch of verified questions for Test 3
BATCH3_TEST3 = {
    # 1. Naryad bo‘yicha ishga qo‘yish qaerda amalga oshiriladi?
    "2c8ded8c-c8fb-4fc2-a46b-f5a1feba945d": "857c9d7c-8d26-462b-bc3f-02337b97055f",
    # 2. Ta’mirlashning kaysi turlariga uzoq muddatli va yillik gra-fiklar tuziladi?
    "2da2b7ae-61bd-415f-a465-8f152e3777c9": "e8cfd72d-74d0-4774-9c51-5494cbf24424",
    # 3. Izolyatsiyalovchi dastakli chilangarlik yig‘uv asboblari qancha kuchlanish bilan sinaladi?
    "2b97f1f8-79ab-442b-a2f4-24c14a1aa596": "d739698c-b2b6-4d42-a974-6d62cb90d3a6",
    # 4. Energetika ob’ektlarida xodimlarning texnik ekspluatatsiya qilish qoidalari talablariga rioya qilishlari uchun kim javobgar hisoblanadi?
    "d822bf53-a6fb-4f62-bee4-ae5dca21845d": "d4a2770e-1d92-4180-9f8b-27a682f850ff",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH3_TEST3.items():
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
