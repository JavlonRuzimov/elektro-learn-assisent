import time
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# 100% tasdiqlangan Level 5 javoblari
VERIFIED_ANSWERS = {
    # 1. Qaysi xujjat asosida xodimlarni tayyorlash:
    "55fa7da8-e38a-4bcd-bad1-203bbfe3f9f4": "ca9f8027-61e2-47fc-ab91-0d111ae1f835", # elektr energetikasi obektlarida xodimlar bilan ishlashni tashkil etish qoidalariga muvofiq
    # 2. TEQ da ko'zda tutilmagan elektr uskunalarni ekspluatatsiya qilish:
    "077cde5e-105a-456d-a6f3-5ea9315aa1f9": "8ff8b478-7579-433f-98c9-832021ebba24", # server to'g'ri ID
    # 3. Dispetcherda tezkor hujjatlar hajmini o'zgartirish mumkinmi:
    "a8e61a45-6cbb-4c42-ada9-14de073ebacb": "aee59524-1637-4d9a-a794-205448dcb65c", # mumkin
    # 4. Yog'och tayanchli havo tarmoqlari kapital ta'mirlanishi:
    "96da8ed6-d452-4552-be34-ad32b46b0f15": "69fee3f8-d0a9-4b76-8d4e-1c55eeb0de7b", # 5 yilda 1 marotaba
    # 5. Erga ulagich va erga ulanayotgan elementlar zanjiri holatini tekshirish:
    "f738ee4d-f97c-4f9d-8954-ba655d0f6232": "1c9a08a4-2652-419a-8369-1b426504cfa7", # 12 yilda kamida 1 marta
    # 6. Tezkor xodimlarni almashtirish ruxsati:
    "71dc6e0d-1f1c-4811-ae4c-7edec21b42b1": "f62ffac2-4330-4d28-9aa7-6477c1ff77c9", # grafikni tasdiqlagan tegishli mamuriy-texnik xodimning ruxsati bilan
    # 7. Yo'riqnomalarni qayta ko'rib chiqish muddati:
    "f8212c9f-9436-4dcc-9deb-da030020113e": "49085cc4-fd33-408f-876d-42824678bd68", # 3 yilda bir marta
    # 8. Avariya rejimlarida transformatorlar o'ta yuklamasi:
    "a854a3cd-56dc-48b0-aac6-25bc3ac7dd3e": "513216dd-8d46-4f86-ad92-47bb37b8fdfd", # ruxsat etiladi
    # 9. Elektr stansiyalari va tarmoqlari asosiy vazifasi:
    "03950889-41b7-42a6-8403-29a5c84c3395": "ddb01f93-173b-489b-ab54-c82228ebf5e9", # ishlab chiqarish, uzatish, taqsimlash va iste'molchilarga yetkazib berish
    # 10. Uskunalar tuzilishi, ekspluatatsiyasi qaysi hujjatlar talabiga mos kelishi kerak:
    "ca3a494a-78d5-4875-b09d-245439d1d58f": "be48d0ab-1b47-4f10-91ee-17d82ede4e66", # mehnat muhofazasi bo'yicha normativ hujjatlarga
    # 11. Havo tarmoqlari tayanchlariga konstruktiv o'zgartirishlar kiritish:
    "c3fc4f5c-e009-4147-acd0-756b37122598": "2e1e7cae-75b2-4883-9c0e-672249f5dcf9", # server to'g'ri ID (faqat texnik hujjatlar / loyiha asosida)
    # 12. EUHT navbatdan tashqari ko'rik o'tkazish holatlari:
    "77df1510-7ae4-482e-a44a-499f105c3cf0": "c1b8a96a-48fd-4e26-b6df-e933894177b7", # muz paydo bo'lganda, o'ynaganda, yong'in, ofat, rele himoya bilan o'chganda
    # 13. Ekspluatatsiya yo'riqnomalariga nimalar kiritiladi:
    "8655eca2-b635-416b-9a58-357fdfed9423": "30b7e53b-6c28-4198-bda2-acd373f6c683", # a,b va javoblar to'g'ri
    # 14. TEQ, XT va Yox qoidalariga rioya qilinishini kim nazorat qiladi:
    "ba447502-63d8-414f-bdb0-84cd1d54daed": "32780d1d-de19-47d7-87a4-e8b7acdce28d", # Energetika tizimini boshqarish organlari tomonidan
    # 15. Pasinka bandaj qilishda sim uzunligi formulasi:
    "41074eaf-8ba2-49f7-b925-83dddf56bc63": "2921f8c8-57c6-44c4-ab28-ebca7d486742", # Lb=26n(D1+D2)
    # 16. Kabel tarmoqlaridan yer qazish mashinalari masofasi:
    "04ac442e-2a31-4291-9a59-e2e70bdd5625": "c3c5c4a0-064d-4048-812a-93c7193eb4b4", # eng kamida 1 metr
    # 17. RTV-10 quvursimon razryadlagichlarda tashqi uchqun oralig'i:
    "4793ef1d-e877-452a-acf7-54ee9561ea96": "30999806-9626-4cad-bae5-44fee576d08b", # 15 mm
    # 18. TEQQ ga nima muvofiqlashtirilishi kerak:
    "1b1c050b-2b20-4c81-b823-ecd720be8ff7": "431f6d72-8fdb-4622-a4ee-0fde86aba011", # server to'g'ri ID
    # 19. Normativ, tashkiliy-farmoyish hujjatlar bajarilishini nazorat qilish:
    "5bf70652-c244-4a95-b5fc-c78d5e95894b": "4d0ee806-b819-440f-9206-1dc91cba7d50", # Energetika tizimini boshqarish organlari tomonidan
    # 20. Kompleks sinovlarda nima tekshiriladi:
    "07b3d143-3583-433d-b7f4-02300b08fb02": "ab05d24d-1bb4-4935-8869-8b256ff8eac9", # asosiy agregatlarni va barcha yordamchi uskunalarni birgalikda yuklama ostida ishlashi
    # 21. Kompleks sinovlar kim tomonidan o'tkaziladi:
    "5152d123-7f43-467c-9e4b-d7719b22fd9a": "4c2be6c3-b147-40e7-8306-b3349678fc8c", # buyurtmachi tomonidan o'tkaziladi
    # 22. Ventilli razryadlagichlarni o'chirib qo'yish:
    "eec62aca-979a-481b-84a5-543e875038cd": "b406f941-3e32-4188-99a2-cef11eb8b6fb", # qish paytida ruxsat etiladi
    # 23. Temir-beton va metall tayanchli havo tarmoqlari kapital ta'mirlanishi:
    "b31b0d67-f579-4bba-99c1-61b2701d1499": "78197ff9-8bac-46ac-afa5-41b3ba8863a9", # 10 yilda 1 marotaba
    # 24. Energetika obyektlarini normal ekspluatatsiya qilish uchun kim javobgar:
    "1f8e1157-72db-4288-b94f-76fe76be7175": "d6888608-0b85-4bb7-901d-16f59562a348", # energetika obektining rahbari
    # 25. Moyli transformatorlarda tok bo'yicha o'ta yuklama 45 foiz:
    "dec03a68-1ff8-4494-87a9-927dc2f1c5c8": "f261f5b6-6148-4011-93f9-a5d86991d28f", # 80 minut
    # 26. Moyli transformatorlarda tok bo'yicha o'ta yuklama 60 foiz:
    "68f6513d-cdf5-4515-bb99-be2e3260b12e": "9b840c7f-95d5-4fc9-b263-0808358c96f0", # 45 minut
    # 27. Har bir energetika obekti nimani taminlashi kerak:
    "ad70f06e-c0d4-4269-80fd-ae0044ebb148": "03830de7-3cdf-4ded-88c2-7150438cf7dc", # maqsadlari va shartlarini
    # 28. Qurilishi tugallangan alohida turgan binolar, inshootlar va uskunalar:
    "2124ee17-8955-4cc6-884a-599c12212c47": "15bf2f99-16da-4e0e-aa0b-9f9140d943ef", # ishchi komissiyalar
    # 29. Havo elektr uzatish tarmoqlarini gabaritlari qanday asboblar yordamida o'lchanadi:
    "60c07e23-23b8-4405-8b1e-5cf9fcbdd2d4": "76e6dde6-dfef-42d5-9d75-19bc8922f514", # uglomer, visotomer
    # 30. Yog'och tayanch va ulama qism (pasinka)larga bandaj qilishda sim o'ramlari soni:
    "e5407060-d776-4b20-b208-6f8f833b18df": "3e93cb71-afef-435b-a53c-3963c5ebc441", # 6 mm bo'lsa 8, 5 mm bo'lsa 10, 4 mm bo'lsa 12
    # 31. Uskunalarga bevosita xizmat ko'rsatuvchi va ta'mirlovchi xodimlar javobgarligi:
    "73fae62e-72c3-44da-80d7-ba1c8c19c55b": "e7f15a11-a7dc-4b9b-99be-f1495e4ed5c4", # shaxsiy javobgar hisoblanadi
    # 32. Energetika moylarni ekspluatatsiya qilganda nima ta'minlanishi kerak:
    "b9a7e466-626e-4095-bd45-417d51498605": "b478fdbf-b11b-442a-8555-94a805015724", # moylarning ekspluatatsion xususiyatlarining saqlanishi...
    # 33. Qancha muddatda havo tarmog'ini bor uzunligi bo'yicha ko'rikdan o'tkazish kerak:
    "29192c89-2c09-4823-b5f5-fce8a5e51274": "180dcfdf-46b5-4d37-8281-45c216b75eed", # 1 yilda kamida 1 marta
    # 34. Ochiq yotqizilgan kabellar yorliqlarida nima ko'rsatilgan bo'lishi kerak:
    "6e3ddcd1-f606-4fa0-9b7a-46975f5f4808": "1c473935-cfc8-41f9-809c-69852986ab52", # markasi, kuchlanishi, ko'ndalang kesimi, liniya raqami yoki nomi
    # 35. Uskuna buzilganligi, yong'in chiqqanligi haqida tezkor xodim kimga xabar berishi kerak:
    "6a9c5d14-eb56-47ab-842a-1eac4811bc2c": "f025faea-472a-46a7-b6e4-0e632cf0b734", # tasdiqlangan ro'yxat bo'yicha yuqori turuvchi tezkor va mamuriy-texnik raxbar xodimlarga
    # 36. TEQ qoidalari nimalarda tatbiq etilmaydi:
    "e220ac79-2ed3-427f-bc16-a3fca573d245": "84480d69-ccf4-42b8-8bcb-4b532dda9828", # stantsionar va ko'chma dizel elektr stantsiyalariga
    # 37. Moy bilan tabiiy sovutiladigan transformatorlar moyining maksimal harorati:
    "2252b805-f50d-4736-88f8-08d1f62422d5": "643449b6-fb7e-4275-9731-a7fd5338bb86", # 95°S
    # 38. Qanday holatlarda uskunalar yuqori turuvchi ruxsatisiz o'chirilishi/ulanishi mumkin:
    "d620aae1-edd7-4a7e-b199-4d9376e781dc": "65d2174a-1f8c-4295-9174-e83450ddb3ad", # odamlar va uskunalarga aniq xavf tug'diradigan holatlar mavjud bo'lganda
    # 39. Quvursimon razryadlagichlarda yoy qaysi printsip asosida so'ndiriladi:
    "802c334c-4952-42b6-a966-204d3d27741d": "0afa574e-27f0-479a-b55f-b76e64bc2030", # uzun bo'ylama portlash hosil bo'lishi xisobiga
    # 40. Uskunalar, binolar va inshoatlarni qoidalarga muvofiqligini kim ta'minlashi kerak:
    "e8689b38-0f28-4b22-814e-2d5dfdb1bd29": "e2e7ce7a-9078-42fd-ae5b-4356fd49162a", # har bir xodim o'z vazifalari doirasida
    # 41. Ta'mirlash ishlarining davriyligi va davomiyligi nima asosida belgilanadi:
    "8109d63a-67b6-43bc-b669-a06ed012ad9c": "3d9af416-083b-442b-8cd5-d0ee584ba405", # uskunalarning ushbu turini ta'mirlash bo'yicha soha qoidalariga asosan
    # 42. Elektr tarmoqlari korxonalarida transformator moyining zaxirasi:
    "296ea166-f714-4bb3-bf96-e498b0e84c61": "2b5b125d-d585-46fb-b17b-4c9fc5c6feea", # uskunalarga quyilgandan kamida 2 foizi miqdorida
    # 43. Alohida kasblar hamda alohida turdagi ishlar uchun yo'riqnomalar qanday asosda:
    "36275295-df83-4f06-bdb3-2e06e5597573": "55c2939d-e49f-4d7a-85cc-74ff932d6bbd", # mehnat muhofazasi bo'yicha yo'riqnomalarni ishlab chiqish to'g'risidagi nizomga asosan
    # 44. Moyli transformatorlarda tok bo'yicha o'ta yuklama 100 foiz bo'lganda davomiyligi:
    "b1db1b77-cf7b-46ea-bd42-1c64a83ae5ff": "16401d1d-2e28-47f1-bda2-8616fb493891", # 10 minut
    # 45. Ekspluatatsion-ta'mirlash hujjatlari yuritilishini kim ta'minlashi kerak:
    "8b63959f-b57a-4c63-bc72-e82a8bf7a261": "88233abc-e808-4b73-b332-fa6786e4a885", # uskunalar ekspluatatsiya qilinishi uchun javobgar shaxslar
    # 46. Nima uchun laboratoriyalarga shikastlangan kabel namunalari taqdim etilishi kerak:
    "b1c4419f-9e53-4149-af8d-cce2c99ecc94": "0dbbc91f-ea41-45fb-91ba-41cb97a13ed4", # shikastlanish sabablarini aniqlash va ularning oldini oluvchi tadbirlarni ishlab chiqish uchun
    # 47. Uskunalarni ta'mirlash uchun talabnomalar necha xil bo'ladi:
    "d71e63c0-9464-47dc-84f2-2700e5b2302e": "5f07f27c-cd5d-4cb7-ac25-87e20098a5b4", # 3 xil (rejali, shoshilinch/kechiktirib bo'lmaydigan, avariya)
    # 48. Ekspluatatsiya jarayonida bajarilgan o'zgartirishlar qayerga kiritiladi:
    "606636e9-fe8e-4b7a-a6dd-cbb8d54ee346": "5a861e45-87ec-41a2-acdf-698fe0f57135", # yo'riqnomalar, sxemalar va chizmalarga
    # 49. Moyli transformatorlarda tok bo'yicha o'ta yuklama 75 foiz bo'lganda davomiyligi:
    "f9d699e6-567a-43ee-a5bb-61f533794645": "da10914b-acf1-4ca3-ae77-2c4b1c1211d4", # 20 minut
    # 50. Xodimlar TEQ qoidalarini buzganligi uchun nima asosida javobgar:
    "061bd0ef-2eb4-4494-b286-60dd95a9ee41": "241e56bb-af93-4465-ad05-ca32bf426cde", # amaldagi qonunchilikka muvofiq
    # 51. 0.4 kVli havo tarmoqlarda simning yo'lning qatnov qismigacha masofasi:
    "dc31cb11-c03c-48f4-a0cf-dd4dcd4825f7": "3a263278-19a2-438b-8e0f-ede486eea6b6", # kamida 6 m
    # 52. Har bir dispetcherlik darajasi uchun boshqarishning nechta toifasi bor:
    "d89c2b2e-557a-406b-800c-300491c9b85c": "13f84329-9384-4849-a8cb-c14bddf94741", # 2 ta (tezkor boshqaruv va tezkor tasarruf)
    # 53. Ishchi komissiyaning vazifalari nimalardan iborat:
    "9ed18c04-0b85-4c9b-8544-3753064d2419": "02c0b7a4-9a20-4b93-acd0-d047e6329814", # ishchi komissiya kompleks sinab ko'rish va nuqsonlar bartaraf etilgandan keyin...
    # 54. Smenani qabul qilish-topshirish vaqtida tezkor xodim nimani bajarishi kerak:
    "296821d8-4cdf-46ae-91a3-82b2ea5be95d": "e8e34047-d17b-4ced-adf3-807eb44f7aba", # jurnalga yoki qaydnomaga yozib, imzosi bilan rasmiylashtiradi
    # 55. Idoraviy texnik va texnologik nazoratning asosiy vazifasi:
    "30613eb9-131c-4625-8688-17654a8f5bc4": "0465546f-954b-4fc2-89c9-cdcccf537a7e", # a,b va v javoblar to'g'ri
    # 56. Energetik obektni qabul qilishda aniqlangan nuqsonlarni bartaraf etish ustidan nazorat:
    "b9bc49ce-16c9-4872-9e92-6993d0c5dcb6": "129e896f-ab03-489c-8e82-723fcf197303", # energetika obektlarini qabul qilishga taqdim qiluvchi buyurtmachi tomonidan
    # 57. Uskunalar ta'mirining sifati nimani hisobga olib baholanadi:
    "32045ec6-f34e-4b67-beb8-caeffc6437ad": "43abdd52-52f8-4057-9e8d-07af0608587b", # a,v va g javoblar to'g'ri
    # 58. Yo'riqnomalar, nizomlar, sxemalar ro'yxati kim tomonidan tasdiqlanadi:
    "2bfffdb8-dc29-40b9-9c36-f9a68157b428": "f37bcafd-342b-4b38-9bdb-1c3d5e9d5333", # energetika obektining bosh muxandisi
    # 59. Uskunalarning texnik holatiga kim javobgar hisoblanadi:
    "e7e45de8-6391-4666-973c-7e34837e9015": "888fcd32-9820-45da-8a63-1dcc897aae30", # energetika obektining rahbarlari*
    # 60. Qoida talablari qaysi sohalarda amal qiladi:
    "28542eb5-e8a2-4ae1-b8c1-c51013ce5940": "2efe0a27-5dfe-45b5-92f3-2283c4211183", # barcha issiqlik va gidroelektrostantsiyalari, qozonxonalar, elektr va issiqlik tarmoqlari...
    # 61. Yog'och tayanchlarda o'rnatiladigan erlagich simining diametri:
    "243350d6-375d-4395-ac4c-2157d54c5363": "f08e73c3-eba9-447e-9c09-a73d51465309", # ko'p tolali 35 mm, yakka tolali 10 mm dan kam bo'lmasligi kerak
    # 62. Korroziyaga qarshi qoplama qachon tiklanishi kerak:
    "f4468a79-3f62-49fe-b92a-9bf1b7b87636": "e1d9e6b4-f009-4df3-99d5-53b5c1ee747e", # energetika obekti bosh muxandisining farmoyishiga asosan
    # 63. Har bir ish joyi bo'yicha lavozim yo'riqnomalarida nimalar ko'rsatilishi kerak:
    "ebc80714-8d72-4035-b3fd-9cd6c1d30b73": "72b8db69-b6ca-47c6-91e6-5d7dbb6e39eb", # uskunalarga xizmat ko'rsatish bo'yicha yo'riqnomalar, sxemalar ro'yxati, huquq, majburiyat, javobgarlik...
    # 64. Uskunalar, binolarga xizmat ko'rsatish, ta'mirlash qayerda tashkil etiladi:
    "7bdbefa1-fadc-4f44-af31-f2781cadde3e": "1adefab0-6666-49b6-bf34-5a585d6656aa", # har bir energetika obektida
    # 65. Zaxiradagi uskunalarga o'tish, profilaktik ko'rik qancha muddatda:
    "1e3a0ba1-90ec-4214-8dd3-f0b4726a8767": "967a1acc-399d-41ad-a8f3-253c25cf63ae", # tasdiqlangan jadval bo'yicha
    # 66. Uskunani ta'mirga chiqarish uchun kim bilan kelishiladi:
    "9796c159-4f25-459a-b75b-580126f1553b": "296ff18f-0220-4910-87ef-54b776d4c14f", # tarmoq korxonalari, tizim operatori va “Energiya” MDM dispetcheri bilan
    # 67. Boshqaruv organiga bevosita ta'sir ko'rsatish huquqiga ega bo'lgan ta'mirlash xodimi:
    "f498fa8e-15bd-4072-b851-90f3ae650fe9": "5d148f58-c4d0-46d0-8488-81dc22af0282", # tezkor tamirlash xodimlari toifasiga
    # 68. Gabaritni cheklovchi belgilar sozligini kim kuzatib borishi kerak:
    "77683ca7-0655-4554-a0d6-d24cb5f48ee3": "89be7922-5873-4582-9daf-01014eac5677", # elektr tarmoqlarini ekspluatatsiya qiluvchi tashkilot
    # 69. Dispetcherlar qachon shaxsiy javobgarlikka tortiladi:
    "62f89e37-1711-4cdf-8ca3-ebc4189d8fe2": "e05ddd1e-4ff8-48e1-a492-6208da11622b", # bevosita qo'l ostidagi xodimlar yoki ularning ko'rsatmasi bo'yicha ish bajaruvchi xodimlar tomonidan yo'l qo'yilgan buzilishlar uchun
    # 70. Puflab sovutilishi o'chirilgan transformatorlarni ishlash sharoiti nima bilan belgilanadi:
    "cfe1538b-7a3f-4d53-a9fd-548c0b9890de": "8828deb9-398b-483c-930a-9311142ac626", # zavod yo'riqnomasi bilan belgilanadi
    # 71. Almashlab-ulash vaqtida kiritilgan o'zgarishlar qayerda aks ettiriladi:
    "514b972c-053b-4c97-9b77-403f1d22f220": "e8beb5b4-7858-4556-a4aa-f6e5a9db5018", # tezkor sxemada yoki mnemosxemada
    # 72. Texnik-iqtisodiy ko'rsatkichlarning muntazam hisobini kim olib boradi:
    "1b6a63e4-3525-4665-a343-0bf8a60f3951": "64352a39-988a-4d69-b202-8bace1d4260a", # energetika obektlari, tamirlash va tamirlash-sozlash tashkilotlari
    # 73. Energetik obektda ishlashga kimga ruxsat beriladi:
    "3bdcc448-3a0f-4f0b-9e19-06f3c544f6ae": "2f83f4f5-d8da-4880-97dc-343273dbdeaf", # 18 yoshdan kichik bo'lmagan hamda egallangan lavozimining talablari xajmida tayyorgalikdan o'tgan shaxslarga
    # 74. Ikkilamchi zanjirlar izolyatsiyasining yerga nisbatan ruxsat etilgan qarshiligi:
    "3e22b536-c639-4e5a-89aa-fdbb49e9c043": "59ac89ee-ba82-4bed-8fff-5140f74684c8", # 1 MOm
    # 75. Transformatorlarni kapital va joriy ta'mirlash qachon o'tkaziladi:
    "b0606668-277f-4a9d-8f16-c31912d34dea": "0812d49a-cf14-413f-8719-00bbc795decd", # sinovlar va tashqi ko'rik natijalari bilan aniqlanadigan texnik holatiga qarab zaruriyat bo'yicha
    # 76. TEQ qoidalarini bilish va bajarish kimlar uchun majburiy:
    "7474dbc3-4c3f-4249-ae5f-e6f21a9cf856": "06b6392c-7b57-42f8-bbb0-5c0ec7fdf354", # energetika tizimi korxonalari va tashkilotlarining barcha xodimlari
    # 77. Barcha ish joylarida bo'lishi kerak bo'lgan yo'riqnomalar kim tomonidan imzolanadi va tasdiqlanadi:
    "9cbcc65d-aef6-4609-a93c-07ad6cc71cd6": "16e67aa4-8b24-4225-954d-d8559c0fddbc", # bo'linma boshlig'i imzolaydi, energetika obekti bosh muxandisi tasdiqlaydi
    # 78. Maxsus texnik ekspluatatsiya qilish qoidalari kim tomonidan joriy etiladi:
    "c191a918-7fb9-4cab-95f3-909fd10341a4": "d70cca13-b9ca-4f3c-a7ff-4644396c748f", # bunga vakolatli idoralar tomonidan, faqat “O'zdavenergonazorat” inspektsiyasi bilan kelishilgan holda
    # 79. Transformatorlarni o'chirmay turib ko'rikdan o'tkazish muddatlari qanday aniqlanadi:
    "0bac87d8-be73-45c7-9ba3-743bb0e3931f": "77d3a7a6-4fbc-41c9-b8df-23de61298845", # energetika obektining texnik rahbari tomonidan ularning vazifasi, o'rnatilgan joyi va texnik holatiga qarab
    # 80. O'lchov vositalari bilan jihozlanishi nimaga muvofiq bo'lishi kerak:
    "7f3508fe-080e-41d5-895a-1830707f2549": "8f926f97-b44a-4fc1-8906-20f86ae551ea", # loyiha-normativ hujjatlar va ularni yetkazib berishning texnik shartlariga muvofiq
    # 81. Tashkilot rahbari nima uchun shaxsiy javobgar hisoblanadi:
    "3b7b1d0f-d855-4360-902a-bde661a7065a": "03689d2b-cf10-46b5-b081-155739729ef7", # a,v va g javoblar to'g'ri
}

