import json
import sys
import os
import glob
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))

from agent.knowledge_base import KnowledgeBase
kb = KnowledgeBase()

# Search terms
queries = [
    ("navbatdan tashqari", ["muz paydo", "releli"]),
    ("ko‘chma yerga ulagich", ["25", "16", "ko‘ndalang"]),
    ("Brigada a’zosi nimaga javob beradi", ["a, b", "yo‘riqnoma"]),
    ("Naryad necha kunga uzaytirilishi mumkin", ["15 kalendar", "uzaytirilgan"])
]

print("=== CHECKING KB ===")
for qid, qdata in kb.data.get("questions", {}).items():
    p = qdata.get("prompt", "")
    opt = qdata.get("option_text", "")
    for term, _ in queries:
        if term.lower() in p.lower() or term.lower() in opt.lower():
            print(f"KB match for '{term}': ID={qid} | Prompt={p} | Opt={opt}")

print("\n=== CHECKING ALL_500 ===")
try:
    with open("c:/Users/Administrator/Desktop/ElektroLearn/data/all_500_questions.json", encoding="utf-8") as f:
        all_500 = json.load(f)
    for th in all_500:
        for q in th.get("questions", []):
            p = q.get("prompt", "")
            for term, _ in queries:
                if term.lower() in p.lower():
                    print(f"all_500 match '{term}': ID={q.get('id')} | Prompt={p}")
                    for o in q.get("options", []):
                        print(f"   Option: {o.get('id')} | {o.get('optionText') or o.get('text')}")
                    # check KB
                    if q.get('id') in kb.data.get("questions", {}):
                        print(f"   -> KB CORRECT: {kb.data['questions'][q.get('id')]}")
except Exception as e:
    print(e)

print("\n=== CHECKING LIBRARY (DOCS) ===")
lib_files = glob.glob("c:/Users/Administrator/Desktop/ElektroLearn/data/library_extracted/**/*.txt", recursive=True)
for lf in lib_files:
    try:
        with open(lf, encoding="utf-8") as f:
            content = f.read()
        for term, words in queries:
            if term.lower() in content.lower():
                idx = content.lower().find(term.lower())
                snippet = content[max(0, idx-100):min(len(content), idx+300)]
                print(f"\n--- Match in {os.path.basename(lf)} for '{term}' ---")
                print(snippet.replace("\n", " "))
    except Exception as e:
        pass
