import json
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# Barcha aniqlangan to'liq savollar va javoblar
EXTRA_METADATA = {
    "a99c6535-d259-4cac-a65d-3f37303c37d1": {
        "prompt": "Yong'inni o'chirish tezkor varaqalari nima maqsadda ishlab chiqiladi?",
        "correct_option_id": "4b7603ed-b05c-4bc9-a41b-120c806de4d2",
        "option_text": "yong'in sodir bo'lganda xodimlarning oqilona harakatini ta'minlash va vaqtini qisqartirish maqsadida yong'in o'chirish tezkor varaqalari ishlab chiqiladi"
    },
    "a5f17128-6927-43f9-80d2-d0b1d880c7e9": {
        "prompt": "Yong'in o'chog'ini birinchi bo'lib payqagan xodimning xarakati kanday bo'lishi kerak?",
        "correct_option_id": "959723e7-359e-403b-a035-7ef6dcccc249",
        "option_text": "xodim zudlik bilan yuqori turuvchi raxbarga yoki tezkor xodimga yong'in sodir bo'lgan joy haqida habar berishi hamda xavfsizlik choralarini ko'rgan holda mavjud yong'in o'chirish vositalari bilan yong'inni o'chirishga kirishishi shart."
    },
    "23aa6d72-c59a-4f2e-b610-bd2a6ecc6e0c": {
        "prompt": "To'liq og'irligi 15 kg dan kam bo'lgan o't o'chirgichlar polga nisbatan qanday joylashtirilishi kerak?",
        "correct_option_id": "13859d0a-a8a7-4c7e-bbe3-0dcd22884ec0",
        "option_text": "uning yuqori qismi poldan 1,5 m dan ko'p bo'lmagan balandlikda joylashishi shart."
    },
    "e1f74cc1-1501-4d5b-b5ca-89d961963bb5": {
        "prompt": "Tezkor-chiqish brigadasi avtomobillarida nechta o't o'chirgich bo'lishi shart?",
        "correct_option_id": "7066b18d-8169-4de4-96a6-9d76f7c7ad19",
        "option_text": "har birining og'irligi 5 kg dan kam bo'lmagan kamida to'rtta karbonat kislota-li va kukunli o't o'chirgichlar bo'lishi shart."
    },
    "bc465158-a89d-4ea8-a498-d3f35e55e257": {
        "prompt": "Yong'in xavfsizligi bo'yicha yo'riqnomalar kim tomonidan tas-diqlanadi?",
        "correct_option_id": "d195240d-59ac-4fad-9e7e-4a3180593804",
        "option_text": "tashkilot bosh muxandisi tomonidan."
    },
    "27cdd0b4-de87-4928-bc7d-9289d066c06a": {
        "prompt": "Tashkilotlarda ko'ngilli yong'inni o'chirish drujinasi nima uchun tashkil etiladi?",
        "correct_option_id": "c863fd56-98e3-455d-bcfd-58099baef955",
        "option_text": "tashkilotlarda yong'inga qarshi rejimni yaxshilash, yong'inni o'chirishning birlamchi vositalari holatini nazorat qilish va yuzaga kelgan o't olish va yong'inlarni o'chirishni tashkil qilishni takomillashtirish buyicha chora-tadbirlarni o'tkazish uchun ko'ngilli yong'inni o'chirish drujinasi tashkil qilinadi"
    },
    "03aae28d-ecaf-4642-9f36-5a00c4aa55ca": {
        "prompt": "Tashkilot rahbari yong'in-texnik komissiyasi va ko'ngilli yong'in-ni o'chirish drujinasi tavsiyalarini qancha muddatda eshitadi?",
        "correct_option_id": "f2c5622e-bdf3-4db7-9301-b7830f5ddc2b",
        "option_text": "kamida 6 oyda bir marta eshitadi."
    },
    "63605e75-f4cb-4033-973e-68f4705920f5": {
        "prompt": "Rele himoyasi panellari kim tomonidan ko'rikdan o'tkazilishi kerak? (Qayta ulovchi uskunalar holati va sinov bloklari qopqoqlari to'g'riligini aniqlash uchun).",
        "correct_option_id": "386fae74-140a-4814-b21a-85c57278ad9e",
        "option_text": "RHA xizmati va ETL xodimlari."
    },
    "094ede35-8577-470f-b1e6-5511386c8685": {
        "prompt": "Rele apparatlarini va yordamchi uskunalarini ochish huquqiga - Kim ega? (O'rnatmasi tezkor xodimlar tomonidan o'zgartiriladiganlardan tashqari).",
        "correct_option_id": "1d174831-7d25-4357-96e9-b3d27c6c717c",
        "option_text": "RHA va ETL xodimlari hamda ularning topshirig'iga asosan tezkor xodimlar."
    }
}

for q_id, item in EXTRA_METADATA.items():
    kb.record_answer(q_id, item["prompt"], item["correct_option_id"], item["option_text"])

# KB holatini tekshirish
with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

qs = data.get("questions", {})
print(f"Jami to'liq saqlangan savollar soni: {len(qs)} ta")
empty_count = sum(1 for v in qs.values() if not v.get("prompt") or not v.get("option_text"))
print(f"Tugallanmaganlar soni: {empty_count} ta (0 bo'lishi kerak)")

