import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

new_entries = [
    ("a21a263c-32d3-45a8-aaf5-e3dade977f83", "cb70d9eb-69db-4a66-bb01-238c0292b2cb", "Farmoyish bilan ish bajarilayotganda brigadani boshqa ish joyiga o'tkazish rasmiylashtiriladimi?", "talab kilinmaydi"),
    ("b1c2af2e-1049-4842-84c8-a3b9d382739b", "8266dbfe-9830-47c2-8f61-988d35c73e59", "Ish jarayonida brigada azolaridan biri yoki bir nechasi ish joyidan vaqtincha ketishi mumkinmi?", "ish bajaruvchining ruxsati bilan mumkin"),
    ("2e7e3d5b-896b-41df-bd69-92407be2c48e", "c6653c71-8932-438d-aa78-cefed3afe77d", "Qaysi xolatda kuzatuvchi tayinlanishi kerak?", "elektr qurilmalarda mustaqil ishlash huquqiga ega bo'lmagan ishchilar brigadasi ustidan nazorat olib borish uchun kuzatuvchi tayinlanishi shart")
]

for qid, opt_id, prompt, text in new_entries:
    kb_q[qid] = {
        "correct_option_id": opt_id,
        "prompt": prompt,
        "option_text": text
    }

with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print(f"Saved {len(new_entries)} verified entries to knowledge_base.json! Total in KB: {len(kb_q)}")
