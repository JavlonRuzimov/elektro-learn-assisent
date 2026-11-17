import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Ninth batch of verified questions for Test 3
BATCH9_TEST3 = {
    # 1. Xodimlar kaysi qoidalardan bilim sinovidan o‘tishlari kerak?
    "58a814aa-8b60-4a77-8f8d-d421470849d9": "c4bafa89-fe78-4d07-92cf-0ff0026ced31",
    # 2. 0,4 kV gacha kuchlanish ostida bo‘lgan uskunalardagi yong‘inni o‘chirishda xavfsiz masofa qancha?
    "7a1dc043-b1c1-4f8e-976d-631ca1d3bd5c": "a464e1a7-8665-42ca-8cf1-7ea054efb3ee",
    # 3. Texnik xizmat ko‘rsatish va rejali ta’mirlash hajmi nima bi-lan aniqlanadi?
    "19270c52-5e79-4983-adb5-18bd4fad9fac": "e8470283-9e6d-4e3c-944f-53d01293159c",
    # 4. Aholi yashamaydigan va yetib borish qiyin bo‘lgan hududlarda kuchlanishi 110 kV bo‘lgan tarmoqlarda havo tarmog‘i simidan yergacha bo‘lgan masofa qancha bo‘lishi kerak?
    "c921a254-93dc-4567-ad73-c3e2a8fd08b1": "c8c48c50-b057-499b-900e-3adfe1389228",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH9_TEST3.items():
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
