import json

with open('data/m5_matched.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('data/library_extracted/11_374 29.11.2001.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

def show_q(num):
    item = items[num - 1]
    clause = item['clause']
    print(f"==================================================")
    print(f"Q{num}: {item['prompt']}")
    print(f"Clause: {clause}")
    
    # print context from text
    if clause:
        pos = full_text.find(clause)
        if pos != -1:
            print("\n--- CLAUSE TEXT ---")
            print(full_text[pos:pos+700])
            print("-------------------\n")
    print("OPTIONS:")
    for opt in item['options']:
        print(f"  [{opt['id']}] {opt['optionText']}")

import sys
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        show_q(int(arg))
else:
    for i in range(1, 11):
        show_q(i)
