import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb['questions']['e9cb7b98-7a44-4110-8909-9a0b49ccb950'] = {
    'correct_option_id': '7f0500db-e9eb-48b5-aa9f-43b77cd230f0',
    'prompt': 'Ish joyini tayyorlovchi shaxs nimaga javob beradi?   ',
    'option_text': "naryadda ko'rsatilgan ish joyini tayyorlash bo'yicha, shuningdek ish sharoitlari bo'yicha talab qilinayotgan choralarni (qulflarni, plakatlarni to'siqlarni o'rnatish va sh.o'.) to'g'ri va aniq bajarilishiga ja¬vob beradi."
}

with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print('Corrected knowledge base entry successfully!')
