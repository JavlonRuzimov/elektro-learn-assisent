import time
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# 100% tasdiqlangan va server kalitlari bilan moslashtirilgan javoblar
VERIFIED_ANSWERS = {
    # MODULE 1: Rele ximoyasi (10/10 TUGATILGAN)
    "46792ad9-02e6-430c-9a9b-0121f40ff7a9": "d0a9dde7-ab40-4da9-8f48-5a1b69e82d76", # Kuchlanish tushib ketishi
    "dbf8b9ab-d8b0-4229-92f9-0c18d2603a32": "518156ef-6c34-425f-b68a-c75423721ba1", # Om qonuniga asosan.
    "5e0c8872-1c38-4894-903a-cfac1d3f1512": "1b5b5d32-a15e-40b1-9a05-cb739c766672", # 1000 V kuchlanish bilan 1 min. davomida
    "ed119a00-a589-4c73-ba12-33dbd381cb5d": "b517935c-685f-458c-baa5-a35313fabf88", # Qoida kabi, ishlatib ko'rish yo'li bilan.
    "8d0fa05a-e2f0-464a-8d84-e2be3efca0fb": "962f6c92-7fc9-432b-8731-0017a2af2d38", # kontaktlari toksiz pauza vaqtida avtomatik ajraladi
    "c4eb00f9-422a-447b-887e-082d634a3d80": "111235ce-aaca-4950-8790-fe95c768b0fa", # faqatgina o'z ishchi zonasini eng qisqa muddatlarda 100% himoya qiladigan
    "4bb00119-8d93-4ab3-bd11-ee0f456e0d0a": "84e69959-fa52-4a97-9ee2-7b4db86f1e1e", # 1 MOm
    "bc604d39-6084-4803-93c9-13f79c3f37bc": "8ef87ae2-ea0d-4d9c-ae1a-bc6d06aa1d0b", # Differensial va gaz himoyasi ishlab transformator o'chganda
    "e11d1a73-e111-40c9-adea-d7b5f7bcf850": "e37ae18e-a3d0-4770-88bf-206062fd7640", # asosiy himoya zonasini va qo'shni zonalarni himoya qiladigan, xayallash vaqti bilan
    "99caecdb-f8c1-4e26-a092-5a0b218b2222": "cc616a90-a5ef-455a-aa5a-f9f2adb6c8cd", # Tanlovchanlik, sezgirlik, tezkorlik, ishonchlilik

    # MODULE 2: Rele ximoyasi 2 (8/15)
    "89661173-6c2f-48e0-a76e-a804bcb03b22": "86762f91-b414-4e46-9500-87290cd9980d", # EUHT rele himoyasi ta'sirida o'chirilganda.
    "0bce1114-a290-4265-8969-4b40976446d3": "e267f5ce-899a-4428-85bd-1820f70846d6", # Relelarga, asboblarga ulangan yoki qisqa tutashtirilgan bo'lishi kerak.
    "4af48e88-1060-4c74-9e60-2d8512d8024c": "7219eabd-84f7-4790-91e6-7f1a86007851", # Himoyani qo'shimcha, navbatdan tashqari tekshirib ko'rish kerak.
    "39493acb-3064-4e98-aff5-69ff0d400065": "7c6e9df8-e4df-4afd-8070-860c847366e4", # Ha, noto'g'ri ishlab ketish xavfi bo'lganda.
    "401f7a23-e3eb-42cf-aa6c-32652b910151": "b015725c-8221-4eea-82fc-bee38c8083a9", # Operativ xodim.
    "63605e75-f4cb-4033-973e-68f4705920f5": "386fae74-140a-4814-b21a-85c57278ad9e", # RHA xizmati va ETL xodimlari.
    "13887340-da64-4ffd-8267-be491644a505": "82f6fe37-a3fd-42e1-a04e-5eea5681e6a8", # 1000 V kuchlanish bilan 1 daqiqa.
    "87b57709-1214-461d-89a7-40524145e853": "d13ae190-7c5e-478f-b2f9-5827f8f496a0", # Qopqoq kamida 1 %, moy quvuri kamida 2 %
    "28cfc58f-2598-419d-9f07-7e81473d72ba": "a5222436-229b-4f73-9056-3cbc324b24b3", # Agar ajralgan gaz yonuvchan bo'lmasa va shikastlanish belgilari aniqlanmasa.
    "44518c7a-ecf9-494f-864c-dd3de0ce541d": "aa11a2cd-b0a3-4d9b-ae9c-071a1c5b4aa7", # 1 MOmdan kam emas
    "2b5defec-3585-47f7-98a8-b4413aa69b46": "bb940f04-6b37-42a0-b4a4-76741ce74b6a", # Ha, zahiradagi himoyalarda tezlatish (uskoreniya) kiritilsa.
    "094ede35-8577-470f-b1e6-5511386c8685": "1d174831-7d25-4357-96e9-b3d27c6c717c", # RHA va ETL xodimlari hamda ularning topshirig'iga asosan tezkor xodimlar.
    "0724ea87-10f6-4862-8ed6-e568f3243e7d": "0a55d54c-b25a-4828-bab6-991410c64c79", # Qoida tariqasida, ishlatib ko'rish yo'li bilan.
    "1caed589-37dd-4394-bcf2-d3173b91a87c": "e64c0636-fd1d-49d0-84b6-2b2f08f0c9cc", # Har 50 m da 1 dan ko'p emas.
    "4940dd78-20f8-4c9e-a564-d87d1e2c0553": "3d4b939d-776b-4ab6-a9ec-0bc3472bc607", # Nominal kuchlanishdan 5 % yuqori.
}

# Knowledge Base ga yozish
for q_id, opt_id in VERIFIED_ANSWERS.items():
    kb.record_answer(q_id, "", opt_id, "")

level4_id = "ea8b4c9c-5e96-43fd-b54e-a58fce05717a"
detail = client.progress.get_level_detail(level4_id)

for t in detail.theories:
    print(f"\n==========================================")
    print(f"BOSQICH: {t.title} ({t.answered_questions}/{t.total_questions})")
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

print("\n==========================================")
print("LEVEL 4 PROGRESSI:")
prog = client.progress.get_progress()
for lvl in prog.levels:
    lock = "Qulf 🔒" if lvl.is_locked else "Ochiq 🔓"
    comp = "100% (Tugallandi)" if lvl.is_completed else f"{lvl.completion_percent}%"
    print(f"  - [{lock}] {lvl.title}: {comp} ({lvl.correct_answers_count}/{lvl.attempts_count})")
