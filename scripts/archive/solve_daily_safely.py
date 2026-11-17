from api.client import BaseClient
import time
import json
import os
import re

client = BaseClient()

# Load all library texts
library_texts = {}
lib_dir = 'data/library_extracted'
for fn in os.listdir(lib_dir):
    if fn.endswith('.txt'):
        with open(os.path.join(lib_dir, fn), 'r', encoding='utf-8', errors='ignore') as f:
            library_texts[fn] = f.read().lower()

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.split())

def find_verified_option(q):
    qid = q['id']
    options = q.get('options', [])
    
    # 1. Check knowledge base
    if qid in kb.get('questions', {}):
        opt_id = kb['questions'][qid].get('correctOptionId')
        if opt_id:
            return opt_id, "Found in Knowledge Base"
            
    # 2. Search library texts for exact option sentences
    best_opt = None
    best_match_info = ""
    
    # Check if an option has an exact unique phrase in the library
    matching_opts = []
    for opt in options:
        opt_id = opt['id']
        opt_text = (opt.get('text') or opt.get('optionText') or '').strip()
        cleaned_opt = clean_text(opt_text)
        if len(cleaned_opt) < 15:
            continue
            
        for fn, text in library_texts.items():
            # Check 30-char chunks or exact sentence
            if opt_text.lower() in text or cleaned_opt in clean_text(text):
                matching_opts.append((opt_id, opt_text, fn))
                break
                
    if len(matching_opts) == 1:
        return matching_opts[0][0], f"Exact match in {matching_opts[0][2]}: {matching_opts[0][1][:50]}"
        
    return None, None

def run_daily_plan():
    print("=== STARTING DAILY PLAN SOLVER ===")
    daily = client.get('/mobile/daily-plan/today')
    answered = daily.get('answeredCount', 0)
    correct = daily.get('correctCount', 0)
    completed = daily.get('completed', False)
    print(f"Current Daily Plan: {correct}/10 correct ({answered} answered), completed={completed}")
    
    while not completed and correct < 10:
        resp = client.get('/mobile/daily-plan/next-question')
        if resp.get('done') or resp.get('exhausted'):
            print("Daily plan indicates done or exhausted.")
            break
            
        q = resp.get('question')
        if not q:
            print("No question returned.")
            break
            
        qid = q['id']
        prompt = q.get('prompt', '')
        print(f"\n--- Question: {prompt[:70]}... ---")
        
        opt_id, info = find_verified_option(q)
        if not opt_id:
            print(f"WARNING: No 100% verified option found for QID={qid}!")
            print("Options were:")
            for o in q.get('options', []):
                print("  *", o.get('id'), o.get('text') or o.get('optionText'))
            print("STOPPING to avoid heart loss!")
            break
            
        print(f"Submitting verified option: {opt_id} ({info})")
        res = client.post("/progress/answer", data={
            "questionId": qid,
            "selectedOptionId": opt_id,
            "source": "DAILY_PLAN"
        })
        
        is_cor = res.get("isCorrect")
        hearts = res.get("hearts", {}).get("heartsCount")
        print(f"Result: isCorrect={is_cor} | Hearts remaining={hearts} | XP earned={res.get('xpEarned')}")
        
        if is_cor:
            kb.setdefault('questions', {})[qid] = {
                'correctOptionId': opt_id,
                'verified': True,
                'note': info
            }
            with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
                json.dump(kb, f, indent=2, ensure_ascii=False)
        else:
            print("ERROR: Answer marked incorrect! Halting immediately.")
            break
            
        time.sleep(1.5)
        daily = client.get('/mobile/daily-plan/today')
        correct = daily.get('correctCount', 0)
        completed = daily.get('completed', False)
        print(f"Daily Plan Progress: {correct}/10")

    final_daily = client.get('/mobile/daily-plan/today')
    print("\n=== FINAL DAILY PLAN STATUS ===")
    print(f"Answered: {final_daily.get('answeredCount')}/10 | Correct: {final_daily.get('correctCount')} | Completed: {final_daily.get('completed')}")

if __name__ == '__main__':
    run_daily_plan()
