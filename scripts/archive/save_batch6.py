import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

new_entries = [
    ("4d30f829-898d-4a9a-b286-6282ebdbc5b5", "0bf4fdbe-2ce4-46c5-bca0-38e58ef8fbca", "Kesilayotgan daraxtni ag'natmasdan ishdagi tanaffusga chi-qish mumkinmi?", "man etiladi"),
    ("039d7189-2191-4d4b-b54e-07c7608fa941", "4fd132ed-34f7-41a7-a19b-d63ca086757f", "Qachon ish rahbari yoki tamirlash brigadasidan tayinlangan ish bajaruvchi ishga qo'yuvchi vazifasini o'rindoshlik yo'li bilan baja-rishi mumkin?", "havo liniyalarda kommutatsion apparatda operatsiya bajarmasdan ish joyi-ni tayyorlashda, faqat kuchlanish yo'qligini tekshirish va ko'chma erga ulagich-larni o'rnatish kerak bo'lgan hollarda"),
    ("26abac3a-b2a0-41a1-b183-ae53dda0cb66", "e80494c9-7697-4ab9-8844-4dbaea29289e", "Ish kuni tugashi tufayli ishdagi tanaffusda naryad kimda qoldiriladi?", "ishga qo'yuvchiga topshiradi, u yo'q bo'lgan taqdirda esa, naryadni maxsus ajratilgan joyda, masalan amaldagi naryadlar jildiga solib qoldirishi shart"),
    ("b8a6285a-9848-48aa-9847-91a11072e604", "55c6d61e-71f6-4dc1-8086-3c4f1e155749", "Ish bajaruvchi raxbarlik qilayotgan brigada azosining guru-hi nechanchi bo'lishi kerak ?", "II guruhga ega bo'lishi shart")
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
