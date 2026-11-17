import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("9accf70b-40ca-4623-880d-7b75c675d441", "22595c0c-31c2-480e-b1a6-651ed02dcd74", ". universal kallakli izolyatsiyalovchi shtangalarni"),
    ("5538514b-282a-4930-9159-e209a0a954a2", "3edaa0ee-360a-4e5b-aad2-93e2bb327805", "1000 V gacha bo'lgan kuchlanish ko'rsatgichining konstruktsiyasi kontakt-uchlikning o'qi bo'ylab harakatlanishiga yo'l qo'ymasligi zarur"),
    ("64ceb47a-3e56-4be4-92af-c2cf97cf4f04", "6e90aff0-fc96-47a6-995b-02854cc57c52", "izolyatsiya qismiga")
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
