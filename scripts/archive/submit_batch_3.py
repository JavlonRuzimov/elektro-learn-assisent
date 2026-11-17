import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("cdc47f6a-fd99-4033-bad4-6e98ccf63957", "a128c1c9-5f11-45ee-af0d-570d9d7da99e", "talab qilinmaydi"),
    ("63f9b9ee-396b-4cb6-8223-dff2099a5af4", "9bc73a28-9824-4d8c-981e-2064d8803add", "1 - 5 minut"),
    ("1e4da1db-c274-4a51-b30a-16f9a4b6db2d", "bee60761-2290-4fa8-8795-4441b4b9625c", "ES va PSdagi ishlab turgan elektr uskunalarida OTQ va YoTQda..."),
    ("70223e20-9ef6-4fa5-8e54-22eea5bc2426", "2a8c395c-5524-4d00-8f9b-22c513fac9f3", "qo'shimcha himoya vositasi, ish joyi montyorning...")
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
