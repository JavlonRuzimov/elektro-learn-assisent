import json
import sys
import os
import time
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Load all 500 questions for broader search
try:
    with open("c:/Users/Administrator/Desktop/ElektroLearn/data/all_500_questions.json", encoding="utf-8") as f:
        all_500 = json.load(f)
except:
    all_500 = []

# Load full theory database - flatten to list of theories with questions
full_db_theories = []
try:
    with open("c:/Users/Administrator/Desktop/ElektroLearn/data/full_theory_database.json", encoding="utf-8") as f:
        full_db_raw = json.load(f)
    for lvl in full_db_raw.get("levels", []):
        for th in lvl.get("theories", []):
            full_db_theories.append(th)
except:
    pass

THEORY_ID = "2f06c650-af5b-485a-84d6-8987e18bff02"

def find_answer_in_kb(q):
    """Search KB and all_500 for a known answer, return (option_id, source_info) or (None, None)"""
    
    # 1. Exact question ID match in KB
    for k_id, k_data in kb.data.get("questions", {}).items():
        if k_id == q.id:
            opt_id = k_data.get("correctOptionId")
            if opt_id:
                for opt in q.options:
                    if opt.id == opt_id:
                        return opt.id, f"KB exact ID: {opt.option_text[:50]}"

    # 2. Match by prompt text in KB
    q_prompt = q.prompt.strip().lower()
    for k_id, k_data in kb.data.get("questions", {}).items():
        k_prompt = k_data.get("prompt", "").strip().lower()
        if k_prompt and k_prompt == q_prompt:
            k_opt_text = (k_data.get("option_text") or "").strip().lower()
            if k_opt_text:
                for opt in q.options:
                    if opt.option_text.strip().lower() == k_opt_text:
                        return opt.id, f"KB prompt match: {opt.option_text[:50]}"
    
    # 3. Fuzzy prompt match in KB (substring)
    for k_id, k_data in kb.data.get("questions", {}).items():
        k_prompt = k_data.get("prompt", "").strip().lower()
        if k_prompt and len(k_prompt) > 20:
            # Check if prompts are similar enough
            if q_prompt in k_prompt or k_prompt in q_prompt:
                k_opt_text = (k_data.get("option_text") or "").strip().lower()
                if k_opt_text:
                    for opt in q.options:
                        if opt.option_text.strip().lower() == k_opt_text:
                            return opt.id, f"KB fuzzy match: {opt.option_text[:50]}"

    # 4. Search in all_500_questions
    for th in all_500:
        for item in th.get("questions", []):
            item_prompt = item.get("prompt", "").strip().lower()
            if item_prompt == q_prompt or (len(item_prompt) > 20 and (q_prompt in item_prompt or item_prompt in q_prompt)):
                item_id = item.get("id")
                # Check if this item_id has a known answer in KB
                for k_id2, k_data2 in kb.data.get("questions", {}).items():
                    if k_id2 == item_id:
                        correct_opt = k_data2.get("correctOptionId")
                        # Find the text of correct option in item
                        correct_text = ""
                        for o in item.get("options", []):
                            if o.get("id") == correct_opt:
                                correct_text = (o.get("optionText") or o.get("text") or "").strip().lower()
                                break
                        if correct_text:
                            for opt in q.options:
                                if opt.option_text.strip().lower() == correct_text:
                                    return opt.id, f"500q match: {opt.option_text[:50]}"
    
    # 5. Search in full_theory_database
    for th in full_db_theories:
        for item in th.get("questions", []):
            item_prompt = item.get("prompt", "").strip().lower()
            if item_prompt == q_prompt or (len(item_prompt) > 20 and (q_prompt in item_prompt or item_prompt in q_prompt)):
                item_id = item.get("id")
                for k_id2, k_data2 in kb.data.get("questions", {}).items():
                    if k_id2 == item_id:
                        correct_opt = k_data2.get("correctOptionId")
                        correct_text = ""
                        for o in item.get("options", []):
                            if o.get("id") == correct_opt:
                                correct_text = (o.get("optionText") or o.get("text") or "").strip().lower()
                                break
                        if correct_text:
                            for opt in q.options:
                                if opt.option_text.strip().lower() == correct_text:
                                    return opt.id, f"FullDB match: {opt.option_text[:50]}"

    return None, None


def run():
    me = client.base_client.get("/progress/me")
    hearts = me.get("hearts", {}).get("heartsCount", 0)
    total_xp = me.get("totalXp", 0)
    print(f"=== TEST 4 SOLVER START ===")
    print(f"Hearts: {hearts}/5 | XP: {total_xp}")

    submitted = 0
    skipped = []

    while True:
        prog = client.progress.get_theory_questions(THEORY_ID)
        answered = prog.get("answered_count", 0)
        remaining = prog.get("remaining_count", 0)
        total = prog.get("total_questions", 40)
        qs = prog.get("questions", [])

        print(f"\nProgress: {answered}/{total} (Remaining: {remaining})")

        if remaining == 0 or len(qs) == 0:
            print("\n[YAKUNLANDI] Test 4 100% COMPLETED!")
            break

        # Check hearts
        me = client.base_client.get("/progress/me")
        hearts = me.get("hearts", {}).get("heartsCount", 0)
        if hearts <= 1:
            print(f"[STOP] Hearts critically low: {hearts}. Stopping to preserve energy.")
            break

        found_q = None
        found_opt = None
        found_info = None

        for q in qs:
            opt_id, info = find_answer_in_kb(q)
            if opt_id:
                found_q = q
                found_opt = opt_id
                found_info = info
                break

        if not found_q:
            print(f"[STOP] No verified answer found for any question in current window.")
            for q in qs:
                print(f"  UNMATCHED: {q.id} | {q.prompt[:70]}")
                for o in q.options:
                    print(f"    [{o.id}] {o.option_text[:80]}")
            break

        print(f"Submitting Q{answered+1}: {found_q.prompt[:60]}...")
        print(f"  Answer: [{found_opt}] ({found_info})")

        res = client.progress.submit_answer(
            question_id=found_q.id,
            selected_option_id=found_opt,
            source="LESSON"
        )

        print(f"  Result: correct={res.is_correct}, XP+={res.xp_earned}, Hearts={res.hearts}")
        
        if res.is_correct:
            opt_text = next((o.option_text for o in found_q.options if o.id == found_opt), "")
            kb.record_answer(found_q.id, found_q.prompt, found_opt, opt_text)
            submitted += 1
        else:
            print(f"  [XATO!] Server javobi: {res.correct_option_id}")
            if res.correct_option_id:
                correct_text = next((o.option_text for o in found_q.options if o.id == res.correct_option_id), "")
                kb.record_answer(found_q.id, found_q.prompt, res.correct_option_id, correct_text)
                print(f"  Recorded correct answer to KB: {correct_text[:60]}")

        time.sleep(2.0)

    # Final status
    print("\n=== FINAL STATUS ===")
    final_prog = client.progress.get_theory_questions(THEORY_ID)
    me = client.base_client.get("/progress/me")
    print(f"Test 4: {final_prog.get('answered_count')}/{final_prog.get('total_questions')}")
    print(f"Total XP: {me.get('totalXp')} | Hearts: {me.get('hearts')}")
    print(f"Submitted: {submitted}")

if __name__ == "__main__":
    run()
