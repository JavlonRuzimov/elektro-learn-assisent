import json, sys, os
sys.path.insert(0, os.path.abspath('.'))
from agent.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

answers = [
    ("c2ae9b47-21a8-473f-b89b-ee7a4db74cc4", "Uskunalarning texnik holati ustidan doimiy nazorat kim tomonidan amalga oshiriladi?", "492a92ec-0f11-49ad-9750-63df9d384462", "tezkor va tezkor -tamirlovchi xodimlar toionidan"),
    ("1f2521aa-b2f2-4144-a61f-7a8f3501d002", "Qaysi vaqtdan boshlab buyurtmachi yangi ishga tushiriladigan obekt jixozlarini asrashga masul xisoblanadi?", "07c13532-56da-432e-8d06-c2d9dc4bc0b3", "ishchi komissiya tomonidan kompleks sinab ko'rish uchun dalolatnoma imzo-langan daqiqadan boshlab buyurtmachi uskunalarni saqlanishi uchun javobgar bo'ladi"),
    ("c176c9d3-e943-4168-a88d-02d543e8ee3e", "Uskunaning texnik holatini doimiy nazorat qilish tartibi nima bilan belgilanadi?", "fa7e298b-1d72-42b6-98cc-eb86c9775a66", "mahalliy ishlab chiqarish va lavozim yo'riqnomalari asosida"),
    ("9bad590f-7166-46b3-938b-36aee4b9f830", "Elektr uskunalarni kapital va o'rta tamirdan keyin qabul qilish nima asosida amalga oshiriladi?", "8ab1ecbc-ca07-4757-8212-67703fe0324e", "ijrochilar bilan kelishilgan va energetika obektining bosh muhandisi tasdiqlagan dastur bo'yicha"),
    ("12c0ad0d-673c-4c6f-a7a7-572140694275", "Yog'och tayanch va ulama qism (pasinka)larga bandaj qilish uchun qanday simlardan foydalaniladi?", "c58a56fd-3797-4423-a262-b692bc27772f", "diametri 4 mm bo'lgan rux bilan ishlov berilgan (otsinkovkalangan) yumshoq oq po'lat simlar, diametri 5-6 mm bo'lgan rux bilan ishlov berilmagan katanka simlardan foydalaniladi"),
    ("f9808494-8540-46a9-be5f-f16798fc8393", "Texnologik sxemalar, chizmalar qancha muddatda qayta ko'rib chiqilishi kerak?", "42737b54-d5b5-4805-9716-511a8b536a69", "3 yilda bir marta"),
    ("69a4e712-d8ae-48c8-863f-17f8019fa4be", "Yog'och tayanchga 1 ta ulama qism (pasinka)ni maxkamlashda bandaj qanday va qaerga qilinadi?", "237ebff4-4627-4aa8-be54-87ef9e19098f", "yog'och tayanchga 1 ta ulama qism (pasinkaning) yuqori qismidan 100 mm pastda, ikkinchisi yog'och tayanchning quyi qismidan 150 mm yuqorida. Bandajlar orasidagi masofa 800-1100 mm ni tashkil etadi"),
    ("a9ca78ed-362d-4752-b48c-ae66ac55fdba", "Xavfsizlik texnikasi qoidalarini buzish hollari aniqlan-ganda yoki ishlayotgan odamlar xayotiga xavf tug'diruvchi boshqa holatlar sezilganda nima qilish kerak?", "2513d6c9-3e64-4db2-9240-2a17194dad9c", "brigada ish joyidan chiqarilishi va ish bajaruvchidan naryad olib qo'yi-lishi shart"),
    ("22a5aa87-edd0-40b2-8857-a0a94b19da50", "Brigada tarkibini kim o'zgartirish xuquqiga ega?", "a701932c-9d1d-487d-8afa-615d5e86947e", "naryad beruvchi yoki ushbu elektr qurilmada mazkur ishni bajarish uchun naryad berish huquqiga ega bo'lgan boshqa xodimga ruxsat beriladi"),
    ("696e4a17-fd08-4dd1-8623-faae5b3f78e2", "Ishlar to'liq tugagandan so'ng ish bajaruvchi nima qiladi?", "47a36231-43e5-4240-8cdc-66b431c28c4f", "brigadani ish joyidan chikarishi, brigada qo'ygan vaqtinchalik to'siqlar, plakatlar, bayroqchalar va erga ulagichlarni olishi, elektr qurilma eshik-larini berkitishi, naryadda o'z imzosi bilan ishlar to'liq tugaganligini rasmiylashtirishi shart"),
    ("2e2f93fb-ef38-4c54-8fc2-5d4a537cabc5", "Naryad muddatini kim uzaytirishi mumkin?", "2a109c3d-fcef-4744-9d17-6df310cab6ca", "mazkur naryadni bergan yoki ushbu elektr qurilmada naryad berish huquqiga ega bo'lgan xodimgina uzaytirishi mumkin"),
    ("99eb80c4-61d8-492c-bccf-1f9231db32bb", "“Naryad berdi” va “Naryad muddati uzaytirildi” degan satr-larga nima yoziladi?", "884a8be9-a773-4553-a0eb-f3105ba6e1d0", "naryad beruvchi unga qo'l qo'ygan vaqtini va sanasini ko'rsatadi. Naryad be-ruvchi va uning muddatini uzaytiruvchi shaxslar qo'l qo'yishdan tashqari o'zla-rining familiyalarini ham ko'rsatishlari shart"),
    ("b8282e58-8ab8-45f3-8bed-453f7999a6c6", "Ish bajaruvchi (kuzatuvchi) ish joyidan vaqtincha ketishi ke-rak bo'lib qolsa uning o'rniga kim qoladi?", "03d492cd-765c-46d7-b823-d7cef08aecd7", "* ish raxbari, ishga qo'yuvchi yoki naryad berish xuquqiga ega bo'lgan xodim qolishi mumkin"),
    ("3c9fcd77-4af3-42fb-81e9-b2bc3b0b4933", "Daraxtlar simlarning ustiga ag'anashini oldini olish uchun nima kilish kerak ?", "94ae62b1-2740-4f19-a3cc-b1c34a6406f1", "ularni kesishdan oldin tortqilar qo'llanilishi shart"),
    ("e14adf92-dda5-4713-a2d2-6d0a0227d964", "Naryadning 3-jadvaliga nima yoziladi?", "1fb24c3b-a874-4a8a-a2ee-8e9ea7e5525a", "har kungi ishga qo'yish va uni tugatish, shu jumladan, brigadani bir ish joyidan ikkinchi ish joyiga o'tkazishda ishga qo'yish hamda brigada azo-lariga ish joyida yo'l-yo'riq berilganligi rasmiylashtiriladi"),
    ("ef71d073-dc40-4511-b61c-ac81c8dea718", "Naryadda ko'rsatilayotgan shaxsning familiyasidan tashqari yana nima yoziladi?", "17eea3f8-180f-49fb-89c2-e158bcc8b38d", "familiyasidan tashqari uning ism-sharifi va elektr xavfsizligi bo'yicha guruhi yoziladi"),
    ("5883037d-6804-4fd2-b7d7-30a96542164f", "Bir ish raxbariga beriladgan naryadlar sonini kim belgilay-di?", "921d1dc4-54af-4d74-86c5-f706faa4f7d8", "naryad beruvchi belgilaydi"),
    ("3120302e-1a58-474c-8b95-6a92ed649adb", "Tok o'tkazuvchi qismlarga erga ulagichni qachon o'rnatish ke-rak?", "47bd5bd4-a7f3-43cc-b31b-b87944d46f40", "bevosita kuchlanish yo'qligi tekshirilgandan keyin o'rnatilishi shart"),
    ("4ee1d74a-8978-47e0-98db-648a3402e4e5", "Yong'inga qarshi mashqlar mavzulari va xajmlari qanday aniqlanadi? (1.14.214)", "0e2d0475-ee9c-4ca1-8234-bf779f654097", "xodimlarni, uskunalarni boshqarishni to'xtatmasdan, yong'in o'chirish bo'-limlari bilan birgalikda yong'inni o'chirishning amaliy ko'nikmalariga ega bo'lishini hisobga olgan holda aniqlanadi"),
    ("2f827149-d893-4e00-9cef-dc469e5ab441", "Yong'in sodir bo'lganda texnologik shartlari bo'yicha tokdan uzib qo'yilishi mumkin bo'lmagan muayyan uskunalar ro'yxati kim tomonidan aniqlanadi? (3.1.91)", "12c213f8-4425-4277-a10b-35c31a83c6d1", "bosh muhandis (texnik rahbar) buyrug'iga ko'ra aniqlanadi"),
    ("70c6683c-8e5f-4942-a725-6abcbeba232d", "FVV hududiy yong'in-qutkaruv bo'linmasining birinchi bo'lin-masi etib kelgandan keyin kim yong'inni o'chirish rahbari hisoblanadi? (3.3.108)", "f5edabff-3e64-41ec-8552-fe7975b1ad11", "yong'in-qutqaruv bo'linmasining birinchi bo'linmasi kelganidan keyin ushbu bo'linmaning navbatchi smena boshlig'i yong'inni o'chirish rahbari hisoblanadi"),
    ("4d4c9468-b133-4413-883f-64d52a62adce", "Rejadan tashqari yo'riqnoma qachon o'tkaziladi?", "219feb1f-5e91-43ed-b203-154552aa7737", "a, b va v javoblar to'g'ri"),
    ("6df4c520-0246-4b28-89a4-1eb7845e0c29", "Maxsus tayyorgarlik nima?", "498537c2-32d6-40e0-8eee-90bee84c7cca", "tezkor va tezkor-tamirlash xodimlarini o'qitish"),
    ("e479fbfe-aa6e-41de-a846-eee21d60351a", "Agar xodim dublyorligi davrida tezkor ishlarni bajarish bo'yicha etarlicha ko'nikmaga ega bo'lmagan bo'lsa yoki avariyaga qarshi nazorat mashg'ulotlarida “qoniqarsiz” baho olsa nima qilish kerak?", "8805b8c7-35d3-45b1-bf03-5623b8833780", "xodimning dublyorlik muddatini (asosiy dublyorlik davomiyligidan ko'p bo'lmagan muddatga) uzaytirishga va qo'shimcha avariyaga qarshi nazorat mashg'uloti o'tkazishga ruxsat etiladi"),
    ("782a87c3-086c-4f8d-8fc7-844ba70e4ddf", "Montyorning saqlagich kamarlari va xavfsizlik arqonlari qanday sinovlardan o'tkaziladi? (3.2.11)", "9b4fde7f-902c-4c8b-b012-45e53e64d5d2", "statik"),
    ("6d8f98b3-515b-4757-8e12-aa12f7019b85", "Ximoya vositalarini sinovdan o'tkazish qanday tartibda amal-ga oshiriladi? (3)", "8fdde697-ebd9-44ca-bf97-ad83ce58ddf4", "namunaviy va qabul qilish-topshirish"),
    ("73b69953-b0a6-42c6-8445-86e6ebd4a990", "Suyaklar sinishi bu nima?", "09f0bc47-fcd2-4a71-af7e-ca6b1254f61d", "suyak butunligining buzilishi suyakning sinishi deb ataladi")
]

for qid, prompt, opt_id, opt_text in answers:
    kb.record_answer(qid, prompt, opt_id, opt_text)

print(f"Recorded all {len(answers)} answers to knowledge base!")
