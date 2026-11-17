import json

with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

m5 = [item for item in data if item.get('theoryId') == '71854476-434f-4108-a439-73ac1e4b1b80'][0]
questions = m5['questions']

for i, q in enumerate(questions[:15]):
    print(f"=== Q{i+1}: {q.get('prompt')} (ID: {q.get('id')}) ===")
    for opt in q.get('options', []):
        print(f"  [{opt.get('id')}] {opt.get('optionText')}")
