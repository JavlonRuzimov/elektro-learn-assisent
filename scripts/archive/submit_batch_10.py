import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("6702c76f-d6b5-4d5c-82ed-f2455dbb18db", "bed7735d-a6c8-441a-b193-e0b982118898", "qabul qilishda karabinga 300 kg, davriy ishlatish sinovlarida esa 225 kg og'irlikdagi yuk bilan 5 minut"),
    ("cac55432-14d6-4c0a-97e7-a56f7367a330", "722b1953-8832-4c1e-abdb-077b66db7fa7", ". elektrostatik induktsiya printsipiga"),
    ("ff89e01c-207f-43b4-b329-3f3eaf7d44d6", "a701db4f-081f-4be8-9685-f78c15aa71e2", "90 V"),
    ("cf5fd394-7189-4881-bcc5-9da8eddeaf2f", "bda6cc06-23fb-441e-afae-9b49add53e8c", "yuqori kuchlanish bilan")
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
