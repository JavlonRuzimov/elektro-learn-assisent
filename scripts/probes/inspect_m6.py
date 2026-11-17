import json

with open('data/all_500_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

m6 = [item for item in data if item.get('theoryId') == 'f1ede884-e103-481a-8642-c06f7480b0d6'][0]
questions = m6['questions']

print(f"Total questions in Module 6: {len(questions)}")
for i, q in enumerate(questions[:10]):
    print(f"=== Q{i+1}: {q.get('prompt')} (ID: {q.get('id')}) ===")
    for opt in q.get('options', []):
        print(f"  [{opt.get('id')}] {opt.get('optionText')}")
