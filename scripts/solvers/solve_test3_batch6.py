import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Sixth batch of verified questions for Test 3
BATCH6_TEST3 = {
    # 1. Kuyishlar necha xil bo‘ladi?
    "e3ce76bb-dde6-4dff-96c3-33a0e17ecfe7": "c5de33e6-3094-404f-961b-a52aa86cfb6f",
    # 2. Ish bajaruvchi ishga qo‘yuvchi vazifasini o‘rindoshlik asosida bajarganda ish joyi qanday tayyorlanadi?
    "a58d1232-c3e4-4024-885f-25d494c9f0fc": "51b778ca-e4df-49f4-b8ed-9927075fb1d2",
    # 3. Ish bajaruvchi (kuzatuvchi) ish joyidan vaqtincha ketishi ke-rak bo‘lib qolsa uning o‘rniga kim qoladi?
    "5ec0a98c-18a6-44c2-b46e-f4901f8f1148": "1b847c9b-b18c-41c2-89d0-4f77b0b1079a",
    # 4. Yilning issiq va sovuq davrida jgut yoki buramani qancha vaqtga qo‘yish mumkin?
    "ca2bf2c0-ec86-4f39-9c63-b3178bdd47e3": "df7e7739-3e24-4cc1-9f83-3e14fa1e8260",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH6_TEST3.items():
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
