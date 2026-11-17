with open('data/library_extracted/09_608 18.10.2022.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'архив' in line.lower():
        start = max(0, idx - 4)
        end = min(len(lines), idx + 5)
        print(f"=== Paragraph at line {idx+1} ===")
        for i in range(start, end):
            print(f"{i+1}: {lines[i].strip()}")
