import time
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Barcha 100% tasdiqlangan javoblar (VM 711-sonli qarori va server kalitlari asosida)
VERIFIED_ANSWERS = {
    # 1. Yong'inni o'chirish tezkor varaqalari
    "a99c6535-d259-4cac-a65d-3f37303c37d1": "4b7603ed-b05c-4bc9-a41b-120c806de4d2",
    # 2. Tashkilot rahbari YOTK tavsiyalarini eshitishi (kamida 6 oyda 1 marta)
    "03aae28d-ecaf-4642-9f36-5a00c4aa55ca": "f2c5622e-bdf3-4db7-9301-b7830f5ddc2b",
    # 3. Yong'in o'chog'ini birinchi bo'lib payqagan xodim
    "a5f17128-6927-43f9-80d2-d0b1d880c7e9": "959723e7-359e-403b-a035-7ef6dcccc249",
    # 4. Ko'ngilli yong'inni o'chirish drujinasi maqsadi
    "27cdd0b4-de87-4928-bc7d-9289d066c06a": "c863fd56-98e3-455d-bcfd-58099baef955",
    # 5. O't o'chirgichlar 15 kg dan kam (yuqori qismi 1.5 m)
    "23aa6d72-c59a-4f2e-b610-bd2a6ecc6e0c": "13859d0a-a8a7-4c7e-bbe3-0dcd22884ec0",
    # 6. Tezkor-chiqish brigadasi avtomobillarida o't o'chirgich
    "e1f74cc1-1501-4d5b-b5ca-89d961963bb5": "7066b18d-8169-4de4-96a6-9d76f7c7ad19",
    # 7. Yo'riqnomalar tasdiqlanishi (server kaliti: tashkilot bosh muhandisi tomonidan)
    "bc465158-a89d-4ea8-a498-d3f35e55e257": "d195240d-59ac-4fad-9e7e-4a3180593804",
}

# Knowledge Base ga ham yozib qo'yamiz
for q_id, opt_id in VERIFIED_ANSWERS.items():
    kb.record_answer(q_id, "", opt_id, "")

level3_id = "a6a784c7-b454-4d3c-af92-3d2dab7f0f30"
detail = client.progress.get_level_detail(level3_id)
t = detail.theories[0]

print(f"=== LEVEL 3: {t.title} ({t.answered_questions}/{t.total_questions}) ===")

# Energiya tekshiruvi
hearts_info = client.base_client.get('/progress/me')['hearts']
print(f"Joriy energiya: {hearts_info['heartsCount']}/{hearts_info['maxHearts']}")
if hearts_info['heartsCount'] < 1:
    print(f"[OGOHLANTIRISH] Energiya 0 ga teng. Qayta tiklanish vaqti: {hearts_info.get('nextRegenAt')}")

while True:
    q_data = client.progress.get_theory_questions(t.id, mode="continue")
    questions = q_data.get("questions", [])
    if not questions or q_data.get("is_module_complete"):
        print(f"\n>> {t.title} muvaffaqiyatli yakunlandi!")
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
        print(f"  -> Tanlangan javob: '{opt_text[:60]}...'")

        time.sleep(2)
        try:
            res = client.progress.submit_answer(q.id, opt_id, source="LESSON")
        except Exception as e:
            print(f"  [XATOLIK]: {e}")
            exit(1)

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
print("LEVEL PROGRESSI:")
prog = client.progress.get_progress()
for lvl in prog.levels:
    lock = "Qulf 🔒" if lvl.is_locked else "Ochiq 🔓"
    comp = "100% (Tugallandi)" if lvl.is_completed else f"{lvl.completion_percent}%"
    print(f"  - [{lock}] {lvl.title}: {comp} ({lvl.correct_answers_count}/{lvl.attempts_count})")
print(f"Energiya: {prog.hearts}")
