import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Complete verified map for all 39 questions of Test 1
VERIFIED_TEST1 = {
    # 1. Naryad muddatini kim uzaytirishi mumkin?
    "ff56b045-9222-4c2a-99b8-6d77e9fcc9d5": "3e375a79-fb30-4b48-ab29-0de1e2db723b",
    # 2. Brigada tarkibini o‘zgartirish haqidagi ko‘rsatma kimga va qanday beriladi?
    "29a40e8d-c11b-4f80-9de6-acf1fb55aa9b": "de3d4538-182b-41d1-9462-3caa09640453",
    # 3. Texnologik sxemalar (chizmalar) qancha muddatda tekshirilishi kerak?
    "62579c02-53bc-4de1-8af0-db8d5bca9ba7": "172d67c2-0840-4269-bb01-1c7546cf8a21",
    # 4. Quvursimon razryadlagichlarda yoy qaysi prinsip asosida so‘ndiriladi?
    "398f5c26-aaab-49f5-9d3d-04b560dabd75": "93377a82-f0f5-4644-9c29-c0003c407b5c",
    # 5. Havo elektr uzatish tarmoqlarini gabaritlari qanday asboblar yordamida o‘lchanadi?
    "d24614af-3daf-4e98-8984-b4632ce32c7b": "421d5540-cca3-4b42-80c2-d9cba235037f",
    # 6. "Ish joyidagi yo‘riqnomalarni qayd qilish jurnali" qancha muddat saqlanadi?
    "aae7baad-8930-41f2-aafe-a15f135b4c85": "e11767f0-0767-48f4-9631-3529c23ab71c",
    # 7. Ximoya vositalarini qayd qilish jurnali qancha muddatda va kim tomonidan nazorat qilinishi kerak?
    "3397d8c7-572f-4ebf-b310-c95ce8e2caef": "f417052c-044c-4f87-a2f8-bc2f084da557",
    # 8. Ximoya vositalari ro‘yxati kim tomonidan tasdiqlanadi?
    "ff9c8ca5-5579-4906-9649-96f75af88e23": "ec9deda2-ca87-46f6-8cad-a7c889235b70",
    # 9. Ichimlik sodasi va bor kislotasining eritmalari qaysi ish joylarida bo‘lishi kerak?
    "cb4bf2e1-f8a4-49ef-9ec8-0b9957078bcb": "2f2997d6-4fa4-44c6-aed8-87eefb49d8ea",
    # 10. Quvursimon razryadlagichlar qanday burchak ostida o‘rnatiladi?
    "738dd04a-9ea4-4a32-9ec3-736abdb4ee28": "a6eb7ec9-7fc3-45e2-ba53-03fd660f0909",
    # 11. Jabrlangan shaxsga birinchi yordam ko‘rsatish maqsadga muvo-fiqligini kim xal qiladi?
    "222d4b44-b1da-413d-8082-3a4ef2bf1f4d": "9d40cca5-9aff-43f3-8206-19018e5b9fd2",
    # 12. Ish rahbari ish joyi tayyorligini kim bilan birga tekshi-radi?
    "f3779e08-15a9-4857-9f40-100b42bb12a7": "52618f91-1787-455b-aeb3-0b08ba77dd2e",
    # 13. Energetika tashkilotlarida yong‘in xavfsizligini ta’minlash uchun mas’uliyat kimga yuklatiladi?
    "70a81c14-de9e-4e53-a275-e63f61abb42e": "7ced5841-9fa4-48e7-b02b-5a52f820a09c",
    # 14. Ximoya vositalarini elektr sinovlaridan oldin nima qilish kerak?
    "692e8d9b-5f8a-4a75-8aec-912e9a9fc32b": "9add9c17-d7b2-43d7-b409-c6165c73e368",
    # 15. Yordam ko‘rsatayotgan shaxs nimalarni bilishi kerak?
    "6171afa1-c406-4a0f-b1d8-2f1eb163a753": "d35eed4e-96a7-4829-987d-c18d651b758f",
    # 16. Energetika uskunalarini boshqarishga, texnik xizmat ko‘rsa-tishga yoki ta’mirlashga kimga ruxsat etiladi?
    "e381c620-c49e-4475-9710-e9b4f2aab9a6": "3bf1aff2-6710-4264-9ac6-133471909c24",
    # 17. Bir dona ulama qism (pasinka) bandaj qilishda simning uzunligi qaysi formula yordamida aniqlanadi
    "c1f6df3b-6267-4d9a-846c-e662c97c0a4e": "17d88601-d89b-4299-8615-75fae15be04e",
    # 18. Ma’muriy-texnik xodimlar tezkor xujjatlarni qancha mud-datda tekshirib turishi kerak?
    "ce38fcae-adc1-48b0-8746-c9d218e45493": "6cd3ba87-a1f5-42f3-9e42-f1e0bd18f0af",
    # 19. Bir ish raxbariga beriladgan naryadlar sonini kim belgilay-di?
    "26dd3f93-dd11-410c-aabe-6e5eeb93bf82": "cfc87562-6cbc-44fb-8b53-4cab0a663614",
    # 20. Brigada a’zolari soni va uning tarkibi nimaga asosan belgi-lanadi?
    "d71fba6d-7547-4234-b5dd-9c6c96887d96": "d10215ed-936a-4221-af1d-570726ed0901",
    # 21. Energetika moylarni ekspluatatsiya qilganda nima ta’min-lanishi kerak?
    "22cd75a1-f844-49d6-a4e2-ce8b34cd376a": "478c4162-39dd-42c1-82ff-caffbd89a8ef",
    # 22. Navbatdan tashqari yo‘riqnoma qachon o‘tkaziladi?
    "6a190ce2-3b0a-4bed-80bd-220a60d15cd1": "7b943982-7ffc-42d8-8221-0d9ab90d2696",
    # 23. Sexlar, laboratoriyalar, bo‘limlar, ustaxonalar va boshqa ob’-yektlarning yong‘in xavfsizligi holati uchun kim javobgar xisoblanadi?
    "bd7b48ee-280a-4833-a241-3eb9bb13179c": "d1b8e115-6c34-41c3-8a98-bf392eb200e4",
    # 24. Ish joyini tayorlash va ishga qo‘yish qachon amalga oshiriladi?
    "75175a38-75ea-48f8-92e7-e4652c41d161": "cc9733f5-2f87-4951-a35c-c38324d3ad53",
    # 25. Ta’mirlash va sozlash xodimlarining mustaqil ishlashiga qachon ruxsat beriladi?
    "3b8003e6-bb5b-4b8d-8369-75c141f854f4": "8a6958bb-a741-4c64-8b46-2b88d872cb61",
    # 26. Yong‘in xavfsizligi bo‘yicha yo‘riqnomalar kim tomonidan tas-diqlanadi?
    "3c944c45-3187-4955-a5a2-df39d99f54d1": "d1da3cc5-7a91-41b7-8124-36ac8349a401",
    # 27. Energetika ob’ektlarini normal ekspluatatsiya kilish uchun kim javobgar?
    "d09f0590-76d2-4b48-ae92-e52ba53457cf": "d5175f53-e48e-40fc-b6eb-9dfb566ea9a8",
    # 28. Elektrostansiya va podstansiya elektr qurilmalarini yakka o‘zi ko‘rib chiqish xuquqi kimlarga beriladi ?
    "baa1eb3f-09f6-4741-bf2f-610d809ab121": "5faa22ce-16e6-4107-8b76-a2b936dc2e0f",
    # 29. Ximoya vositalarini qanday temperaturada sinovdan o‘tkazila-di?
    "47ebe259-1050-4fa2-81e5-5205757db4e4": "c60c46d6-8452-48b7-9328-09c1c9c1b931",
    # 30. KMT brigadasi ishlayotgan HL uchastkasiga yerga ulagichni kim o‘rnatishi va olib tashlashi mumkin?
    "5f219d64-b958-4737-9208-32e6d5fd1dc5": "e785ae69-8208-4f3a-9444-ce842240d63f",
    # 31. Suzayotgan odamning boldir mushaklarida tomir tortishib qolsa nima kilish tavsiya etiladi?
    "68acd467-bde6-440a-8dd3-f63ba68760d5": "2bf9c8ca-1075-4bd6-9492-94408a4ae642",
    # 32. Naryad yoki farmoyish beruvchining javobgarligi nimadan ibo-rat?
    "b7554977-aeb0-4e72-a2db-bb75f06b1837": "c7ba92b0-60b5-43e7-bf59-064b5befda4e",
    # 33. Uskunalarni ta’mirlash uchun talabnomalar necha xil bo‘ladi?
    "04b605dd-7f36-4ad3-9384-cc582a39cf4d": "89dc52b4-9d61-42bc-bb2e-f793e5ddcbde",
    # 34. Korxona rahbariyatining yozma ko‘rsatmasi bilan o‘z xodimlar-iga qaysi huquqlarni berish rasmiylashtiriladi?
    "2732995e-f9b1-400d-8aea-02f7be260aef": "744dcf63-bf4e-4dc5-9ce4-7f534fe6af87",
    # 35. Elektr stansiyalari, qozonxonalar, elektr va issiqlik sohalarining asosiy vazifasi nimadan iborat?
    "77847795-d97e-4056-8e87-dbe0a78ab0dc": "ec3a0ed5-586e-4cdb-a4da-33fcfe5ad19d",
    # 36. Kaysi holatlarda zarb bilan ishlaydigan mashina va mexa-nizmlarning kabel trassalarida ishlashiga ruxsat berilmaydi?
    "9c87cc0a-db3e-4653-a1cd-040edc805f52": "3de7b8fc-d446-44a7-8491-3cb14425db03",
    # 37. Ish rahbarining javobgarligi nimadan iborat?
    "a0781306-c7f0-49fc-8b04-9126ee3a2726": "467b09b0-4b28-4f3a-a88b-1d49c623572f",
    # 38. Yong‘in xavfsizligi bo‘yicha yo‘riqnomalar qancha muddatda qay-ta ko‘rib chiqilishi kerak?
    "b23951bb-1627-496b-af40-84a8c64ced51": "c9e97470-efae-4579-987c-2255649b52fe",
    # 39. Quyida sanab o‘tilganlardan qaysi birida navbatdan tashqari bilim sinovi o‘tkaziladi?
    "a122dd29-129d-4bff-b934-685a9e929e3f": "f15e09d5-ad27-45e6-b504-0084ad059dc6",
}

