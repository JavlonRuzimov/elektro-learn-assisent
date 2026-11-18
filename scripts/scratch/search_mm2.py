import glob
import re

files = glob.glob("c:/Users/Administrator/Desktop/ElektroLearn/data/library_extracted/**/*.txt", recursive=True)

for fpath in files:
    with open(fpath, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    for m in re.finditer(r"(?:16|25|35)\s*mm[2²]", text, re.IGNORECASE):
        idx = m.start()
        print(f"[{fpath}]:")
        print(text[max(0, idx-80):min(len(text), idx+150)].replace("\n", " "))
        print("-" * 50)
