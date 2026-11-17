import json
import glob
import os

with open("data/test1_all_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

docs = {}
for path in glob.glob("data/library_extracted/*.txt"):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        docs[os.path.basename(path)] = f.read()

print(f"Loaded {len(docs)} library documents.")

verified_map = {}
unmatched = []

for idx, q in enumerate(questions, 1):
    q_id = q["id"]
    prompt = q["prompt"]
    options = q["options"]
    
    # Try to find exact matches for each option in the documents
    best_opt = None
    best_source = None
    best_count = 0
    
    # Check each option
    for opt in options:
        opt_text = opt["option_text"].strip()
        if len(opt_text) < 10:
            continue
            
        # Clean opt text for search (remove leading dot or dash)
        clean_text = opt_text.lstrip(". -–—").strip()
        
        # Check in all docs
        for doc_name, text in docs.items():
            if clean_text.lower() in text.lower():
                best_opt = opt
                best_source = doc_name
                best_count += 1
                break
        if best_opt:
            break
            
    if best_opt:
        verified_map[q_id] = {
            "prompt": prompt,
            "option_id": best_opt["id"],
            "option_text": best_opt["option_text"],
            "source": best_source
        }
    else:
        unmatched.append(q)

print(f"\nExact library matches found: {len(verified_map)} / {len(questions)}")
print(f"Unmatched remaining: {len(unmatched)}")

with open("data/test1_verified_matches.json", "w", encoding="utf-8") as f:
    json.dump(verified_map, f, ensure_ascii=False, indent=2)

with open("data/test1_unmatched.json", "w", encoding="utf-8") as f:
    json.dump(unmatched, f, ensure_ascii=False, indent=2)

print("\nSample verified matches (first 5):")
for k, v in list(verified_map.items())[:5]:
    print(f"- Prompt: {v['prompt'][:60]}...")
    print(f"  Answer: {v['option_text'][:60]}... ({v['source']})")