print(f"Total verified answers in solver: {len(VERIFIED_TEST1)}")

theory_id = "62ff9db9-4545-4944-9a7b-27de8e31b522"

submitted_count = 0
while True:
    # Check energy
    me = client.base_client.get("/progress/me")
    hearts = me.get("hearts", {})
    cur_hearts = hearts.get("heartsCount", 0)
    if cur_hearts <= 0:
        print("\n[STOP] Energiya tugadi (0/5). To'xtatildi.")
        break
        
    q_data = client.progress.get_theory_questions(theory_id, mode="continue")
    questions = q_data.get("questions", [])
    remaining = q_data.get("remaining_count", 0)
    total = q_data.get("total_questions", 40)
    answered = q_data.get("answered_count", 0)
    
    if remaining == 0 or len(questions) == 0:
        print(f"\n[MUVAFFAQINAT!] Test № 1 to'liq yakunlandi! ({answered}/{total})")
        break
        
    # Pick first question that is in VERIFIED_TEST1
    target_q = None
    target_opt = None
    for q in questions:
        if q.id in VERIFIED_TEST1:
            target_q = q
            target_opt = VERIFIED_TEST1[q.id]
            break
            
    if not target_q:
        print("\n[OGOHLANTIRISH] Hozirgi darchadagi savollar bazada yo'q! Kutish yoki to'xtatish...")
        break
        
    # Get option text
    opt_text = ""
    for opt in target_q.options:
        if opt.id == target_opt:
            opt_text = opt.option_text
            break
            
    submitted_count += 1
    print(f"\n[{submitted_count}] Savol yechilmoqda (Qolgan: {remaining}):")
    print(f"  ID: {target_q.id}")
    print(f"  Savol: {target_q.prompt[:70]}...")
    print(f"  Tanlangan javob: [{target_opt}] {opt_text[:70]}...")
    
    res = client.progress.submit_answer(
        question_id=target_q.id,
        selected_option_id=target_opt,
        source="LESSON"
    )
    
    print(f"  Natija: Correct={res.is_correct}, Hearts={res.hearts}")
    
    if res.is_correct:
        kb.record_answer(
            question_id=target_q.id,
            prompt=target_q.prompt,
            correct_option_id=target_opt,
            option_text=opt_text
        )
        print("  -> Bilimlar bazasiga (knowledge_base.json) saqlandi.")
    else:
        print("  -> DIQQAT: XATO JAVOB! Jon yo'qotmaslik uchun to'xtatildi!")
        break
        
    time.sleep(2.0)

print("\n--- Yakuniy holat ---")
final_me = client.base_client.get("/progress/me")
print("Hearts:", final_me.get("hearts"))
