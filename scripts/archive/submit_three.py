import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("014fbda1-4291-4f75-8938-f1cb2b2e620e", "fc4efdab-7201-4b7a-a80c-64f1de369683", "darhol sinovdan keyin ushlab ko'rib"),
    ("93780fcf-3871-44f0-bb14-8f785f6ef98d", "5699dd91-8f85-4a19-9378-7bc103c3bae2", ". qancha kV kuchlanishgacha yaroqliligi va keyingi sinov muddati"),
    ("ece95fc5-5a99-499f-8b0a-f4cb7124c3c4", "7a4f4be4-cd57-4b31-9b95-0dea603f3696", "o'zgarmas tok bilan")
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
