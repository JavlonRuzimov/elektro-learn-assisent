import json
import re

with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('data/library_extracted/11_374 29.11.2001.txt', 'r', encoding='utf-8') as f:
    doc_text = f.read()

m5 = [item for item in data if item.get('theoryId') == '71854476-434f-4108-a439-73ac1e4b1b80'][0]
questions = m5['questions']

results = []

for idx, q in enumerate(questions):
    prompt = q.get('prompt', '')
    qid = q.get('id')
    options = q.get('options', [])
    
    # Try finding clause in parentheses
    m = re.search(r'\(([\d\.]+)\)', prompt)
    clause = m.group(1) if m else None
    
    text_snippet = ""
    if clause:
        # Search for clause
        matches = [m.start() for m in re.finditer(re.escape(clause), doc_text)]
        for pos in matches:
            # take around pos
            snippet = doc_text[max(0, pos-20):min(len(doc_text), pos+600)]
            text_snippet += "\n--- SNIPPET ---\n" + snippet
            
    results.append({
        "num": idx + 1,
        "qid": qid,
        "prompt": prompt,
        "clause": clause,
        "snippet": text_snippet,
        "options": options
    })

with open('data/m5_analyzed.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved data/m5_analyzed.json with 50 analyzed questions.")
