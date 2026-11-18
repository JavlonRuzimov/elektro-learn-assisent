import glob
import re

files = glob.glob("c:/Users/Administrator/Desktop/ElektroLearn/data/library_extracted/**/*.txt", recursive=True)

for fpath in files:
    with open(fpath, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    for m in re.finditer(r"1000\s*v.*?25\s*mm", text, re.IGNORECASE):
        idx = m.start()
        print(f"[{fpath}]:")
        print(text[max(0, idx-50):min(len(text), idx+300)].replace("\n", " "))
        print("-" * 50)
    for m in re.finditer(r"ko[\'ʻʼ]?chma\s+yerga\s+ulagich.*?kesim", text, re.IGNORECASE):
        idx = m.start()
        print(f"[{fpath} kesim]:")
        print(text[max(0, idx-50):min(len(text), idx+300)].replace("\n", " "))
        print("-" * 50)
