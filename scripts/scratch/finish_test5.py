import sys
import os
import time
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

THEORY_ID = "007a32c2-6b88-44eb-8444-3bb7e831142f"

FINAL_4_MAPPING = {
    # 1. Navbatdan tashqari ko'rik
    "1aa93822-455f-4769-9d03-0a84540e8708": "0730ac9f-56ba-446c-97c7-00ba341886c6",
    # 2. Ko'chma yerga ulagichlar kesimi (25 mm2 va 16 mm2)
    "76d7342a-be0f-4783-b680-0c15c18bb6d6": "57a04ba8-0596-438d-ac6a-bd824baf98a7",
    # 3. Brigada a'zosi nimaga javob beradi (a, b va g to'g'ri)
    "f23853a7-0787-4761-b834-d13c1745711e": "20d89f77-da51-4b85-bd74-18a07fdbce80",
    # 4. Naryad necha kunga uzaytirilishi mumkin (15 kalendar kuni)
    "24c82789-afe6-45df-a09c-ea742f3b08b2": "adda4ff6-6459-42b3-bc1c-3b0e3c3c5cad"
}

def run():
    me = client.base_client.get("/progress/me")
    hearts = me.get("hearts", {}).get("heartsCount", 0)
    print(f"=== FINISHING TEST 5 (Last 4 questions) ===")
    print(f"Hearts: {hearts}/5 | XP: {me.get('totalXp')}")

    prog = client.progress.get_theory_questions(THEORY_ID)
    qs = prog.get("questions", [])
    print(f"Questions to solve: {len(qs)}")

    for q in qs:
        if q.id in FINAL_4_MAPPING:
            opt_id = FINAL_4_MAPPING[q.id]
            print(f"\nSubmitting for Q ID {q.id}: {q.prompt[:60]}...")
            print(f"  Selected Option: {opt_id}")

            res = client.progress.submit_answer(
                question_id=q.id,
                selected_option_id=opt_id,
                source="LESSON"
            )

            print(f"  Result: correct={res.is_correct}, XP+={res.xp_earned}, Hearts={res.hearts}")
            
            if res.is_correct:
                opt_text = next((o.option_text for o in q.options if o.id == opt_id), "")
                kb.record_answer(q.id, q.prompt, opt_id, opt_text)
            else:
                print(f"  [CRITICAL ERROR] Server expected: {res.correct_option_id}")
                break

            time.sleep(2.0)
        else:
            print(f"Unknown question ID: {q.id}")
            break

    # Final verification
    print("\n=== FINAL TEST 5 STATUS ===")
    final_prog = client.progress.get_theory_questions(THEORY_ID)
    me = client.base_client.get("/progress/me")
    print(f"Test 5: {final_prog.get('answered_count')}/{final_prog.get('total_questions')}")
    print(f"Total XP: {me.get('totalXp')} | Hearts: {me.get('hearts')}")

if __name__ == "__main__":
    run()
