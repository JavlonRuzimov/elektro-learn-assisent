import json
import re
import os

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

# Load all library texts
library_dir = 'data/library_extracted'
lib_files = {}
for fname in os.listdir(library_dir):
    if fname.endswith('.txt'):
        with open(os.path.join(library_dir, fname), 'r', encoding='utf-8', errors='ignore') as f:
            lib_files[fname] = clean(f.read())

print(f"Loaded {len(lib_files)} library files.")

with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    theories = json.load(f)

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)
kb_q = kb.get('questions', {})

found_exact = []
for t in theories:
    t_title = t.get('title')
    for q in t.get('questions', []):
        qid = q.get('id')
        if qid in kb_q:
            continue
        
        prompt_c = clean(q.get('prompt', ''))
        # find matching library file
        matching_file = None
        for fname, ftext in lib_files.items():
            # if 3 prompt words appear together
            p_words = [w for w in prompt_c.split() if len(w) > 4]
            if len(p_words) >= 3:
                count = sum(1 for w in p_words if w in ftext)
                if count / len(p_words) > 0.7:
                    matching_file = fname
                    break
        
        if matching_file:
            ftext = lib_files[matching_file]
            # Now check which option matches verbatim in ftext
            opt_matches = []
            for opt in q.get('options', []):
                opt_c = clean(opt.get('optionText', ''))
                if len(opt_c) > 25 and opt_c in ftext:
                    opt_matches.append(opt)
            
            if len(opt_matches) == 1:
                found_exact.append((q, opt_matches[0], matching_file))

print(f"Found {len(found_exact)} new questions with verbatim 100% exact option matches in library books!")
for q, opt, fname in found_exact[:10]:
    print(f"\n[Book: {fname}]")
    print(f"Q: {q['prompt'][:80]}...")
    print(f"-> Verbatim Exact Option: {opt['optionText'][:80]}...")
