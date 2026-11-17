import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("dc642e55-7090-470d-a674-b2e6792fa999", "80e621e4-0065-49e1-b976-f21c8ecfdf47", ". elektr uzatish tarmoqlarida ularning yaxlitliligini buzmasdan tar-moqdagi tok, kuchlanish va quvvatni o'lchash uchun"),
    ("7afbbb11-ece5-4c97-bd16-f957850e45ec", "5b831c1d-a9a1-44e2-b364-4a8048394606", "xatolik bilan ish joyiga kuchlanish berish mumkin bo'lgan kommutatsion apparatlar harakatini taqiqlash...")
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

print("\nAll 2 submitted successfully!")
