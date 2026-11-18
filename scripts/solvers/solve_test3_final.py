import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Complete final mapping for the last 5 questions of Test 3
FINAL_TEST3 = {
    # 1. 0,4 kVgacha kuchlanish ostida bo‘lgan uskunalardagi yong‘inni nima bilan o‘chirishga ruxsat beriladi?
    "b999ec0a-4237-404b-bb4e-3366343593d9": "ab71ecc3-fa4c-4ec2-9e1e-ad45bf30e2aa",
    # 2. Tok o‘tkazuvchi qismlarga yerga ulagichni qachon o‘rnatish kerak?
    "8daf7541-5062-4542-a03b-e4c148094c28": "36f1a846-549d-40bb-b48b-51ab4092758d",
    # 3. Ishida tanaffus bo‘lgan ta’mirlash va sozlash xodimlariga qachon mustaqil ishlashga ruxsat beriladi?
    "6db1d3be-9c8b-4226-98e6-6c8709c25320": "effded62-7cdc-4c6e-aa73-bc9e2bc73891",
    # 4. Qachon ish rahbari yoki ta’mirlash brigadasidan tayinlangan ish bajaruvchi ishga qo‘yuvchi vazifasini o‘rindoshlik yo‘li bilan baja-rishi mumkin?
    "e8513907-b31b-4276-8df0-f1bcac4747a2": "931f5eb3-a1b0-4410-aef1-e9a8a44015fe",
    # 5. 0,4 kVli havo tarmoqlarda simning eng salqi joyidan yergacha va yo‘lning qatnov qismigacha bo‘lgan masofa qancha bo‘lishi kerak?
    "ee0b3f5b-a746-4fb1-8ab4-1c6a1a769300": "1d947f93-2cc7-4651-ad73-d8066ec0e2cf",
}

theory_id = "4ba84c4d-61e3-49d7-bbfb-5d4f5a8bf10b"

def run():
    me = client.base_client.get("/progress/me")
    hearts = me.get("hearts", {}).get("heartsCount", 0)
    print(f"Current hearts: {hearts}")
    if hearts <= 0:
        print("[STOP] Hearts = 0. Waiting for regen.")
        return

    while True:
        prog = client.progress.get_theory_questions(theory_id)
        qs = prog.get("questions", [])
        remaining = prog.get("remaining_count", 0)
        answered = prog.get("answered_count", 0)
        total = prog.get("total_questions", 40)
        print(f"\nProgress: {answered}/{total} (Remaining: {remaining})")

        if remaining == 0 or len(qs) == 0:
            print("\n[MUVAFFAQIYAT!] Test № 3 TO'LIQ 100% YAKUNLANDI!")
            break

        # Find a question in FINAL_TEST3
        target_q = None
        target_opt = None
        for q in qs:
            if q.id in FINAL_TEST3:
                target_q = q
                target_opt = FINAL_TEST3[q.id]
                break

        if not target_q:
            print(f"[OGOHLANTIRISH] Hozirgi darchadagi savollar ro'yxatda yo'q!")
            for q in qs:
                print(f"  {q.id}: {q.prompt}")
            break

        print(f"\nSubmitting: {target_q.prompt[:60]}... -> Option: {target_opt}")
        res = client.progress.submit_answer(
            question_id=target_q.id,
            selected_option_id=target_opt,
            source="LESSON"
        )
        print(f"Result: is_correct={res.is_correct}, hearts={res.hearts}")
        if res.is_correct:
            kb.record_answer(target_q.id, target_q.prompt, target_opt, "Verified in Test 3 final")
        else:
            print(f"-> XATO! Server javobi: {res.correct_option_id}")
            break
        time.sleep(2.0)

if __name__ == "__main__":
    run()
