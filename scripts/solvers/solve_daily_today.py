import sys
import os
import time
import json
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Load all 500 questions mapping as extra knowledge
try:
    with open("data/all_500_questions.json", encoding="utf-8") as f:
        all_500 = json.load(f)
except Exception:
    all_500 = []

def find_answer(q):
    # 1. Exact Question ID match in KB
    known = kb.get_known_answer(q.id)
    if known:
        for opt in q.options:
            if opt.id == known:
                return opt.id, f"KB exact ID match: {opt.option_text[:50]}"

    # 2. Match by exact prompt in KB
    for k_id, k_data in kb.data.get("questions", {}).items():
        k_prompt = k_data.get("prompt", "")
        if k_prompt and k_prompt.strip().lower() == q.prompt.strip().lower():
            k_opt_text = (k_data.get("option_text") or "").strip().lower()
            if k_opt_text:
                for opt in q.options:
                    if opt.option_text.strip().lower() == k_opt_text:
                        return opt.id, f"KB prompt match: {opt.option_text[:50]}"

    # 3. Fuzzy search in all_500_questions if option matches known KB answers
    for th in all_500:
        for item in th.get("questions", []):
            if item.get("prompt", "").strip().lower() == q.prompt.strip().lower():
                # Check which option of item is in KB
                for o in item.get("options", []):
                    c_opt = kb.get_known_answer(item.get("id"))
                    if c_opt == o.get("id"):
                        # Found matching text
                        target_text = (o.get("optionText") or o.get("text") or "").strip().lower()
                        for opt in q.options:
                            if opt.option_text.strip().lower() == target_text:
                                return opt.id, f"KB 500-question match: {opt.option_text[:50]}"

    return None, None

def run_daily_solver():
    print("=== STARTING DAILY PLAN SOLVER FOR 2026-11-18 ===")
    plan = client.daily_plan.get_today()
    print(f"Current Daily Plan: {plan.correct_count}/{plan.daily_goal_correct} correct, Completed: {plan.completed}")

    target = plan.daily_goal_correct or 10

    while plan.correct_count < target and not plan.completed:
        q = client.daily_plan.get_next_question()
        if not q:
            print("[INFO] No more daily questions returned.")
            break

        print(f"\n--- Question {plan.correct_count + 1}/{target} (Total Answered: {plan.answered_count}) ---")
        print(f"ID: {q.id}")
        print(f"Prompt: {q.prompt}")

        opt_id, info = find_answer(q)
        if not opt_id:
            print(f"[STOP] No verified answer found for: {q.prompt}!")
            print("Options:")
            for o in q.options:
                print(f"  [{o.id}] {o.option_text}")
            break

        print(f"Chosen Option: [{opt_id}] ({info})")

        res = client.progress.submit_answer(
            question_id=q.id,
            selected_option_id=opt_id,
            source="DAILY_PLAN"
        )

        print(f"Result: is_correct={res.is_correct}, XP earned={res.xp_earned}, Hearts={res.hearts}")

        if res.is_correct:
            opt_text = next((o.option_text for o in q.options if o.id == opt_id), "")
            kb.record_answer(q.id, q.prompt, opt_id, opt_text)
            print("-> Successfully recorded to Knowledge Base!")
        else:
            print(f"[ERROR] Answer incorrect! Server returned correctOptionId: {res.correct_option_id}")
            if res.correct_option_id:
                correct_text = next((o.option_text for o in q.options if o.id == res.correct_option_id), "")
                kb.record_answer(q.id, q.prompt, res.correct_option_id, correct_text)
            break

        solved += 1
        time.sleep(2.0)
        plan = client.daily_plan.get_today()

    print("\n=== FINAL DAILY PLAN STATUS ===")
    final_plan = client.daily_plan.get_today()
    print(f"Correct: {final_plan.correct_count}/{final_plan.daily_goal_correct} | Completed: {final_plan.completed}")
    me = client.base_client.get("/progress/me")
    print(f"Total XP: {me.get('totalXp')} | Hearts: {me.get('hearts')}")

if __name__ == "__main__":
    run_daily_solver()
