import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

new_entries = [
    ("1c904160-0f60-40eb-ab77-c2f63a74ae6c", "c284c3f8-f7d5-45c3-9467-850f3ab78764", "Kabel liniyasining muhofaza zonasida ish bajarish uchun berilgan ruxsatnomada nima ko'rsatilishi kerak?", "kabel liniyasining joylashishi va yotgan chuqurligi ko'psatilishi shart"),
    ("ad789671-0a8c-4fd0-ba1d-54823feac108", "54742e62-52e6-4f99-b6d6-fa9ca438657e", "Ish joyini tayyorlovchi shaxs nimaga javob beradi?", "naryadda ko'rsatilgan ish joyini tayyorlash bo'yicha, shuningdek ish sharoitlari bo'yicha talab qilinayotgan choralarni (qulflarni, plakatlarni to'siqlarni o'rnatish va sh.o'.) to'g'ri va aniq bajarilishiga javob beradi"),
    ("1f29b15b-66aa-4a2e-8b75-0c79e1652e2e", "7139360a-396f-46ac-a450-8b04e55b044f", "Qanday xodim ish rahbari bo'lishi mumkin?", "ish rahbari qilib V guruhga ega bo'lgan muxandis-texnik xodimlar tayin-lanishi shart"),
    ("303ad782-eada-40b8-8df3-b44cc8bc99aa", "48eaba8d-6673-45f9-9cf4-221cba8ea61a", "Elektrostantsiya va podstantsiya elektr qurilmalarini yakka o'zi ko'rib chiqish xuquqi kimlarga beriladi ?", "navbatchi yoki tezkor-tamirlash xodimlaridan bo'lgan elektr xavfsizligi bo'yicha III dan kam bo'lmagan guruhga ega xizmatchi yoki V guruhga ega bo'lgan mamuriy-texnik xodim, yoxud korxona raxbariyati bir o'zi ko'rikdan o'tkazi-shi mumkin")
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
