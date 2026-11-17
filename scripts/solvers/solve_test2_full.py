import sys
import os
import time
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Complete verified map for all 40 questions of Test 2
VERIFIED_TEST2 = {
    # 1. Xodimlar bilan ishlash uchun javobgarlik kimning zimmasiga yuklatilgan?
    "20734064-a4e7-4ffa-9e7a-3519d8350480": "2c7a22fc-d4fa-48a2-841a-123edc93ac49",
    # 2. Ishga yaroqsiz deb topilgan himoya vositasining eski shtampi nima qilinadi?
    "b7db9c13-e3b5-47da-aebd-e3b6241e6528": "9a4bf1c0-8639-4dbb-946e-09ab392f4756",
    # 3. Tayyorlangan ish joyiga kelgusi kunlarda brigadani ishga qo‘yish kim tomonidan amalga oshirishladi?
    "7d06e4f4-7dfd-4a53-a5ba-4e30807beb03": "1f7a41ed-3384-4658-b47d-1bb66c2547bf",
    # 4. RTV-10-0.5/2,5U1, RTV-10-2/10U1 markali quvursimon razryadlagichlarda tashqi uchqun oralig‘i (iskroviy promejutok) masofasi qancha bo‘ladi?
    "42324579-e053-4e8c-aa66-cdf2d2e05003": "2906a52d-6aca-426d-92d0-e7651504a958",
    # 5. Yong‘in-texnik minimumi mashg‘ulotlari kimlar bilan o‘tkazi-ladi?
    "b8c94e7a-cc1d-43db-a877-7f6823416ae7": "4a8c759e-5235-486d-9ed9-18c697d4abb5",
    # 6. Dublyorlikdan kimlar va qaysi holatlarda o‘tadi?
    "9fc6440c-e6ec-47ef-8d9b-90890ae1356c": "cd48b4cf-6537-4e2f-9aa6-4d209052e765",
    # 7. Ish joyini tayorlashga va ishga qo‘yishga ruxsat kimga va qan-day beriladi?
    "c4a2c813-ba81-480b-9ebc-0e05dbfa49de": "ecbb7417-0265-4874-9ac3-42b48f283ac6",
    # 8. Naryad va farmoyishlar bo‘yicha bajariladigan ishlarni xi-sobga olish jurnali to‘lgandan keyin qancha muddat saqlanadi?
    "c5deb709-2563-4a15-9166-f082a052042b": "9b42ad96-fc2b-4048-9e9f-dc71de355748",
    # 9. Ximoya vositalarining sinovdan o‘tkazilganligi qaerda qayd qilinadi?
    "789dc55c-b439-4824-b31c-44d11b62670f": "0854dbc6-cf5b-4d51-a03a-d000d493e10a",
    # 10. Xodisa ro‘y bergan joyga tibbiyot xodimlarini chaqirish imko-ni bo‘lmasa nima qilish kerak?
    "e5b07a98-7f4b-4664-b509-cfb212aed6ad": "d93f2901-e2b3-4955-9d45-7b2515648e6e",
    # 11. Moy bilan tabiiy sovutiladigan transformatorlar moyining yuqori katlamlarida ruxsat etilgan maksimal haroratini ko‘rsating?
    "3cbbd046-2f39-442e-a712-929f762cc57a": "6b57781c-ed04-4315-a89a-c5ef76e83490",
    # 12. Ish joyini tayyorlashga va ishlashga ruxsat etgan yoki uni o‘rni-ni almashtirgan shaxsning ruxsatini (farmoyishini) olmasdan elektr qurilmani elektr tarmoqqa ulash mumkinmi?
    "63f20de0-9b86-4481-9d3c-92130502d366": "82e59af9-a093-4d72-85be-8704517fb348",
    # 13. Tuman tarmoqlari dispetcherida qaysi hujjatlar bo‘lishi shart?
    "5ba31600-e4b1-468a-a888-a1df954e135c": "c0aa688e-cf40-4749-bf5c-a297aa75c012",
    # 14. Qanday holatlarda yuqori turuvchi xodim farmoyishini baja-rish taqiqlanadi?
    "dbda2b0a-36fa-4036-b89e-3ef93126a6f4": "436d2ca0-33c3-4fc9-ba91-03607dc33cb2",
    # 15. Tayyorlangan ish joyiga kelgusi kunlarda brigadani qayta ishga qo‘yish naryadda qanday rasmiylashtiriladi.
    "1186b572-8166-4474-8a41-ebe7fdd26bb0": "0527690a-7fee-4275-b80d-5a2fb22ada20",
    # 16. Avariya holatlarida ta’mirlashga chiqarilgan elektr quril-mani yoki elektr uskunani tarmoqga ulash mumkinmi?
    "e446306f-f6b6-420a-8e94-b790c6a7b768": "c493d784-8c16-4310-beb2-360b9fe9f61f",
    # 17. Razryadlagichlar qachon sinovdan o‘tkaziladi?
    "63895ad6-2ff8-4de7-befe-3e37441f3b32": "c6514c0d-e31a-4eee-aee6-ebd74022061d",
    # 18. 1000 Vgacha bo‘lgan elektr uskunalarda kuchlanish bor yo‘qli-gini tekshirish uchun nazorat lampasidan foydalanish mumkinmi?
    "f2e4cbe2-90bb-4933-b2be-3894811a2dd8": "f28e102f-5f65-4925-8034-7ec1f50379ba",
    # 19. Farmoyish yoki ruxsat bergan yoki olgan tezkor xodim nima qi-lishi kerak?
    "ad5af8e2-9522-4044-8661-217cb05a3308": "fb665b74-d461-4095-a013-8c1a024092f6",
    # 20. Ish to‘liq tugagandan keyin elektr qurilmani tarmoqga ulash kimning ruxsati bilan amalga oshiriladi?
    "ac9162ef-9faf-4707-9aa5-d09385f78850": "191a1bf5-55f8-47bc-8386-fc29a5cf3ece",
    # 21. Smenani qabul qilish - topshirish vaqtida tezkor xodim quyi-dagilardan qaysi birini bajarishi kerak?
    "0f2278db-8eda-436c-bb02-09c88a57b2f4": "7dbcec92-4f7b-48b0-982a-a036b3339434",
    # 22. Hushsizlik nima?
    "236a86cd-de9a-4504-8ac1-e8e3ce61452c": "66ad909c-375b-4710-ae66-ee5d3f09a3bf",
    # 23. Elektr tarmorlari dispetcherlari qachon shaxsiy javobarlikga tortiladi?
    "773e5eb2-9d33-4e7f-9f1e-fdad96bb8d2f": "025ed5ad-b34f-484e-a109-64b1db55173f",
    # 24. Jabrlanganga birinchi yordamni ko‘rsatishda amalga oshirila-digan xarakatlar qanday ketma-ketlikda bajarilishi kerak?
    "a7a94589-3d0d-4fed-9bb1-9a09fc86fd4e": "d0b1208b-2dee-453f-a2ee-44def4593a73",
    # 25. Ishida tanaffus bo‘lgan tezkor va tezkor-ta’mirlash xodim-lari mustaqil ishlashiga ruxsat berilishidan oldin nima bilan tani-shishlari kerak?
    "495fd609-e903-4b48-9861-55f9f9551306": "909e88e3-d5dc-4cd8-b93e-86af984af1b7",
    # 26. Tezkor-chiqish brigadasi avtomobillarida nechta o‘t o‘chirgich bo‘lishi shart?
    "eeba7674-b97d-42a3-a51e-97277c0803fd": "0c102cf7-2df6-4434-941a-683e6dd275d1",
    # 27. Ish joyini tayyorlashga va ishga qo‘yishga ruxsat bergan yoki uni o‘rnini almashtirgan shaxsning ruxsati (farmoyish)ni olmasdan elektr qurilmani elektr tarmoqqa ulash xuquqi berilishi qaerda yoziladi?
    "725b2276-b13c-4a6a-bd13-4bcef8cb0718": "b7d6f5e1-5a84-4c62-934d-533a1e1eef49",
    # 28. Ish joyini tayyorlashga va ishga qo‘yishga ruxsat etuvchi shaxs nimaga javob beradi?
    "f996c584-cb90-4b88-a02a-a8aaac29cdf6": "ad125b41-6e38-4b9e-a9e4-ae334a2ea958",
    # 29. Yong‘inga qarshi suv bilan ta’minlash tizimining barcha quvur-lari qaysi rangga bo‘yaladi?
    "9d5da343-22b0-4504-9ff1-cf2a07cc1781": "a9a8296f-913d-49fc-91e6-e183cdac02f9",
    # 30. Boshkaruv organiga bevosita ta’sir ko‘rsatish xuquqiga ega bo‘lgan ta’mirlash xodimi tezkor xodimlarning qaysi toifasiga tegish-li bo‘ladi?
    "bd1375ab-c7e7-4b65-a12b-3de001abf2c7": "5f860970-6613-4581-a3ad-659cd176e76e",
    # 31. Qaysi holatda ish joyini tayorlash to‘xtatiladi?
    "eaef953e-0e62-4b46-989f-b39c2d4b5d99": "32133f0c-47fa-4db8-8829-3f8ac0be0e68",
    # 32. Tezkor xodimlardan birini ikkinchisiga almashtirishga kim ruxsat berishi mumkin?
    "06a0a4d8-7176-419f-b7fe-56d07341d50b": "cd4beda2-9c73-4adc-9ecd-1c5572d44c66",
    # 33. Tezkor xodimlarning birini ikkinchisiga almashtirilishi kimga ma’lum qilinishi kerak?
    "5f8d9758-eea2-4b16-912b-3478c4c830e7": "ad296ed7-f0ec-4c96-8f2f-c84780413858",
    # 34. Yuqori turuvchi tezkor xodimning vakolatiga kiruvchi masala-lar bo‘yicha ma’muriy - texnik raxbar xodim farmoyishini, tezkor xodim qanday bajarishi kerak?
    "f826a929-e5e3-474a-b438-47c9a84061f6": "20c5fba9-5d9c-4c51-9ad9-ec4dc2ee4e70",
    # 35. Brigada tarkibini kim o‘zgartirish xuquqiga ega?
    "6491973a-8d00-4b8a-a721-14ed00aeaff4": "2268b8c7-37c6-4556-a2f7-3a8929c1692f",
    # 36. Brigadani nechta naryad bilan ishga qo‘yishga ruxsat beriladi?
    "58e9d309-1a1b-478b-9eb6-0cf00c530100": "7c0129ea-e7eb-452d-b089-6d573704360e",
    # 37. Ish faoliyatida tanaffusi bo‘lgan tezkor va tezkor-ta’mirlash xodimlari qancha muddat dublyorlikdan o‘tishi kerak?
    "d8f4313e-6a9a-47a1-8d62-a6394e9df19f": "20a7b92d-8931-417a-98d4-767200d762e1",
    # 38. Travma nima?
    "74f3df99-6452-4f44-8511-bbf5b2c6a5a5": "0423a7cb-9986-4123-b6fa-d48799b608c6",
    # 39. Yopiq taqsimlash qurilmalarida payvandlash va boshqa yong‘in chiqishi xavfi bo‘lgan ishlarini bajarish mumkinmi?
    "acab5495-e0a0-4570-9b65-798f349e321d": "a70662a5-1f5a-4ac4-a530-5bbedfa299d2",
    # 40. O‘lchov shtangalari qachon yerga ulanmaydi?
    "57fe9926-cb61-410a-91ca-b13014217e8f": "82e5b3ea-cc1b-452f-86bf-68509ab4dc46",
}

print(f"Total verified answers in solver for Test 2: {len(VERIFIED_TEST2)}")

theory_id = "c14799ca-7bf7-4643-86a4-05baa902faf8"

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
        print(f"\n[MUVAFFAQINAT!] Test № 2 to'liq yakunlandi! ({answered}/{total})")
        break
        
    # Pick first question that is in VERIFIED_TEST2
    target_q = None
    target_opt = None
    for q in questions:
        if q.id in VERIFIED_TEST2:
            target_q = q
            target_opt = VERIFIED_TEST2[q.id]
            break
            
    if not target_q:
        print("\n[OGOHLANTIRISH] Hozirgi darchadagi savollar bazada yo'q! To'xtatildi.")
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
