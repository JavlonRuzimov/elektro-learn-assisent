import json
import sys
import os
import time
import re
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

THEORY_ID = "007a32c2-6b88-44eb-8444-3bb7e831142f"

# Known verified answers specific to Test 5
KNOWN_ANSWERS = {
    # Razryadlagichlar qanday vazifani bajaradi?
    "e7e386bd-cf1c-42a7-b10c-51c479e45e19": "18f9a0b7-3502-40d9-aeb7-fdc8731b4f9b",
    # Xodimlar texnik ekspluatatsiya kilish qoidalarini buzganligi uchun nima asosida javobgar xisoblanadi?
    "7ba266fe-3f15-4267-9156-4987023d4c0e": "8e43f9f2-2564-4acf-a350-41eab1f4516a",
    # 10 kV gacha kuchlanish ostida bo‘lgan uskunadagi yong‘inni qaysi turdagi o‘t o‘chirgich bilan o‘chirish mumkin?
    "0681766f-971e-48cf-b774-3421b4c6d1fb": "eb219eb2-6815-47bd-be7f-2aefb306f712",
    # Yong‘in xavfsizligi choralari haqidagi yo‘riqnomalar kim tomo-nidan tasdiqlanadi?
    "538df022-b8f9-4ea1-9b83-ffb5772c0f73": "5f3b9712-d179-4071-b3c8-e8d44710b9c3",
    # Daraxtlar simlarga aganasa unga yakinlashish mumkinmi?
    "4053fd5e-86ef-46c5-992e-cb24869ed0f9": "7f048139-f0d1-46a5-a9b4-7ea69f889d89",
}

# Load all 500 questions for broader search
try:
    with open("c:/Users/Administrator/Desktop/ElektroLearn/data/all_500_questions.json", encoding="utf-8") as f:
        all_500 = json.load(f)
except:
    all_500 = []

# Load full theory database
full_db_theories = []
try:
    with open("c:/Users/Administrator/Desktop/ElektroLearn/data/full_theory_database.json", encoding="utf-8") as f:
        full_db_raw = json.load(f)
    for lvl in full_db_raw.get("levels", []):
        for th in lvl.get("theories", []):
            full_db_theories.append(th)
except:
    pass

def normalize_text(text):
    if not text:
        return ""
    # remove special quotes, hyphens, punctuation
    t = text.lower()
    t = re.sub(r"[\‘\’\'\`\"\-\—\–\,\.\?\!\:\;]", " ", t)
    return " ".join(t.split())

