import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Tenth batch of verified questions for Test 3
BATCH10_TEST3 = {
    # 1. Ishida tanaffus bo‘lgan ta’mirlash va sozlash xodimlariga qachon mustaqil ishlashga ruxsat beriladi?
    "6db1d3be-9c8b-4226-98e6-6c8709c25320": "effded62-7cdc-4c6e-aa73-bc9e2bc73891",
    # 2. Yong‘inni o‘chirish tezkor varaqalarini kim tasdiqlaydi?
    "6d7d2d79-95a5-46f1-8851-16dce4a28d1a": "188b9cc6-4eca-47d7-8058-9251c8ea3639",
    # 3. 0,4 kVli havo tarmoqlarda simning eng salqi joyidan yergacha va yo‘lning qatnov qismigacha bo‘lgan masofa qancha bo‘lishi kerak?
    "ee0b3f5b-a746-4fb1-8ab4-1c6a1a769300": "1d947f93-2cc7-4651-ad73-d8066ec0e2cf",
    # 4. Qachon ish rahbari yoki ta’mirlash brigadasidan tayinlangan ish bajaruvchi ishga qo‘yuvchi vazifasini o‘rindoshlik yo‘li bilan baja-rishi mumkin?
    "e8513907-b31b-4276-8df0-f1bcac4747a2": "931f5eb3-a1b0-4410-aef1-e9a8a44015fe",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

def run_batch():
    me = client.base_client.get("/progress/me")
    hearts = me.get("hearts", {}).get("heartsCount", 0)
    if hearts <= 0:
        print(f"[STOP] Hearts = {hearts}. Waiting for heart regeneration.")
        return

    for qid, opt_id in BATCH10_TEST3.items():
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

if __name__ == "__main__":
    run_batch()
