import json
import re

with open('data/m5_analyzed.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('data/library_extracted/11_374 29.11.2001.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Helper to normalize text (latin/cyrillic basics, lower, punctuation)
def normalize(t):
    t = t.lower()
    # Cyrillic to latin map for uzbek
    charmap = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ҳ': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh',
        'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ў': 'o', 'қ': 'q', 'ғ': 'g'
    }
    res = []
    for c in t:
        if c in charmap:
            res.append(charmap[c])
        elif c.isalnum() or c.isspace():
            res.append(c)
        else:
            res.append(' ')
    return ' '.join(''.join(res).split())

# We want to match options against snippet or full_text around clause
results = []
for item in items:
    qnum = item['num']
    prompt = item['prompt']
    qid = item['qid']
    clause = item['clause']
    options = item['options']
    snippet = item['snippet']
    
    # If no snippet, search for clause or prompt words
    if not snippet:
        if qnum == 7:
            clause = "2.1.49"
            pos = full_text.find("2.1.49")
            snippet = full_text[pos:pos+400]
            
    norm_snippet = normalize(snippet) if snippet else ""
    
    # Score each option
    opt_scores = []
    for opt in options:
        opt_text = opt['optionText']
        norm_opt = normalize(opt_text)
        
        # Word overlap
        opt_words = [w for w in norm_opt.split() if len(w) > 2]
        matches = [w for w in opt_words if w in norm_snippet]
        score = len(matches) / max(1, len(opt_words))
        
        # Check phrase match
        if len(norm_opt) > 5 and norm_opt in norm_snippet:
            score += 2.0
            
        opt_scores.append((score, opt['id'], opt_text))
        
    opt_scores.sort(key=lambda x: x[0], reverse=True)
    best = opt_scores[0]
    
    results.append({
        "num": qnum,
        "qid": qid,
        "prompt": prompt,
        "clause": clause,
        "best_id": best[1],
        "best_text": best[2],
        "best_score": best[0],
        "runner_up": opt_scores[1] if len(opt_scores) > 1 else None,
        "options": options,
        "snippet": snippet[:200].replace('\n', ' ') if snippet else ""
    })

with open('data/m5_matched.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved data/m5_matched.json")
