import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import time
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

def main():
    client = ElektroLearnClient()
    kb = KnowledgeBase()
    
    # 1. Check profile and hearts
    me = client.base_client.get('/progress/me')
    hearts = me.get('hearts', {})
    cur_hearts = hearts.get('heartsCount', 0)
    print(f"Current hearts: {cur_hearts}/5")
    
    # Verified 4 answers to submit
    batch = [
        ("8c2711ea-5f25-4010-9106-75dfa092baad", "f21efa88-f26a-435b-bc6f-7c5197ad46bd", "muzlab qolganda yordam ko'rsatishning eng muhimi - tananing muzlab qolgan joylarining birdaniga tez isishiga yo'l qo'ymaslikdir"),
        ("e8b82af9-9d5d-415a-beeb-501c63c8cba0", "77be8d80-2afe-4803-9e1a-9568802858a9", "yilning issiq kunlari 2 soatdan, sovuq kunlari 1 soatdan ko'proq qo'yib bo'lmaydi"),
        ("39b9419d-9356-4c0c-ba88-1c4bac85f602", "8145eb61-25cb-4af9-8837-f0d75e481c7f", "gazlardan zaharlanganda odamda bosh og'rig'i, chakkada dukkilash, quloqda shang'illash, umumiy holsizlik paydo bo'ladi, bosh aylanishi, yurakning tez urib ketishi, ko'ngil aynishi va qayt qilishi mumkin"),
        ("b1439723-06f8-4dbd-91d0-777ab61c1fb3", "6bb84955-6519-43cd-9943-54472960228d", "umurtqa suyagi shikastlangan jabrlanuvchini joydan - joyga ko'chirish uchun zambilning tagiga keng taxta, uning ustiga esa kiyimlarni solib qo'yib, jabrlanuvchini chalqancha yotqizgan holda amalga oshirish lozim. Taxta bo'lma-gan taqdirda jabrlanuvchini zambilga qornini pastga qilib yotqizish kerak")
    ]
    
    for qid, opt_id, opt_text in batch:
        print(f"\nSubmitting {qid} -> {opt_id}...")
        res = client.progress.submit_answer(qid, opt_id)
        is_correct = getattr(res, 'is_correct', False)
        print(f"Result: {is_correct}, XP: {getattr(res, 'xp_earned', 0)}, Hearts: {getattr(res, 'hearts', None)}")
        if not is_correct:
            print("ALERT: WRONG ANSWER! Stopping immediately.")
            sys.exit(1)
        kb.record_answer(qid, "", opt_id, opt_text)
        time.sleep(0.5)

    # Now get theory questions for module 6
    theory_id = "f1ede884-e103-481a-8642-c06f7480b0d6"
    t_q = client.progress.get_theory_questions(theory_id, mode="continue")
    questions = t_q.get('questions', [])
    print(f"\nRemaining count in module: {t_q.get('remaining_count')}, Total: {t_q.get('total_questions')}")
    print(f"Fetched questions batch count: {len(questions)}")
    for i, q in enumerate(questions):
        print(f"\n--- Question {i+1} ---")
        print(f"ID: {q.id}")
        print(f"Prompt: {q.prompt}")
        for opt in q.options:
            print(f"  [{opt.id}] {opt.option_text}")

if __name__ == '__main__':
    main()
