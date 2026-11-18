import glob
import json

queries = ["ko‘ndalang kesimi", "ko'ndalang kesimi", "ko'ndalang kesim", "ko‘ndalang kesim"]

for path in glob.glob("c:/Users/Administrator/Desktop/ElektroLearn/data/**/*.json", recursive=True):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        text = json.dumps(data, ensure_ascii=False)
        for q in queries:
            if q.lower() in text.lower():
                print(f"Found in {path} for {q}")
                idx = 0
                while True:
                    idx = text.lower().find(q.lower(), idx)
                    if idx == -1:
                        break
                    print(text[max(0, idx-80):min(len(text), idx+200)])
                    print("="*40)
                    idx += len(q)
    except:
        pass
