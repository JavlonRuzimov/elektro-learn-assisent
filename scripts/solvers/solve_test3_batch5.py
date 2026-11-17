import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Fifth batch of verified questions for Test 3
BATCH5_TEST3 = {
    # 1. Kontaktsiz kuchlanish ko‘rsatkichini yerga ulash talab qilina-dimi?
    "b2904f8d-0ab2-4e21-b0db-2cc874a55426": "bf99057f-857a-4fb7-8a5b-2b12853b3e3b",
    # 2. Ish bajaruvchiga ishga qo‘yuvchi vazifasini bajarish tayin-langan hollarda naryadning ikkinchi nusxasi kimda qoladi?
    "9274e3a0-a03c-492c-8b88-e4078f755995": "0daee43b-932f-45ae-bd12-c2bad4ff0a31",
    # 3. Razryadlagich, ajratgich, chaqmoqdan ximoyalovchi tros, saqlagichlar va hokazolar o‘rnatilgan kuchlanishi 1 kV dan yuqori bo‘lgan tarmoqning yog‘och tayanchlarida o‘rnatiladigan yerlagich simining diametri qancha bo‘lishi kerak?
    "d0e33d1b-5d27-47a8-95ca-79706db28d42": "f81e8f5a-84cc-4c3a-b63c-9e050a9c195f",
    # 4. Uskunalarni ta’mirga chiqarish va ishga tushirish qaerda ko‘r-satilgan?
    "b694102a-dbe3-4a77-b3ed-4e144ec41a00": "727b7ef9-0b86-41cd-967c-81831d351988",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH5_TEST3.items():
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
