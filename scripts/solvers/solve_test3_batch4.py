import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Fourth batch of verified questions for Test 3
BATCH4_TEST3 = {
    # 1. Uskunalarning davriy ko‘rikdan o‘tkazilishi kim tomonidan amalga oshiriladi?
    "44a00b06-c04e-4657-a037-0253fc9c8713": "1ed15e33-9ab7-4b4c-8dbb-e47759668860",
    # 2. Jabrlanuvchi 6-10 kV tok o‘tkazuvchi qismdan ajratilganda uni shu maydondan qancha masofaga olib chiqish kerak?
    "96e9d130-1fbf-4da7-bfda-5ab72ffe50bb": "f76ae7eb-dcf5-42cc-9f6c-5e67dd14ab72",
    # 3. Ish bajaruvchiga (kuzatuvchiga) va ishga qo‘yuchiga nechta naryad yoki farmoyish berilishi mumkin?
    "9d366839-1791-4c09-8504-25254aebd3aa": "7784e036-840b-4536-9088-301cff1f9775",
    # 4. Yong‘inni o‘chirish tezkor varaqalari nima maqsadda ishlab chi-qiladi?
    "4da098c3-419e-45c5-9de4-21b0720d1d7f": "e00c8ffe-c613-4330-af07-dffaf50d1708",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH4_TEST3.items():
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
