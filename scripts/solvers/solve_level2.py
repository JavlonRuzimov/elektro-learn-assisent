import time
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

ANSWERS_LEVEL2 = {
    # 1-Mavzu: электр энергетикаси тизими
    "2acfefcf-32ef-474e-9cda-56a6aca129b0": "7acb3413-8246-4ee8-8d33-de721f018419",
    "9a14bbd8-363f-4006-923d-006d606bec46": "9e391c1e-fb9f-4248-9078-6a6fd5e99285",
    "08848557-1d05-4ab3-af19-7b37e48d8b5e": "ac9c8333-ff9d-45e3-a81b-485bd3bb55cd",
    "8d76fb23-13bf-46d2-b404-23ddbadaa562": "02c2d78d-e46d-4bec-97bf-8350f18c8650",

    # 2-Mavzu: техник эксплуатация қилиш қоидалари
    "96c71337-5377-4fb1-aa75-42bd35848e4d": "11b55a6c-edf7-40a9-b3c4-5db75c8912af",
    "196c3d03-2118-4f4f-ae56-415d9603d61f": "c26dffff-74b8-4196-815a-24f1e53990a1",
    "da48da22-0517-45f2-b20e-8cad2de405fe": "2caa4ae1-3a09-41ee-9eb7-4772afc1a6c3",
    "805c30dc-cbb9-4be9-89e7-4dc64d6d6172": "4db4c396-bf45-4f65-acf2-bcea8231d38a",

    # 3-Mavzu: электр ускуналар
    "10007b11-8cb9-42de-904a-e94004df0b91": "56fdeb04-2e3e-4c60-b244-455b43a70387",
    "98b86b2a-4288-4db5-847e-c803fe25d592": "6f3e1d8d-2768-43f6-bfc9-32b0ddb5f6ce",
    "653cdd8f-d576-4754-9b92-f47af4fedb25": "67bbdf93-30e3-4e84-bc1b-b65592fc7e92",
    "5e8d0f92-5347-4c45-8074-e979e5b05887": "bbb91816-b183-4587-b7c7-9b6cc5d84570",
}

level2_id = "cfb2490a-4950-4886-adf3-7c79fbb4e4ad"
detail = client.progress.get_level_detail(level2_id)

print(f"=== LEVEL 2: {detail.title} NI 100% YAKUNLASH BOSHLANDI ===")

for t in detail.theories:
    if t.is_complete:
        print(f">> {t.title}: 100% tugallangan.")
        continue

    print(f"\n==========================================")
    print(f"Bajarilmoqda: {t.title}")
    q_data = client.progress.get_theory_questions(t.id, mode="continue")
    questions = q_data.get("questions", [])

    for q in questions:
        opt_id = ANSWERS_LEVEL2.get(q.id)
        if not opt_id:
            print(f"[XATO] Savol lug'atda yo'q: {q.prompt}")
            exit(1)

        opt_text = next((o.option_text for o in q.options if o.id == opt_id), opt_id)
        print(f"\n[Savol]: {q.prompt}")
        print(f"  -> Tanlangan: '{opt_text[:55]}'")

        time.sleep(2)
        res = client.progress.submit_answer(q.id, opt_id, source="LESSON")

        if res.is_correct:
            hearts = res.hearts.get('heartsCount') if isinstance(res.hearts, dict) else res.hearts
            print(f"  [+] TO'G'RI! (+{res.xp_earned} XP, Energiya: {hearts})")
            kb.record_answer(q.id, q.prompt, opt_id, opt_text)
        else:
            print(f"  [-] XATO! Server to'g'ri ID: {res.correct_option_id}")
            exit(1)
        time.sleep(1.5)

print("\n==========================================")
print("LEVEL 2 TO'LIQ YAKUNLANDI! NATIJALAR:")
prog = client.progress.get_progress()
for lvl in prog.levels:
    lock = "Qulf 🔒" if lvl.is_locked else "Ochiq 🔓"
    comp = "100% (Tugallandi)" if lvl.is_completed else f"{lvl.completion_percent}%"
    print(f"  - [{lock}] {lvl.title}: {comp} ({lvl.correct_answers_count}/{lvl.attempts_count})")

