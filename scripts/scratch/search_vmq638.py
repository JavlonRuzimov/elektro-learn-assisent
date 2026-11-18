import re

with open("c:/Users/Administrator/Desktop/ElektroLearn/data/library_extracted/12_638 09.10.2020.txt", encoding="utf-8") as f:
    text = f.read()

print("=== BRIGADA A'ZOSI ===")
for m in re.finditer(r"brigada\s+a[\'ʻʼ]zos[ia]", text, re.IGNORECASE):
    idx = m.start()
    print(text[max(0, idx-50):min(len(text), idx+300)].replace("\n", " "))
    print("=" * 40)

print("\n=== KO'CHMA YERGA ULAGICH ===")
for m in re.finditer(r"ko[\'ʻʼ]?chma\s+yerga", text, re.IGNORECASE):
    idx = m.start()
    print(text[max(0, idx-50):min(len(text), idx+300)].replace("\n", " "))
    print("=" * 40)
