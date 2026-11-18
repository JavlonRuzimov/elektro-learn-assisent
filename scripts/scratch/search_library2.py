import glob
import re

queries = [
    "ko‘chma yerga ulagich",
    "kochma yerga ulagich",
    "Brigada a’zosi",
    "Brigada azosi",
    "javob beradi"
]

files = glob.glob("c:/Users/Administrator/Desktop/ElektroLearn/data/library_extracted/**/*.txt", recursive=True)
files += glob.glob("c:/Users/Administrator/Desktop/ElektroLearn/data/*.json")

for fpath in files:
    if fpath.endswith(".txt"):
        with open(fpath, encoding="utf-8", errors="ignore") as f:
            text = f.read()
            for q in queries:
                matches = [m.start() for m in re.finditer(re.escape(q), text, re.IGNORECASE)]
                for m in matches[:3]:
                    print(f"[{fpath}] match '{q}':")
                    print(text[max(0, m-80):min(len(text), m+200)].replace("\n", " "))
                    print("-" * 50)
