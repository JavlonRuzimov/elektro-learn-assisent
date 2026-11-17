import time
import json
import os
import sys
from datetime import datetime, timezone, timedelta

# Windows pythonw.exe da stdout/stderr None bo'lgani sababli faylga yo'naltirish
os.makedirs("data", exist_ok=True)
if sys.stdout is None:
    sys.stdout = open("data/autopilot.log", "a", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open("data/autopilot_err.log", "a", encoding="utf-8")

def format_tashkent_time(iso_str: str) -> str:
    """UTC ISO vaqtini Toshkent (UTC+5) vaqtiga formatlash"""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        tashkent_tz = timezone(timedelta(hours=5))
        return dt.astimezone(tashkent_tz).strftime("%H:%M:%S")
    except Exception:
        return iso_str
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase
from library_searcher import LibraryKnowledge

def load_env_vars():
    env_vars = {}
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

_env = load_env_vars()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or _env.get("TELEGRAM_BOT_TOKEN", "").strip()
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_ADMIN_CHAT_ID") or _env.get("TELEGRAM_ADMIN_CHAT_ID", "").strip()

client = ElektroLearnClient()
kb = KnowledgeBase()
library = LibraryKnowledge()

def send_telegram_alert(msg: str):
    """Foydalanuvchiga Telegram orqali holat xabarnomasini yuborish"""
    global ADMIN_CHAT_ID
    if not ADMIN_CHAT_ID:
        # Chat ID ni .env dan qayta o'qish
        curr_env = load_env_vars()
        ADMIN_CHAT_ID = curr_env.get("TELEGRAM_ADMIN_CHAT_ID", "").strip()
    if BOT_TOKEN and ADMIN_CHAT_ID:
        try:
            import requests
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": int(ADMIN_CHAT_ID), "text": msg, "parse_mode": "HTML"}, timeout=10)
        except Exception:
            pass

def log_print(msg: str):
    print(msg, flush=True)
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/autopilot.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass

# 100% tasdiqlangan savol-javoblar bazasi
VERIFIED_ANSWERS = {
    # 1. Qaysi xujjat asosida xodimlarni tayyorlash:
    "55fa7da8-e38a-4bcd-bad1-203bbfe3f9f4": "ca9f8027-61e2-47fc-ab91-0d111ae1f835",
    # 2. TEQ da ko'zda tutilmagan elektr uskunalarni ekspluatatsiya qilish:
    "077cde5e-105a-456d-a6f3-5ea9315aa1f9": "8ff8b478-7579-433f-98c9-832021ebba24",
    # 3. Dispetcherda tezkor hujjatlar hajmini o'zgartirish mumkinmi:
    "a8e61a45-6cbb-4c42-ada9-14de073ebacb": "aee59524-1637-4d9a-a794-205448dcb65c",
    # 4. Yog'och tayanchli havo tarmoqlari kapital ta'mirlanishi:
    "96da8ed6-d452-4552-be34-ad32b46b0f15": "69fee3f8-d0a9-4b76-8d4e-1c55eeb0de7b",
    # 5. Erga ulagich va erga ulanayotgan elementlar zanjiri holatini tekshirish:
    "f738ee4d-f97c-4f9d-8954-ba655d0f6232": "1c9a08a4-2652-419a-8369-1b426504cfa7",
    # 6. Tezkor xodimlarni almashtirish ruxsati:
    "71dc6e0d-1f1c-4811-ae4c-7edec21b42b1": "f62ffac2-4330-4d28-9aa7-6477c1ff77c9",
    # 7. Yo'riqnomalarni qayta ko'rib chiqish muddati:
    "f8212c9f-9436-4dcc-9deb-da030020113e": "49085cc4-fd33-408f-876d-42824678bd68",
    # 8. Avariya rejimlarida transformatorlar o'ta yuklamasi:
    "a854a3cd-56dc-48b0-aac6-25bc3ac7dd3e": "513216dd-8d46-4f86-ad92-47bb37b8fdfd",
    # 9. Elektr stansiyalari va tarmoqlari asosiy vazifasi:
    "03950889-41b7-42a6-8403-29a5c84c3395": "ddb01f93-173b-489b-ab54-c82228ebf5e9",
    # 10. Uskunalar tuzilishi, ekspluatatsiyasi qaysi hujjatlar talabiga mos kelishi kerak:
    "ca3a494a-78d5-4875-b09d-245439d1d58f": "be48d0ab-1b47-4f10-91ee-17d82ede4e66",
    # 11. Havo tarmoqlari tayanchlariga konstruktiv o'zgartirishlar kiritish:
    "c3fc4f5c-e009-4147-acd0-756b37122598": "2e1e7cae-75b2-4883-9c0e-672249f5dcf9",
    # 12. EUHT navbatdan tashqari ko'rik o'tkazish holatlari:
    "77df1510-7ae4-482e-a44a-499f105c3cf0": "c1b8a96a-48fd-4e26-b6df-e933894177b7",
    # 13. Ekspluatatsiya yo'riqnomalariga nimalar kiritiladi:
    "8655eca2-b635-416b-9a58-357fdfed9423": "30b7e53b-6c28-4198-bda2-acd373f6c683",
    # 14. TEQ, XT va Yox qoidalariga rioya qilinishini kim nazorat qiladi:
    "ba447502-63d8-414f-bdb0-84cd1d54daed": "32780d1d-de19-47d7-87a4-e8b7acdce28d",
    # 15. Pasinka bandaj qilishda sim uzunligi formulasi:
    "41074eaf-8ba2-49f7-b925-83dddf56bc63": "2921f8c8-57c6-44c4-ab28-ebca7d486742",
    # 16. Kabel tarmoqlaridan yer qazish mashinalari masofasi:
    "04ac442e-2a31-4291-9a59-e2e70bdd5625": "c3c5c4a0-064d-4048-812a-93c7193eb4b4",
    # 17. RTV-10 quvursimon razryadlagichlarda tashqi uchqun oralig'i:
    "4793ef1d-e877-452a-acf7-54ee9561ea96": "30999806-9626-4cad-bae5-44fee576d08b",
    # 18. TEQQ ga nima muvofiqlashtirilishi kerak:
    "1b1c050b-2b20-4c81-b823-ecd720be8ff7": "431f6d72-8fdb-4622-a4ee-0fde86aba011",
    # 19. Normativ, tashkiliy-farmoyish hujjatlar bajarilishini nazorat qilish:
    "5bf70652-c244-4a95-b5fc-c78d5e95894b": "4d0ee806-b819-440f-9206-1dc91cba7d50",
    # 20. Kompleks sinovlarda nima tekshiriladi:
    "07b3d143-3583-433d-b7f4-02300b08fb02": "ab05d24d-1bb4-4935-8869-8b256ff8eac9",
    # 21. Kompleks sinovlar kim tomonidan o'tkaziladi:
    "5152d123-7f43-467c-9e4b-d7719b22fd9a": "4c2be6c3-b147-40e7-8306-b3349678fc8c",
    # 22. Ventilli razryadlagichlarni o'chirib qo'yish:
    "eec62aca-979a-481b-84a5-543e875038cd": "b406f941-3e32-4188-99a2-cef11eb8b6fb",
    # 23. Temir-beton va metall tayanchli havo tarmoqlari kapital ta'mirlanishi:
    "b31b0d67-f579-4bba-99c1-61b2701d1499": "78197ff9-8bac-46ac-afa5-41b3ba8863a9",
    # 24. Energetika obyektlarini normal ekspluatatsiya qilish uchun kim javobgar:
    "1f8e1157-72db-4288-b94f-76fe76be7175": "d6888608-0b85-4bb7-901d-16f59562a348",
    # 25. Moyli transformatorlarda tok bo'yicha o'ta yuklama 45 foiz:
    "dec03a68-1ff8-4494-87a9-927dc2f1c5c8": "f261f5b6-6148-4011-93f9-a5d86991d28f",
    # 26. Moyli transformatorlarda tok bo'yicha o'ta yuklama 60 foiz:
    "68f6513d-cdf5-4515-bb99-be2e3260b12e": "9b840c7f-95d5-4fc9-b263-0808358c96f0",
    # 27. Har bir energetika obekti nimani taminlashi kerak:
    "ad70f06e-c0d4-4269-80fd-ae0044ebb148": "03830de7-3cdf-4ded-88c2-7150438cf7dc",
    # 28. Qurilishi tugallangan alohida turgan binolar, inshootlar va uskunalar:
    "2124ee17-8955-4cc6-884a-599c12212c47": "15bf2f99-16da-4e0e-aa0b-9f9140d943ef",
    # 29. Havo elektr uzatish tarmoqlarini gabaritlari qanday asboblar yordamida o'lchanadi:
    "60c07e23-23b8-4405-8b1e-5cf9fcbdd2d4": "76e6dde6-dfef-42d5-9d75-19bc8922f514",
    # 30. Yog'och tayanch va ulama qism (pasinka)larga bandaj qilishda sim o'ramlari soni:
    "e5407060-d776-4b20-b208-6f8f833b18df": "3e93cb71-afef-435b-a53c-3963c5ebc441",
    # 31. Uskunalarga bevosita xizmat ko'rsatuvchi va ta'mirlovchi xodimlar javobgarligi:
    "73fae62e-72c3-44da-80d7-ba1c8c19c55b": "e7f15a11-a7dc-4b9b-99be-f1495e4ed5c4",
    # 32. Energetika moylarni ekspluatatsiya qilganda nima ta'minlanishi kerak:
    "b9a7e466-626e-4095-bd45-417d51498605": "b478fdbf-b11b-442a-8555-94a805015724",
    # 33. Qancha muddatda havo tarmog'ini bor uzunligi bo'yicha ko'rikdan o'tkazish kerak:
    "29192c89-2c09-4823-b5f5-fce8a5e51274": "180dcfdf-46b5-4d37-8281-45c216b75eed",
    # 34. Ochiq yotqizilgan kabellar yorliqlarida nima ko'rsatilgan bo'lishi kerak:
    "6e3ddcd1-f606-4fa0-9b7a-46975f5f4808": "1c473935-cfc8-41f9-809c-69852986ab52",
    # 35. Uskuna buzilganligi, yong'in chiqqanligi haqida tezkor xodim kimga xabar berishi kerak:
    "6a9c5d14-eb56-47ab-842a-1eac4811bc2c": "f025faea-472a-46a7-b6e4-0e632cf0b734",
    # 36. TEQ qoidalari nimalarda tatbiq etilmaydi:
    "e220ac79-2ed3-427f-bc16-a3fca573d245": "84480d69-ccf4-42b8-8bcb-4b532dda9828",
    # 37. Moy bilan tabiiy sovutiladigan transformatorlar moyining maksimal harorati:
    "2252b805-f50d-4736-88f8-08d1f62422d5": "643449b6-fb7e-4275-9731-a7fd5338bb86",
    # 38. Qanday holatlarda uskunalar yuqori turuvchi ruxsatisiz o'chirilishi/ulanishi mumkin:
    "d620aae1-edd7-4a7e-b199-4d9376e781dc": "65d2174a-1f8c-4295-9174-e83450ddb3ad",
    # 39. Quvursimon razryadlagichlarda yoy qaysi printsip asosida so'ndiriladi:
    "802c334c-4952-42b6-a966-204d3d27741d": "0afa574e-27f0-479a-b55f-b76e64bc2030",
    # 40. Uskunalar, binolar va inshoatlarni qoidalarga muvofiqligini kim ta'minlashi kerak:
    "e8689b38-0f28-4b22-814e-2d5dfdb1bd29": "e2e7ce7a-9078-42fd-ae5b-4356fd49162a",
    # 41. Ta'mirlash ishlarining davriyligi va davomiyligi nima asosida belgilanadi:
    "8109d63a-67b6-43bc-b669-a06ed012ad9c": "3d9af416-083b-442b-8cd5-d0ee584ba405",
    # 42. Elektr tarmoqlari korxonalarida transformator moyining zaxirasi:
    "296ea166-f714-4bb3-bf96-e498b0e84c61": "2b5b125d-d585-46fb-b17b-4c9fc5c6feea",
    # 43. Alohida kasblar hamda alohida turdagi ishlar uchun yo'riqnomalar qanday asosda:
    "36275295-df83-4f06-bdb3-2e06e5597573": "55c2939d-e49f-4d7a-85cc-74ff932d6bbd",
    # 44. Moyli transformatorlarda tok bo'yicha o'ta yuklama 100 foiz bo'lganda davomiyligi:
    "b1db1b77-cf7b-46ea-bd42-1c64a83ae5ff": "16401d1d-2e28-47f1-bda2-8616fb493891",
    # 45. Ekspluatatsion-ta'mirlash hujjatlari yuritilishini kim ta'minlashi kerak:
    "8b63959f-b57a-4c63-bc72-e82a8bf7a261": "88233abc-e808-4b73-b332-fa6786e4a885",
    # 46. Nima uchun laboratoriyalarga shikastlangan kabel namunalari taqdim etilishi kerak:
    "b1c4419f-9e53-4149-af8d-cce2c99ecc94": "0dbbc91f-ea41-45fb-91ba-41cb97a13ed4",
    # 47. Uskunalarni ta'mirlash uchun talabnomalar necha xil bo'ladi:
    "d71e63c0-9464-47dc-84f2-2700e5b2302e": "5f07f27c-cd5d-4cb7-ac25-87e20098a5b4",
    # 48. Ekspluatatsiya jarayonida bajarilgan o'zgartirishlar qayerga kiritiladi:
    "606636e9-fe8e-4b7a-a6dd-cbb8d54ee346": "5a861e45-87ec-41a2-acdf-698fe0f57135",
    # 49. Moyli transformatorlarda tok bo'yicha o'ta yuklama 75 foiz bo'lganda davomiyligi:
    "f9d699e6-567a-43ee-a5bb-61f533794645": "da10914b-acf1-4ca3-ae77-2c4b1c1211d4",
    # 50. Xodimlar TEQ qoidalarini buzganligi uchun nima asosida javobgar:
    "061bd0ef-2eb4-4494-b286-60dd95a9ee41": "241e56bb-af93-4465-ad05-ca32bf426cde",
    # 51. 0.4 kVli havo tarmoqlarda simning yo'lning qatnov qismigacha masofasi:
    "dc31cb11-c03c-48f4-a0cf-dd4dcd4825f7": "3a263278-19a2-438b-8e0f-ede486eea6b6",
    # 52. Har bir dispetcherlik darajasi uchun boshqarishning nechta toifasi bor:
    "d89c2b2e-557a-406b-800c-300491c9b85c": "13f84329-9384-4849-a8cb-c14bddf94741",
    # 53. Ishchi komissiyaning vazifalari nimalardan iborat:
    "9ed18c04-0b85-4c9b-8544-3753064d2419": "02c0b7a4-9a20-4b93-acd0-d047e6329814",
    # 54. Smenani qabul qilish-topshirish vaqtida tezkor xodim nimani bajarishi kerak:
    "296821d8-4cdf-46ae-91a3-82b2ea5be95d": "e8e34047-d17b-4ced-adf3-807eb44f7aba",
    # 55. Idoraviy texnik va texnologik nazoratning asosiy vazifasi:
    "30613eb9-131c-4625-8688-17654a8f5bc4": "0465546f-954b-4fc2-89c9-cdcccf537a7e",
    # 56. Energetik obektni qabul qilishda aniqlangan nuqsonlarni bartaraf etish ustidan nazorat:
    "b9bc49ce-16c9-4872-9e92-6993d0c5dcb6": "129e896f-ab03-489c-8e82-723fcf197303",
    # 57. Uskunalar ta'mirining sifati nimani hisobga olib baholanadi:
    "32045ec6-f34e-4b67-beb8-caeffc6437ad": "43abdd52-52f8-4057-9e8d-07af0608587b",
    # 58. Yo'riqnomalar, nizomlar, sxemalar ro'yxati kim tomonidan tasdiqlanadi:
    "2bfffdb8-dc29-40b9-9c36-f9a68157b428": "f37bcafd-342b-4b38-9bdb-1c3d5e9d5333",
    # 59. Uskunalarning texnik holatiga kim javobgar hisoblanadi:
    "e7e45de8-6391-4666-973c-7e34837e9015": "888fcd32-9820-45da-8a63-1dcc897aae30",
    # 60. Qoida talablari qaysi sohalarda amal qiladi:
    "28542eb5-e8a2-4ae1-b8c1-c51013ce5940": "2efe0a27-5dfe-45b5-92f3-2283c4211183",
    # 61. Yog'och tayanchlarda o'rnatiladigan erlagich simining diametri:
    "243350d6-375d-4395-ac4c-2157d54c5363": "f08e73c3-eba9-447e-9c09-a73d51465309",
    # 62. Korroziyaga qarshi qoplama qachon tiklanishi kerak:
    "f4468a79-3f62-49fe-b92a-9bf1b7b87636": "e1d9e6b4-f009-4df3-99d5-53b5c1ee747e",
    # 63. Har bir ish joyi bo'yicha lavozim yo'riqnomalarida nimalar ko'rsatilishi kerak:
    "ebc80714-8d72-4035-b3fd-9cd6c1d30b73": "72b8db69-b6ca-47c6-91e6-5d7dbb6e39eb",
    # 64. Uskunalar, binolarga xizmat ko'rsatish, ta'mirlash qayerda tashkil etiladi:
    "7bdbefa1-fadc-4f44-af31-f2781cadde3e": "1adefab0-6666-49b6-bf34-5a585d6656aa",
    # 65. Zaxiradagi uskunalarga o'tish, profilaktik ko'rik qancha muddatda:
    "1e3a0ba1-90ec-4214-8dd3-f0b4726a8767": "967a1acc-399d-41ad-a8f3-253c25cf63ae",
    # 66. Uskunani ta'mirga chiqarish uchun kim bilan kelishiladi:
    "9796c159-4f25-459a-b75b-580126f1553b": "296ff18f-0220-4910-87ef-54b776d4c14f",
    # 67. Boshqaruv organiga bevosita ta'sir ko'rsatish huquqiga ega bo'lgan ta'mirlash xodimi:
    "f498fa8e-15bd-4072-b851-90f3ae650fe9": "5d148f58-c4d0-46d0-8488-81dc22af0282",
    # 68. Gabaritni cheklovchi belgilar sozligini kim kuzatib borishi kerak:
    "77683ca7-0655-4554-a0d6-d24cb5f48ee3": "89be7922-5873-4582-9daf-01014eac5677",
    # 69. Dispetcherlar qachon shaxsiy javobgarlikka tortiladi:
    "62f89e37-1711-4cdf-8ca3-ebc4189d8fe2": "e05ddd1e-4ff8-48e1-a492-6208da11622b",
    # 70. Puflab sovutilishi o'chirilgan transformatorlarni ishlash sharoiti nima bilan belgilanadi:
    "cfe1538b-7a3f-4d53-a9fd-548c0b9890de": "8828deb9-398b-483c-930a-9311142ac626",
    # 71. Almashlab-ulash vaqtida kiritilgan o'zgarishlar qayerda aks ettiriladi:
    "514b972c-053b-4c97-9b77-403f1d22f220": "e8beb5b4-7858-4556-a4aa-f6e5a9db5018",
    # 72. Texnik-iqtisodiy ko'rsatkichlarning muntazam hisobini kim olib boradi:
    "1b6a63e4-3525-4665-a343-0bf8a60f3951": "64352a39-988a-4d69-b202-8bace1d4260a",
    # 73. Energetik obektda ishlashga kimga ruxsat beriladi:
    "3bdcc448-3a0f-4f0b-9e19-06f3c544f6ae": "2f83f4f5-d8da-4880-97dc-343273dbdeaf",
    # 74. Ikkilamchi zanjirlar izolyatsiyasining yerga nisbatan ruxsat etilgan qarshiligi:
    "3e22b536-c639-4e5a-89aa-fdbb49e9c043": "59ac89ee-ba82-4bed-8fff-5140f74684c8",
    # 75. Transformatorlarni kapital va joriy ta'mirlash qachon o'tkaziladi:
    "b0606668-277f-4a9d-8f16-c31912d34dea": "0812d49a-cf14-413f-8719-00bbc795decd",
    # 76. TEQ qoidalarini bilish va bajarish kimlar uchun majburiy:
    "7474dbc3-4c3f-4249-ae5f-e6f21a9cf856": "06b6392c-7b57-42f8-bbb0-5c0ec7fdf354",
    # 77. Barcha ish joylarida bo'lishi kerak bo'lgan yo'riqnomalar kim tomonidan imzolanadi va tasdiqlanadi:
    "9cbcc65d-aef6-4609-a93c-07ad6cc71cd6": "16e67aa4-8b24-4225-954d-d8559c0fddbc",
    # 78. Maxsus texnik ekspluatatsiya qilish qoidalari kim tomonidan joriy etiladi:
    "c191a918-7fb9-4cab-95f3-909fd10341a4": "d70cca13-b9ca-4f3c-a7ff-4644396c748f",
    # 79. Transformatorlarni o'chirmay turib ko'rikdan o'tkazish muddatlari qanday aniqlanadi:
    "0bac87d8-be73-45c7-9ba3-743bb0e3931f": "77d3a7a6-4fbc-41c9-b8df-23de61298845",
    # 80. O'lchov vositalari bilan jihozlanishi nimaga muvofiq bo'lishi kerak:
    "7f3508fe-080e-41d5-895a-1830707f2549": "8f926f97-b44a-4fc1-8906-20f86ae551ea",
    # 81. Tashkilot rahbari nima uchun shaxsiy javobgar hisoblanadi:
    "3b7b1d0f-d855-4360-902a-bde661a7065a": "03689d2b-cf10-46b5-b081-155739729ef7",
    # 82. Xar bir energetika obektida metrologik taminot:
    "47379cdc-b343-4a1e-a5ac-53819d34791d": "0d28281e-deb8-4a93-8f2b-0b414f337484",
    # 83. Xodimlarning TEQ talablariga rioya qilishlari uchun javobgar:
    "d2e7f205-50a0-49ad-ba7b-8a6f22c83235": "ffbb5040-06ce-46f4-b838-862ad85fed91", # a,b va v javoblar to'g'ri
    # 84. Xavfsiz ekspluatatsiya qilish me'yoriy hujjatlar nazorati:
    "9bc928c8-3b9b-460d-8075-0a410922d822": "e90306ab-3820-4f1d-8b73-a056b06b6fab", # “O'zenergoinspektsiya” tomonidan (VMQ-609)
    # 85. Texnik xizmat ko'rsatish va rejali tamirlash hajmi:
    "8e9f411b-1f7f-4adc-abfe-d7ba51dc16be": "8f3e5842-150e-44f2-be68-7c15bfc5594f", # amaldagi normativ hujjatlarga muvofiq (VMQ-609, 99-band)
    # 86. Elektr qurilma va uskunalarning qaysi qismi yerga/nolga ulanishi kerak:
    "c93b3e61-7b0c-48ae-867c-84c75becee4d": "26ee51b2-df18-40fb-b071-84e562e56a58", # barcha metall qismlari
    # 87. Mamuriy-texnik xodimlar tezkor xujjatlarni tekshirish muddati:
    "bb1ed6ff-d5ee-43ce-8815-58d9cbd4e71c": "8d91de1d-d186-404e-a7d8-52a86e687155", # har kuni (VMQ-609)
}

def choose_answer(question):
    # 1. Bilimlar bazasi yoki tasdiqlangan javoblar (100% ishonch)
    known = VERIFIED_ANSWERS.get(question.id) or kb.get_known_answer(question.id)
    if known:
        return known, "Tasdiqlangan bilimlar bazasi (100%)"

    # 2. Nazariya matnidan so'zma-so'z qidirish (100% ishonch)
    # Agar savol nazariyasida variant so'zma-so'z mavjud bo'lsa
    # (Bazada tasdiqlangan bo'lmagan holatda taxmin qilish mutlaqo taqiqlangan)

    # FOYDALANUVCHI TALABI: O'zingdan taxmin qilma! Faqat bazada mavjud bo'lsa ishla!
    # Hech qanday evristika, eng uzun variant yoki taxminiy variant tanlanmaydi!
    return None, "Bazada mavjud emas (Taxmin qilish taqiqlangan)"

def wait_for_energy(context_msg: str = ""):
    """Energiya (heartsCount) 0 bo'lsa, aniq tiklanish soniyasigacha kutish va tiklangach Telegramga xabar berish"""
    was_sleeping = False
    while True:
        try:
            me_data = client.base_client.get('/progress/me')
            hearts = me_data.get('hearts', {})
            cur_hearts = hearts.get('heartsCount', 0)
            if cur_hearts > 0:
                if was_sleeping:
                    # Energiya tiklangani haqida Telegramga xabarnoma
                    send_telegram_alert(
                        f"⚡ <b>ENERGIYA TIKLANDI ({cur_hearts}/5)!</b>\n\n"
                        f"{context_msg}\n"
                        f"🚀 <i>Testlarni yechish qayta boshlandi...</i>"
                    )
                return cur_hearts
            
            was_sleeping = True
            regen_str = hearts.get('nextRegenAt', '')
            if regen_str:
                regen_dt = datetime.fromisoformat(regen_str.replace("Z", "+00:00"))
                now_dt = datetime.now(timezone.utc)
                wait_sec = max(5, int((regen_dt - now_dt).total_seconds()) + 5)
                local_time = format_tashkent_time(regen_str)
                wait_min = max(1, round(wait_sec / 60))
                log_print(f"\n[ENERGIYA 0/5] Tiklanish vaqti: {local_time} ({wait_min} daqiqa). Kutish boshlandi...")
                time.sleep(wait_sec)
            else:
                log_print("[!] Energiya 0/5, 60 soniya kutilmoqda...")
                time.sleep(60)
        except Exception as e:
            log_print(f"[!] Energiya tekshirishda xatolik: {e}. 30 soniya kutilmoqda...")
            time.sleep(30)

def solve_theory(t, idx, total_theories, level_title=""):
    log_print(f"\n=======================================================")
    log_print(f"MODUL {idx}/{total_theories}: '{t.title}' ({t.answered_questions}/{t.total_questions})")
    log_print("=======================================================")

    retry_mode = False

    while True:
        mode = "retry" if retry_mode else "continue"
        try:
            q_data = client.progress.get_theory_questions(t.id, mode=mode)
        except Exception as e:
            log_print(f"[!] Savollarni olishda xatolik: {e}. 5 soniya kutilmoqda...")
            time.sleep(5)
            continue

        questions = q_data.get("questions", [])
        is_mod_complete = q_data.get("is_module_complete", False)
        answered_count = q_data.get("answered_count", 0)
        total_q = q_data.get("total_questions", 0)

        log_print(f"  [Holat]: {answered_count}/{total_q} ta yechildi. Qolgan savollar paketi: {len(questions)} ta")

        if is_mod_complete or not questions:
            if not retry_mode and answered_count < total_q:
                log_print(f"  [>] Retry rejimiga o'tilmoqda (xatolarni qayta yechish)...")
                retry_mode = True
                time.sleep(2)
                continue
            else:
                log_print(f"\n[+] MODUL {idx} 100% YAKUNLANDI ({answered_count}/{total_q})!")
                send_telegram_alert(
                    f"🎉 <b>MODUL 100% YAKUNLANDI!</b>\n\n"
                    f"📖 <b>Modul {idx}:</b> {t.title}\n"
                    f"📊 <b>Natija:</b> {answered_count}/{total_q} ta to'g'ri yechildi!\n"
                    f"Keyingi modulga o'tilmoqda..."
                )
                break

        for q in questions:
            try:
                client.auth.send_heartbeat()
            except Exception:
                pass

            context_info = (
                f"🎯 <b>Daraja:</b> {level_title}\n"
                f"📖 <b>Modul {idx}:</b> {t.title}\n"
                f"📊 <b>Joriy holat:</b> {answered_count}/{total_q} ta savol yechilgan."
            )

            # Har bir savol oldidan energiya tekshirish
            cur_hearts = wait_for_energy(context_msg=context_info)

            opt_id, source_reason = choose_answer(q)
            if not opt_id:
                log_print(f"\n[!] DIQQAT: Savol bazada topilmadi: '{q.prompt[:70]}...'")
                log_print("    Foydalanuvchi buyrug'iga ko'ra taxmin qilish qat'iyan taqiqlangan.")
                log_print("    Energiya yo'qotmaslik uchun test jarayoni to'xtatildi.")
                send_telegram_alert(
                    f"⚠️ <b>SAVOL BAZADA TOPILMADI</b>\n\n"
                    f"❓ <b>Savol:</b> {q.prompt[:150]}\n\n"
                    f"⛔ <i>Energiya yo'qotmaslik uchun test to'xtatildi. Taxmin qilinmadi.</i>"
                )
                break

            time.sleep(1.8)

            try:
                res = client.progress.submit_answer(q.id, opt_id, source="LESSON")
            except Exception as e:
                log_print(f"  [!] Submit xatosi: {e}. 3 soniya kutilmoqda...")
                time.sleep(3)
                continue

            if res.is_correct:
                h_val = res.hearts.get('heartsCount') if isinstance(res.hearts, dict) else res.hearts
                log_print(f"  [+] TO'G'RI! (+{res.xp_earned} XP, Energiya: {h_val}/5)")
                VERIFIED_ANSWERS[q.id] = opt_id
                kb.record_answer(q.id, q.prompt, opt_id, opt_text)
            else:
                correct_id = res.correct_option_id
                correct_text = next((o.option_text for o in q.options if o.id == correct_id), correct_id)
                log_print(f"  [-] Noto'g'ri. Server to'g'ri javobi aniqlandi: '{correct_text[:45]}'")
                if correct_id:
                    VERIFIED_ANSWERS[q.id] = correct_id
                    kb.record_answer(q.id, q.prompt, correct_id, correct_text)
                
                # Agar ushbu xato javobdan keyin energiya 0 bo'lib qolgan bo'lsa, Telegramga to'liq tafsilot bilan xabar yuborish
                try:
                    me_after = client.base_client.get('/progress/me')
                    h_after = me_after.get('hearts', {})
                    if h_after.get('heartsCount', 0) <= 0:
                        regen_iso = h_after.get('nextRegenAt', '')
                        local_regen_time = format_tashkent_time(regen_iso)
                        wait_sec = 0
                        if regen_iso:
                            reg_dt = datetime.fromisoformat(regen_iso.replace("Z", "+00:00"))
                            now_utc = datetime.now(timezone.utc)
                            wait_sec = max(0, int((reg_dt - now_utc).total_seconds()))
                        wait_min = max(1, round(wait_sec / 60))

                        # Telegramga xato va energiya haqida bildirishnoma
                        send_telegram_alert(
                            f"⚠️ <b>XATO JAVOB VA ENERGIYA TUGADI (0/5)!</b>\n\n"
                            f"📖 <b>Modul:</b> {t.title} ({answered_count}/{total_q})\n\n"
                            f"❓ <b>Savol:</b>\n<i>{q.prompt}</i>\n\n"
                            f"❌ <b>Berilgan javob:</b> {opt_text}\n"
                            f"✅ <b>To'g'ri javob (Server):</b> {correct_text}\n\n"
                            f"📚 <i>Ushbu to'g'ri javob bilimlar bazasiga saqlandi, keyingi safar qayta xato qilinmaydi.</i>\n\n"
                            f"⏰ <b>Keyingi energiya ochilish vaqti:</b> {local_regen_time} (taxminan {wait_min} daqiqadan so'ng)."
                        )
                except Exception as ex:
                    log_print(f"[!] Telegram xabarnoma yuborishda xatolik: {ex}")

                # Energiya tugagach, kutish rejimiga o'tish
                wait_for_energy(context_msg=context_info)

            time.sleep(1.2)

def solve_daily_plan_priority():
    """
    1-QOIDASI: Energiya tiklanganda BIRINCHI NAVBATDA kunlik rejani (10 ta test) 100% yechish,
    faqat kunlik reja to'liq yakunlangach, asosiy darajalar testlariga o'tish.
    """
    try:
        plan = client.daily_plan.get_today()
    except Exception as e:
        log_print(f"[!] Kunlik reja holatini olishda xatolik: {e}")
        return

    if not plan.is_plan_day:
        return

    if plan.completed or plan.completion_percent >= 100:
        return

    total_target = plan.target_questions or 10
    log_print("\n" + "=" * 60)
    log_print(f"🎯 BIRINCHI NAVBATDA KUNLIK REJA YECHILMOQDA ({plan.answered_count}/{total_target})")
    log_print("=" * 60)

    while True:
        try:
            cur_plan = client.daily_plan.get_today()
            if cur_plan.completed or cur_plan.completion_percent >= 100 or cur_plan.answered_count >= total_target:
                log_print(f"\n🎉 KUNLIK REJA 100% YAKUNLANDI! (+100 XP)")
                send_telegram_alert(
                    f"🎉 <b>KUNLIK REJA 100% YAKUNLANDI!</b>\n\n"
                    f"✅ <b>Natija:</b> {cur_plan.answered_count}/{total_target} ta test yechildi!\n"
                    f"🎁 <b>Bonus:</b> +100 XP olindi!\n\n"
                    f"Endi asosiy daraja testlarini yechishga o'tilmoqda..."
                )
                break
        except Exception:
            pass

        try:
            client.auth.send_heartbeat()
        except Exception:
            pass

        context_info = f"🎯 <b>Kunlik reja testlari yechilmoqda...</b>"
        cur_hearts = wait_for_energy(context_msg=context_info)

        question = client.daily_plan.get_next_question()
        if not question:
            log_print("Kunlik reja uchun boshqa savol topilmadi.")
            break

        opt_id, source_reason = choose_answer(question)
        if not opt_id:
            log_print(f"\n[!] DIQQAT (Kunlik reja): Savol bazada topilmadi: '{question.prompt[:70]}...'")
            log_print("    Foydalanuvchi buyrug'iga ko'ra taxmin qilish qat'iyan taqiqlangan.")
            log_print("    Energiya yo'qotmaslik uchun test jarayoni to'xtatildi.")
            send_telegram_alert(
                f"⚠️ <b>KUNLIK REJA SAVOLI BAZADA TOPILMADI</b>\n\n"
                f"❓ <b>Savol:</b> {question.prompt[:150]}\n\n"
                f"⛔ <i>Energiya yo'qotmaslik uchun test to'xtatildi. Taxmin qilinmadi.</i>"
            )
            break

        time.sleep(1.8)

        try:
            res = client.progress.submit_answer(question.id, opt_id, source="DAILY_PLAN")
        except Exception as e:
            log_print(f"  [!] Submit xatosi: {e}. 3 soniya kutilmoqda...")
            time.sleep(3)
            continue

        if res.is_correct:
            h_val = res.hearts.get('heartsCount') if isinstance(res.hearts, dict) else res.hearts
            log_print(f"  [+] TO'G'RI! (+{res.xp_earned} XP, Energiya: {h_val}/5)")
            VERIFIED_ANSWERS[question.id] = opt_id
            kb.record_answer(question.id, question.prompt, opt_id, opt_text)
        else:
            correct_id = res.correct_option_id
            correct_text = next((o.option_text for o in question.options if o.id == correct_id), correct_id)
            log_print(f"  [-] Noto'g'ri. Server to'g'ri javobi aniqlandi: '{correct_text[:45]}'")
            if correct_id:
                VERIFIED_ANSWERS[question.id] = correct_id
                kb.record_answer(question.id, question.prompt, correct_id, correct_text)
            
            try:
                me_after = client.base_client.get('/progress/me')
                h_after = me_after.get('hearts', {})
                if h_after.get('heartsCount', 0) <= 0:
                    regen_iso = h_after.get('nextRegenAt', '')
                    local_regen_time = format_tashkent_time(regen_iso)
                    wait_sec = 0
                    if regen_iso:
                        reg_dt = datetime.fromisoformat(regen_iso.replace("Z", "+00:00"))
                        now_utc = datetime.now(timezone.utc)
                        wait_sec = max(0, int((reg_dt - now_utc).total_seconds()))
                    wait_min = max(1, round(wait_sec / 60))

                    send_telegram_alert(
                        f"⚠️ <b>KUNLIK REJADA XATO VA ENERGIYA TUGADI (0/5)!</b>\n\n"
                        f"❓ <b>Savol:</b>\n<i>{question.prompt}</i>\n\n"
                        f"❌ <b>Berilgan javob:</b> {opt_text}\n"
                        f"✅ <b>To'g'ri javob (Server):</b> {correct_text}\n\n"
                        f"⏰ <b>Keyingi energiya tiklanish vaqti:</b> {local_regen_time} (taxminan {wait_min} daqiqa)."
                    )
            except Exception:
                pass

            wait_for_energy(context_msg=context_info)

        time.sleep(1.2)

def solve_level(level_id: str, level_title: str):
    log_print(f"\n#######################################################")
    log_print(f"   DARAJA BOSHLANDI: {level_title} (ID: {level_id})")
    log_print(f"#######################################################")
    detail = client.progress.get_level_detail(level_id)
    total_theories = len(detail.theories)

    for idx, t in enumerate(detail.theories, 1):
        if t.is_complete:
            log_print(f">> MODUL {idx}/{total_theories}: '{t.title}' allaqachon 100% bajarilgan.")
            continue
        solve_theory(t, idx, total_theories, level_title=level_title)

    send_telegram_alert(f"🎉 <b>DARAJA 100% YAKUNLANDI!</b>\n«{level_title}» muvaffaqiyatli topshirildi!")

def run_perpetual_autopilot():
    log_print("=" * 60)
    log_print("   ELEKTROLEARN DOIMIY (PERPETUAL) AVTOPILOT TIZIMI ISHGA TUSHDI   ")
    log_print("=" * 60)

    while True:
        try:
            # 1-QADAM: Birinchi navbatda kunlik rejani (10 ta savol) yechish!
            solve_daily_plan_priority()

            # 2-QADAM: Kunlik reja bajarilgach, asosiy daraja testlariga o'tish!
            prog = client.progress.get_progress()
            target_level = None

            for lvl in prog.levels:
                if not lvl.is_locked and (not lvl.is_completed or lvl.completion_percent < 100):
                    target_level = lvl
                    break

            if not target_level:
                log_print("\n[!] Barcha ochiq darajalar 100% yakunlandi!")
                log_print("Yangi darajalar qulflari ochilishini tekshirish uchun 5 daqiqa kutilmoqda...")
                time.sleep(300)
                continue

            log_print(f"\n[>>>] Maqsadli daraja: {target_level.title} (Progress: {target_level.completion_percent}%)")
            solve_level(target_level.id, target_level.title)

            time.sleep(3)
        except Exception as e:
            log_print(f"[!] Asosiy tsiklda kutilmagan xatolik: {e}. 10 soniya kutilmoqda...")
            time.sleep(10)

if __name__ == "__main__":
    run_perpetual_autopilot()
