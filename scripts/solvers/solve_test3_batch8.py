import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Eighth batch of verified questions for Test 3
BATCH8_TEST3 = {
    # 1. Yog‘och tayanchga 1 ta ulama qism (pasinka)ni maxkamlashda bandaj qanday va qaerga qilinadi?
    "7635a3b7-e2c9-4f0c-9066-32e7d59f0934": "c3e3a90f-046e-4676-ba6d-c912449a428f",
    # 2. Qachon ish rahbari yoki ta’mirlash brigadasidan tayinlangan ish bajaruvchi ishga qo‘yuvchi vazifasini o‘rindoshlik yo‘li bilan baja-rishi mumkin?
    "e8513907-b31b-4276-8df0-f1bcac4747a2": "931f5eb3-a1b0-4410-aef1-e9a8a44015fe",
    # 3. 0,4 kV gacha kuchlanish ostida bo‘lgan uskunalardagi yong‘inni o‘chirishda xavfsiz masofa qancha?
    "7a1dc043-b1c1-4f8e-976d-631ca1d3bd5c": "a464e1a7-8665-42ca-8cf1-7ea054efb3ee",
    # 4. Tok o‘tkazuvchi qismlarga yerga ulagichni qachon o‘rnatish kerak?
    "8daf7541-5062-4542-a03b-e4c148094c28": "36f1a846-549d-40bb-b48b-51ab4092758d",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH8_TEST3.items():
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
