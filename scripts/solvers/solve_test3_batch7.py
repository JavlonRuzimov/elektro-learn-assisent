import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Seventh batch of verified questions for Test 3
BATCH7_TEST3 = {
    # 1. Ish jarayonida brigada a’zolari ustidan nazorat kimga yukla-nadi?
    "9fbd3fca-928b-4c93-aaf6-084ef4d7973c": "f2c01151-36ca-488c-923d-0e47a367f3a8",
    # 2. Energetika ob’ektlaridagi yo‘riqnomalar, nizomlar, texnolo-gik va tezkor sxemalar ro‘yxati kim tomonidan tasdiqlanadi?
    "12497ae1-b174-4a46-8bbe-a991331d68a8": "bdb0742f-6523-4b23-81bb-f16681c2aead",
    # 3. Uskunalar ta’mirining sifati nimani hisobga olib baholana-di?
    "a3099b53-4f6d-4d72-8c48-baf2a1eaa29a": "4faac23b-b8e7-496b-89a8-3f8cc9fba6a5",
    # 4. 1000 Vgacha kuchlanishli elektr qurilmada farmoyish bilan ish bajarganda, ish bajaruvchi qisqa muddatga ish joyidan ketishi mum-kinmi?
    "c8c1b9ea-182d-41b9-a247-cd307e2b3733": "f33f7809-45d5-4371-9bee-9ad181f07ff4",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

for qid, opt_id in BATCH7_TEST3.items():
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