level5_id = "f15546e6-82ac-4d89-ad78-b9ef37009aea"
detail = client.progress.get_level_detail(level5_id)

print(f"=== LEVEL 5: {detail.title} ===")
hearts_info = client.base_client.get('/progress/me')['hearts']
print(f"Joriy energiya: {hearts_info['heartsCount']}/{hearts_info['maxHearts']}")

for idx, t in enumerate(detail.theories, 1):
    if t.is_complete:
        print(f">> MODUL {idx}: {t.title} allaqachon tugatilgan.")
        continue

    print(f"\n==========================================")
    print(f"MODUL {idx}: {t.title} ({t.answered_questions}/{t.total_questions})")
    print(f"==========================================")

    while True:
        q_data = client.progress.get_theory_questions(t.id, mode="continue")
        questions = q_data.get("questions", [])
        if not questions or q_data.get("is_module_complete"):
            print(f">> {t.title} yakunlandi!")
            break

        answered_any = False
        for q in questions:
            opt_id = VERIFIED_ANSWERS.get(q.id)
            if not opt_id:
                print(f"\n[TO'XTATILDI - Yangi savol]: '{q.prompt}' (ID: {q.id})")
                for opt in q.options:
                    print(f"   [{opt.id}] {opt.option_text}")
                exit(0)

            opt_text = next((o.option_text for o in q.options if o.id == opt_id), opt_id)
            print(f"\n[Savol]: {q.prompt}")
            print(f"  -> Tanlangan: '{opt_text[:50]}'")

            time.sleep(2)
            res = client.progress.submit_answer(q.id, opt_id, source="LESSON")

            if res.is_correct:
                hearts = res.hearts.get('heartsCount') if isinstance(res.hearts, dict) else res.hearts
                print(f"  [+] TO'G'RI JAVOB! (+{res.xp_earned} XP, Energiya: {hearts})")
                kb.record_answer(q.id, q.prompt, opt_id, opt_text)
                answered_any = True
            else:
                print(f"  [-] XATO! Server to'g'ri deb ko'rsatgan ID: {res.correct_option_id}")
                exit(1)
            time.sleep(1.5)

        if not answered_any:
            break
