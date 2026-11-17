import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

# Newly verified questions
verified_list = [
    ("0282cf96-c26f-481f-a06f-18053869b57e", "02ade816-4c2f-478e-bc9d-cbfabb158a62", "Metrologik taminot bo'yicha ishlar bajarilishining nazora-tini kim amalga oshiradi?", "metrologiya xizmati"),
    ("a625c367-af45-44fa-a236-885841676db8", "3c1e92c9-ea7a-49ac-ac62-250d9792e453", "Energetik uskunalar jixozlarini boshqarish, texnik xizmat ko'r-satish yoki tamirlashga kimga ruxsat etiladi?", "maxsus tayyorgallik kursini o'tgan va tegishli lavozimda ishlash uchun atestatsiyadan o'tgan shaxslarga ijozat beriladi"),
    ("bc23dc26-a23f-4653-b0b0-6db6ec89e43e", "c75077c6-4aa1-4a71-9eeb-d15f43cc026f", "Qaysi vaqtdan boshlab uskuna tamirdan keyin ishga tushi-rilgan hisoblanadi?", "ekspluatatsiya qiluvchi tashkilot tomonidan tamirlash ishlari tugatil-ganligi to'g'risida xabar berilganidan, uni tarmoqqa ulanganidan, tezkor talabnoma yopilganidan so'ng uskuna tamirlashdan ishga kiritilgan deb xisoblanadi"),
    ("c713b80a-65d5-4896-94ec-5d01f6d2cffc", "c38eff36-7c47-4892-aa01-b89a96f45e1c", "Qachon elektr tarmoqlarida kompleks sinab ko'rish o'tkazilgan xisoblanadi?", "podstantsiya uskunalarini 72 soat davomida, elektr uzatish liniyalarini esa 24 soat davomida yuklama ostida normal va uzluksiz ishlashi xisoblanadi"),
    ("ef9b05c9-bc0a-4862-915f-cf5efff54d7b", "e50acbb9-e0d0-42c8-ad32-b8b006b634e2", "Ishlab turgan havo tarmoqlari va havo aloqa tarmoqlari ustidan o'tgan havo tarmoqlarining tayanchlari orasidagi simlarda nech-ta ulanmaga ruxsat etiladi?", "2 ta")
]

for qid, opt_id, prompt, opt_text in verified_list:
    kb_q[qid] = {
        "correct_option_id": opt_id,
        "prompt": prompt,
        "option_text": opt_text
    }

with open('data/knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(verified_list)} verified answers into knowledge_base.json!")
print(f"Total verified in KB now: {len(kb_q)}")
