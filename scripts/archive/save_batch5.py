import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

new_entries = [
    ("c81c4a4e-b48e-45cd-b760-68eca56cfbf3", "89a928ff-4634-4da5-a05e-7ba2e13bb5c5", "Noelektrotexnik xodimlar elektrostantsiya va podstantsiya-ning elektr qurilmalarini ko'rib chiqish yoki ekskursiyasi qanday tash-kil qilinadi ?", "korxona rahbariyatining ruxsati bilan bir o'zi ko'rib chiqish huquqiga ega bo'lgan IV guruhga mansub xodim nazorati ostida amalga oshirilishi mumkin"),
    ("fcdad520-b683-41b2-8b13-0a5b2ddaa273", "841a17f0-4c10-476e-817c-676400ab6ebd", "Tayanchning detallarini almashtirishda nimaning oldi oli-nishi kerak?", "uning qulashi yoki qo'zg'alishini oldini olinishi shart"),
    ("284bc2ef-922b-433c-85c7-2af870f3a3bf", "ed958b12-e08e-4eac-b24c-b9f92f269499", "Brigada azolari soni va uning tarkibi nimaga asosan belgi-lanadi?", "ularning elektr xavfsizligi bo'yicha guruhlarini hisobga olgan holda ish bajarish sharoitlariga, hamda brigada azolari ustidan ish bajaruvchining (kuzatuvchining) nazoratini taminlash imkoniyatiga qarab belgilanadi"),
    ("a6baefcd-75b9-4d13-a874-5b1e2d77ff57", "39bdca65-d3af-4991-abbf-5592d9597d58", "Daraxtni to'liq kesmasdan ag'darish mumkinmi?", "daraxtni malum qismini chopmasdan yoki arralamasdan yiqitish, shuning-dek, butunlay arralab ag'natish taqiqlanadi")
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
