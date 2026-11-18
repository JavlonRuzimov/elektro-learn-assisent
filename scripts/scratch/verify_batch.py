import json
import sys
import os
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

try:
    with open("c:/Users/Administrator/Desktop/ElektroLearn/data/all_500_questions.json", encoding="utf-8") as f:
        all_500 = json.load(f)
except:
    all_500 = []

full_db_theories = []
try:
    with open("c:/Users/Administrator/Desktop/ElektroLearn/data/full_theory_database.json", encoding="utf-8") as f:
        full_db_raw = json.load(f)
    for lvl in full_db_raw.get("levels", []):
        for th in lvl.get("theories", []):
            full_db_theories.append(th)
except:
    pass

q_prompts = [
    "Xodimlar texnik ekspluatatsiya kilish qoidalarini buzganligi uchun nima asosida javobgar xisoblanadi?",
    "10 kV gacha kuchlanish ostida bo‘lgan uskunadagi yong‘inni qaysi turdagi o‘t o‘chirgich bilan o‘chirish mumkin?",
    "Yong‘in xavfsizligi choralari haqidagi yo‘riqnomalar kim tomo-nidan tasdiqlanadi?",
    "Daraxtlar simlarga aganasa unga yakinlashish mumkinmi?"
]

for p in q_prompts:
    print(f"\n==========================================")
    print(f"Searching for: {p}")
    p_clean = p.lower().strip()
    
    # 1. Search in KB
    found_kb = False
    for k_id, k_val in kb.data.get("questions", {}).items():
        k_p = k_val.get("prompt", "").lower().strip()
        if p_clean in k_p or k_p in p_clean or (len(p_clean) > 15 and p_clean[:20] in k_p):
            print(f"  [KB FOUND] ID: {k_id}")
            print(f"    Prompt: {k_val.get('prompt')}")
            print(f"    CorrectOptId: {k_val.get('correctOptionId')}")
            print(f"    OptText: {k_val.get('option_text')}")
            found_kb = True
            
    # 2. Search in all_500
    for th in all_500:
        for q in th.get("questions", []):
            qp = q.get("prompt", "").lower().strip()
            if p_clean in qp or qp in p_clean or (len(p_clean) > 15 and p_clean[:20] in qp):
                print(f"  [ALL_500 FOUND] QID: {q.get('id')} in Theory: {th.get('title')}")
                # check if in KB
                if q.get('id') in kb.data.get("questions", {}):
                    c_id = kb.data["questions"][q.get('id')].get("correctOptionId")
                    print(f"    -> KB has answer for this 500q ID: {c_id}")
                    for opt in q.get("options", []):
                        if opt.get("id") == c_id:
                            print(f"    -> Text: {opt.get('optionText') or opt.get('text')}")
                            
    # 3. Search in full_db
    for th in full_db_theories:
        for q in th.get("questions", []):
            qp = q.get("prompt", "").lower().strip()
            if p_clean in qp or qp in p_clean or (len(p_clean) > 15 and p_clean[:20] in qp):
                print(f"  [FULL_DB FOUND] QID: {q.get('id')} in Theory: {th.get('title')}")
                if q.get('id') in kb.data.get("questions", {}):
                    c_id = kb.data["questions"][q.get('id')].get("correctOptionId")
                    print(f"    -> KB has answer for this FullDB ID: {c_id}")
                    for opt in q.get("options", []):
                        if opt.get("id") == c_id:
                            print(f"    -> Text: {opt.get('optionText') or opt.get('text')}")
