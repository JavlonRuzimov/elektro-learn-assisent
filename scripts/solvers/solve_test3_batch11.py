import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Eleventh batch of verified questions for Test 3
BATCH11_TEST3 = {
    # 1. Yong‘inni o‘chirish tezkor varaqalarini kim tasdiqlaydi?
    "6d7d2d79-95a5-46f1-8851-16dce4a28d1a": "188b9cc6-4eca-47d7-8058-9251c8ea3639",
    # 2. Montyorning saqlagich kamarlari va xavfsizlik arqonlari qanday sinovlardan o‘tkaziladi?
    "059719af-a80c-43d2-9fb2-b812eff57988": "fd971108-42f1-4782-bbb2-3bda6a54a60e",
    # 3. Tok o‘tkazuvchi qismlarga yerga ulagichni qachon o‘rnatish kerak?
    "8daf7541-5062-4542-a03b-e4c148094c28": "36f1a846-549d-40bb-b48b-51ab4092758d",
    # 4. 0,4 kVli havo tarmoqlarda simning eng salqi joyidan yergacha va yo‘lning qatnov qismigacha bo‘lgan masofa qancha bo‘lishi kerak?
    "ee0b3f5b-a746-4fb1-8ab4-1c6a1a769300": "1d947f93-2cc7-4651-ad73-d8066ec0e2cf",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH11_TEST3.items():
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
