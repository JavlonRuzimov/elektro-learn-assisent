import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_q = kb['questions']

new_entries = [
    ("ef19f8bf-e360-48a1-92bd-ba237dde4c5d", "7f5b6ec8-79b7-42af-a17a-f6273d661c79", "Ish bajaruvchi ish joyini tayyorligini kim bilan birga tek-shiradi?", "ish raxbari yoki ishga qo'yuvchi bilan birga tekshirishi shart"),
    ("c6908938-4b55-4818-9fc4-517f3891b181", "2a92d0bb-e34d-466e-bb2e-a43d89d6fec4", "Agar ishlar avtomobillar, mexanizmlar, o'zi yurar kranlar-ni qo'llab bajariladigan bo'lsa, naryadning «Brigada azolari bilan» degan qatorlariga nima yozilishi kerak?", "brigada azolaridan kim haydovchi, kranchi, yuk iluvchi ekani ko'psatilishi hamda ishlatilayotgan mexanizmning yoki o'zi yurar kranning turi ko'psatili-shi zarur"),
    ("39b0f30e-f9aa-4461-8587-faadba315ae5", "d4520233-9117-4b5c-b7ad-532d9fe96989", "Ko'chma erga ulagichlarni qaerga o'rnatish man qilinadi?", "tasodifiy tuproq uyumlariga"),
    ("6f9d9e97-b1d5-476d-adc8-785a9bfad98a", "57497f6b-8024-40f3-8c44-7862886d47d9", "Ish raxbari tayinlanmay bajariladigan ishlarda naryad-ning “Ish raxbariga” deb ko'rsatilgan qatoriga nima yoziladi?", "«Ish raxbariga» degan qatopga «Tayinlanmaydi» deb yozib qo'yiladi")
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
