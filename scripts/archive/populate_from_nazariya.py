import json
import re

with open('data/full_theory_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb.get('questions', {})
initial_count = len(kb_q)

def transliterate(text):
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ц': 's', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': "'",
        'ы': 'i', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ў': "o'", 'ғ': "g'", 'қ': 'q',
        'ҳ': 'h'
    }
    t = text.lower()
    return "".join(mapping.get(c, c) for c in t)

def clean(text):
    t = transliterate(text)
    t = re.sub(r"['’`ʼ\"]", "", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

new_verified = 0

for lvl in db.get('levels', []):
    for t in lvl.get('theories', []):
        # Build clean theory text for this specific theory
        theory_texts = [clean(s.get('content', '')) for s in t.get('nazariyaSections', []) if s.get('content')]
        full_theory = " ".join(theory_texts)
        
        for q in t.get('questions', []):
            qid = q.get('id')
            if qid in kb_q:
                continue
            
            # Check prompt and options
            best_opt = None
            for opt in q.get('options', []):
                opt_c = clean(opt.get('optionText', ''))
                # Exact phrase match in this theory's nazariya
                if len(opt_c) > 20 and opt_c in full_theory:
                    best_opt = opt
                    break
            
            if best_opt:
                kb_q[qid] = {
                    "correct_option_id": best_opt['id'],
                    "prompt": q['prompt'],
                    "option_text": best_opt['optionText'].strip()
                }
                new_verified += 1

print(f"Initial verified: {initial_count}")
print(f"Newly added from exact Nazariya matching: {new_verified}")
print(f"Total verified now: {len(kb_q)}")

with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)
print("Saved to data/knowledge_base.json")
