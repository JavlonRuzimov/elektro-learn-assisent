import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# First batch of verified questions for Test 3
BATCH1_TEST3 = {
    # 1. Ish joyida birlamchi yo‘riqnoma kimlar bilan o‘tkaziladi?
    "03088b4e-60de-437e-931f-73621ca1847c": "fce4fd85-f243-4530-8d86-5961e4f5207a",
    # 2. Ishga qo‘yuvchi ishga qo‘yishdan oldin nima qilishi kerak?
    "fdf35456-37ce-45b6-bf9c-199a5e6a0ef6": "c977899d-ba2f-4be4-94ea-d06b468911be",
    # 3. Ish bajaruvchi nimaga javob beradi?
    "4a1fb12a-2891-493b-8c9e-c0bbe36238cf": "d38d8d68-74e9-4f1b-80aa-9d7f01e5a0ce",
    # 4. Ta’mirlashni boshlashdan oldin kim uskunalar, bino va insho-otlarning nuqsonlarini aniqlaydi?
    "381a57f4-52ce-451c-86d6-cb7c481114b0": "e9a007f4-9a28-4166-9cd5-7e4746933629",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH1_TEST3.items():
    # Submit answer
    print(f"\nSubmitting answer for QID: {qid} with Option: {opt_id}...")
    res = client.progress.submit_answer(
        question_id=qid,
        selected_option_id=opt_id,
        source="LESSON"
    )
    print(f"Result: is_correct={res.is_correct}, hearts={res.hearts}")
    if res.is_correct:
        print("-> To'g'ri!")
    else:
        print(f"-> XATO! To'g'ri javob: {res.correct_option_id}")
        break
    time.sleep(2.0)

prog = client.progress.get_theory_questions(theory_id)
print(f"\nTest 3 Status: {prog['answered_count']}/{prog['total_questions']} answered.")
