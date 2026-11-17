import json
import re

with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('data/library_extracted/11_374 29.11.2001.txt', 'r', encoding='utf-8') as f:
    doc_text = f.read()

m5 = [item for item in data if item.get('theoryId') == '71854476-434f-4108-a439-73ac1e4b1b80'][0]
questions = m5['questions']

print(f"Total questions: {len(questions)}")

for i, q in enumerate(questions):
    prompt = q.get('prompt', '')
    qid = q.get('id')
    print(f"--- Q{i+1}: {prompt} ({qid}) ---")
    
    # Extract clause reference if any, e.g. (1.2.18) or (2.1.46)
    m = re.search(r'\(([\d\.]+)\)', prompt)
    clause = m.group(1) if m else None
    
    context = ""
    if clause:
        # Find clause in text
        pos = doc_text.find(clause)
        if pos != -1:
            context = doc_text[pos:pos+500].replace('\n', ' ')
            print(f"  [Found clause {clause}]: {context[:150]}...")
        else:
            print(f"  [Clause {clause} NOT found in text]")
    else:
        print(f"  [No clause in prompt]")
        
    for opt in q.get('options', []):
        print(f"    [{opt.get('id')}] {opt.get('optionText')}")