def find_answer(q):
    # 0. Manual known mapping
    if q.id in KNOWN_ANSWERS:
        opt_id = KNOWN_ANSWERS[q.id]
        for opt in q.options:
            if opt.id == opt_id:
                return opt.id, f"Manual Verified: {opt.option_text[:50]}"

    # 1. Exact question ID match in KB
    for k_id, k_data in kb.data.get("questions", {}).items():
        if k_id == q.id:
            opt_id = k_data.get("correctOptionId")
            if opt_id:
                for opt in q.options:
                    if opt.id == opt_id:
                        return opt.id, f"KB exact ID: {opt.option_text[:50]}"

    q_prompt = q.prompt.strip().lower()
    q_norm = normalize_text(q.prompt)

    # 2. Match by normalized prompt text in KB
    for k_id, k_data in kb.data.get("questions", {}).items():
        k_prompt = k_data.get("prompt", "").strip().lower()
        k_norm = normalize_text(k_prompt)
        if k_norm and (k_norm == q_norm or (len(q_norm) > 25 and (q_norm in k_norm or k_norm in q_norm))):
            k_opt_text = (k_data.get("option_text") or "").strip().lower()
            k_opt_norm = normalize_text(k_opt_text)
            if k_opt_norm:
                for opt in q.options:
                    opt_norm = normalize_text(opt.option_text)
                    if opt_norm == k_opt_norm or (len(k_opt_norm) > 15 and (k_opt_norm in opt_norm or opt_norm in k_opt_norm)):
                        return opt.id, f"KB prompt match: {opt.option_text[:50]}"

    # 3. Search in all_500_questions
    for th in all_500:
        for item in th.get("questions", []):
            item_prompt = item.get("prompt", "").strip().lower()
            item_norm = normalize_text(item_prompt)
            if item_norm and (item_norm == q_norm or (len(q_norm) > 25 and (q_norm in item_norm or item_norm in q_norm))):
                item_id = item.get("id")
                if item_id in kb.data.get("questions", {}):
                    correct_opt = kb.data["questions"][item_id].get("correctOptionId")
                    correct_text = ""
                    for o in item.get("options", []):
                        if o.get("id") == correct_opt:
                            correct_text = o.get("optionText") or o.get("text") or ""
                            break
                    if correct_text:
                        c_norm = normalize_text(correct_text)
                        for opt in q.options:
                            opt_norm = normalize_text(opt.option_text)
                            if opt_norm == c_norm or (len(c_norm) > 15 and (c_norm in opt_norm or opt_norm in c_norm)):
                                return opt.id, f"500q match: {opt.option_text[:50]}"

    # 4. Search in full_theory_database
    for th in full_db_theories:
        for item in th.get("questions", []):
            item_prompt = item.get("prompt", "").strip().lower()
            item_norm = normalize_text(item_prompt)
            if item_norm and (item_norm == q_norm or (len(q_norm) > 25 and (q_norm in item_norm or item_norm in q_norm))):
                item_id = item.get("id")
                if item_id in kb.data.get("questions", {}):
                    correct_opt = kb.data["questions"][item_id].get("correctOptionId")
                    correct_text = ""
                    for o in item.get("options", []):
                        if o.get("id") == correct_opt:
                            correct_text = o.get("optionText") or o.get("text") or ""
                            break
                    if correct_text:
                        c_norm = normalize_text(correct_text)
                        for opt in q.options:
                            opt_norm = normalize_text(opt.option_text)
                            if opt_norm == c_norm or (len(c_norm) > 15 and (c_norm in opt_norm or opt_norm in c_norm)):
                                return opt.id, f"FullDB match: {opt.option_text[:50]}"

    return None, None


def run():
    me = client.base_client.get("/progress/me")
    hearts = me.get("hearts", {}).get("heartsCount", 0)
    total_xp = me.get("totalXp", 0)
    print(f"=== TEST 5 SOLVER START ===")
    print(f"Hearts: {hearts}/5 | XP: {total_xp}")

    submitted = 0

    while True:
        prog = client.progress.get_theory_questions(THEORY_ID)
        answered = prog.get("answered_count", 0)
        remaining = prog.get("remaining_count", 0)
        total = prog.get("total_questions", 40)
        qs = prog.get("questions", [])

        print(f"\nProgress: {answered}/{total} (Remaining: {remaining})")

        if remaining == 0 or len(qs) == 0:
            print("\n[YAKUNLANDI] Level 9 Test 5 100% COMPLETED!")
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
            opt_id, info = find_answer(q)
            if opt_id:
                found_q = q
                found_opt = opt_id
                found_info = info
                break

        if not found_q:
            print(f"[PAUSE] No verified answer found for questions in current window:")
            for q in qs:
                print(f"  UNMATCHED: {q.id} | {q.prompt}")
                for o in q.options:
                    print(f"    [{o.id}] {o.option_text}")
            break

        print(f"Submitting Q{answered+1}: {found_q.prompt[:65]}...")
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
                print(f"  Recorded correct answer to KB: {correct_text}")
            break

        time.sleep(2.0)

    # Final status
    print("\n=== CURRENT / FINAL STATUS ===")
    final_prog = client.progress.get_theory_questions(THEORY_ID)
    me = client.base_client.get("/progress/me")
    print(f"Test 5: {final_prog.get('answered_count')}/{final_prog.get('total_questions')}")
    print(f"Total XP: {me.get('totalXp')} | Hearts: {me.get('hearts')}")
    print(f"Submitted in this session: {submitted}")

if __name__ == "__main__":
    run()
