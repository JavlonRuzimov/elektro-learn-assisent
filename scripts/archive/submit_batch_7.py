import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("46786b81-6618-4985-929e-1242bb4c35da", "a983b112-aee0-48c9-9068-4de14e99cbaa", "15° S - 20° S haroratda 50 Gts chastotali o'zgaruvchan tok bilan"),
    ("42763116-146c-4430-821c-4da7c0acd544", "626d4c38-a52c-4010-aebd-2d685742c75b", "raqami va erga ulovchi simlarning ko'ndalang kesimi"),
    ("d65d959b-6a16-4fad-ad2d-e4aedbb1ebef", "520adcb9-9973-43f8-b0d5-2243f3d13a19", "yopiq joylarda hamda yog'ingarchilik bo'lmaganda ochiqda joylashgan elektr uskunalarida qo'shimcha himoya vositasi sifatida"),
    ("fbb6cc8f-22ce-45e7-9098-378a1b37ec1a", "0f17b222-a8c8-4224-a1bd-74bf5244347d", ". GOST 9071-79 da")
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

print("\nAll 4 submitted successfully!")
