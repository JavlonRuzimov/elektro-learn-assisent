import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

new_entries = [
    ("1e452076-36d2-4f09-b92a-368c60e82b2b", "cc51187d-1651-4973-89d5-eededf231511", "1000 Vdan yuqori kuchlanishli havo liniyasida uzilib erda yotgan simga qancha masofaga yaqinlashish mumkin emas?", "8 metrdan kam masofaga yaqinlashish taqiqlanadi"),
    ("4babddd9-d26d-43d6-b297-a7d4965eaf95", "7ab15d07-2737-4884-bd33-30a242e4fc93", "Ushlab va tortib turuvchi ko'p zanjirli izolyatsiyalovchi osma-larda ishlaganda ximoya kamarining arqonini qaerga mahkamlash man qilinadi?", "ish bajarrilayotgan shodaga mahkamlash man qilinadi"),
    ("67e17b59-b14e-4694-beda-312d75832c3b", "974ebb42-d1c4-4ee4-848a-032396745dd8", "Kabel liniyalarining muhofaza zonalarida er kazish ishla-rini boshlashdan oldin nima kilish kerak?", "kabel liniyalarini ekspluatatsiya qiluvchi xodim nazorati ostida kabel-larning joylashishi va chuqurligini aniqlash uchun, tekshirib ko'rish maqsa-dida er yuzasi ochilishi, shuningdek er qazish mashinalarini ishlash maydo-nini belgilab qo'yish uchun vaqtinchalik to'siqlar o'rnatilishi lozim"),
    ("51dddb1f-038a-4303-b4ef-2b4be209d71f", "5d21ef39-65ce-449f-b0e6-5b81595024d2", "Ishlashda ish joyini tayyorlash uchun kuchlanishni olish talab qilinsa, qaysi texnik tadbirlar bajariladi ?", "Zarur bo'lgan o'chirishlar amalga oshirilishi va kommutatsion apparatlar-ning o'z-o'zidan yoki yanglishib ulanishiga to'sqinlik qiluvchi choralar ko'rili-shi, kommutatsion apparatlarning qo'l bilan boshqariladigan yuritmalariga va masofadan boshqariladigan kalitlariga taqiqlovchi plakatlar osilishi, odamlarni elektr toki bilan jarohatlanishdan saqlash uchun erga ulanishi zarur bo'lgan tok o'tkazuvchi qismlarda kuchlanish yo'qligi tekshirilishi; erga ulagichlar o'rnatilishi (erga ulagich pichoqlarini ulash, ko'chma erga ulagich-larni o'rnatish); zarur bo'lganda ish joylarini yoki kuchlanish ostida qolgan boshqa tok o'tkazuvchi qismlarni to'sish va to'siqlarga xavfsizlik plakatlari osilishi. Mahalliy sharoitlarga qarab o'chirilgan tok o'tkazuvchi qismlar erga ulanishdan oldin yoki keyin to'siqlar bilan ajratiladi")
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
