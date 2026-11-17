import json
import re
import os

with open('data/full_theory_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)
kb_questions = kb.get('questions', {})

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

# Collect all theory sections text
all_theory_corpus = []
for lvl in db.get('levels', []):
    for t in lvl.get('theories', []):
        for s in t.get('nazariyaSections', []):
            content = s.get('content', '')
            if content:
                all_theory_corpus.append(clean(content))

full_corpus_text = " ".join(all_theory_corpus)

# Also load library extracted texts
library_dir = 'data/library_extracted'
lib_corpus = []
if os.path.exists(library_dir):
    for fname in os.listdir(library_dir):
        if fname.endswith('.txt'):
            with open(os.path.join(library_dir, fname), 'r', encoding='utf-8', errors='ignore') as f:
                lib_corpus.append(clean(f.read()))

full_lib_text = " ".join(lib_corpus)

total = 0
exact_kb = 0
exact_theory = 0
exact_lib = 0
unmatched = 0

for lvl in db.get('levels', []):
    for t in lvl.get('theories', []):
        for q in t.get('questions', []):
            total += 1
            qid = q.get('id')
            if qid in kb_questions:
                exact_kb += 1
                continue
            
            matched = False
            # Check options against theory
            for opt in q.get('options', []):
                opt_c = clean(opt.get('optionText', ''))
                if len(opt_c) > 15 and opt_c in full_corpus_text:
                    exact_theory += 1
                    matched = True
                    break
            
            if not matched:
                for opt in q.get('options', []):
                    opt_c = clean(opt.get('optionText', ''))
                    if len(opt_c) > 20 and opt_c in full_lib_text:
                        exact_lib += 1
                        matched = True
                        break
            
            if not matched:
                unmatched += 1

print(f"Total questions: {total}")
print(f"1. Verified in Knowledge Base (100%): {exact_kb}")
print(f"2. Exact phrase in Nazariya sections: {exact_theory}")
print(f"3. Exact phrase in Library documents: {exact_lib}")
print(f"4. Needs intelligent semantic matching: {unmatched}")
print(f"High-confidence coverage: {(exact_kb + exact_theory + exact_lib)/total*100:.1f}%")
