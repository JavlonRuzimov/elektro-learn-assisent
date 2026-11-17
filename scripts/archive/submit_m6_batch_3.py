import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("5e2ce5b1-6c5e-414f-bbfc-ba1214d168aa", "28202494-5006-4773-8655-c4d5b9bad27b", "issiq yoki oftob urganida, jabrlanuvchini zudlik bilan salqin joyga olib o'tiladi..."),
    ("c80f7453-b469-4a03-b65d-3e84f8dedfe8", "2546d467-64d2-4245-beab-56c35597a68e", "fakat shifokor"),
    ("f204adee-f6d8-47d6-a739-41e82e26e5de", "41f9f423-9b4b-4d65-a309-57c3bb559d5c", "hasharotlar chaqganida terining ichiga kirib qolgan nishini olib tashlash...")
]

for qid, opt_id, desc in submissions:
    print(f"\nSubmitting {qid}...")
    print(f"Selected: {opt_id} ({desc})")
    time.sleep(1.5)
    
    res = client.progress.submit_answer(qid, opt_id, source="LESSON")
    is_correct = res.is_correct if hasattr(res, 'is_correct') else (res.get('isCorrect') if isinstance(res, dict) else getattr(res, 'isCorrect', False))
    print(f"Result: is_correct={is_correct}")
    
    me_after = client.base_client.get('/progress/me')
    curr_hearts = me_after.get('hearts', {}).get('heartsCount')
    print(f"Hearts: {curr_hearts}/5")
    
    if not is_correct:
        print("HALTING IMMEDIATELY! INCORRECT ANSWER!")
        sys.exit(1)
        
    kb.record_answer(qid, desc, opt_id, desc)
    print("Recorded to KB.")

print("\nAll 3 submitted successfully!")
