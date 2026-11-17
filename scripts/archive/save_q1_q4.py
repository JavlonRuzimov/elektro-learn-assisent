import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

new_entries = [
    ("31561321-a9eb-433b-88b7-ba35efbbc723", "9a93cdb0-351c-4bae-a027-145226a13b2b", "Naryad qaysi holatda yangidan berilishi lozim?", "ish rahbari yoki ish bajaruvchi almashtirilganda, yoki brigada tarkibi yarmidan ko'pga o'zgartirilsa"),
    ("4cfbf0e7-7124-4c88-a7af-12241f3a7611", "f333793a-318f-4b2a-a01c-4d409dbd3948", "Farmoyish nima?", "ishni xavfsiz bajarish uchun, uning mazmunini, ish joyini, vaqtini xavfsizlik choralarini (kerak bo'lgan taqdirda) va ishni bajarilishi top-shirilgan shaxslarni belgilovchi og'zaki topshiriq"),
    ("5ac80a0c-0ce8-426f-b011-533f1d07f294", "aa3a2494-5738-4c46-a29e-11d7bcc5c851", "Naryadning 2-jadvali qachon to'ldiriladi?", "ish joyini tayyorlashga va birinchi bor ishga qo'yishga ruxsat berilganda to'ldiriladi"),
    ("8d813f1e-fc72-41be-bf8a-631e6a244be1", "6f2b4a9d-e186-4b03-9771-2f2aaf3fb07b", "I va II guruh brigada azolari ish jarayonida taqsimlovchi qurilma joylashgan xonadan mustaqil chiqib ketishi mumkinmi?", "faqat III guruh brigada azosi yoki elektr qurilmani bir o'zi ko'rib, chiqish xuquqiga ega bo'lgan shaxslar hamroxligida chiqishlari va yana ish joyiga qaytarib kelishlari mumkin")
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
