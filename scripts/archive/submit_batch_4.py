import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("76fd4139-a308-4fa1-9515-69ae9b2f3d86", "a81081cd-f079-497f-b949-4a6ac2917bdc", ". har 6 oyda bir marta himoya vositalari holatiga javobgar mamuriy tex-nik xodim tomonidan"),
    ("f814154f-4897-411f-865d-435dca5c06c1", "e55bb9f4-c66b-4053-a82e-868b1453d7a9", "kuchlanishi 1000 V dan yuqori bo'lgan elektr uskunalari uchun 25 mm2 dan, kuchlanishi 1000 V gacha bo'lgan elektr uskunalari uchun esa 16 mm2 dan kam bo'lmasligi zarur"),
    ("aa8e2b23-12bb-49b8-97de-159b763d45ff", "288754ae-8a95-48bd-b25e-972a52962dd2", "man etiladi")
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
