import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("94ed8ec3-3275-4d27-a1ce-8ec7659828fe", "00bc21f6-18ba-43d7-ad93-ef3fefcc390a", ". ixtiyoriy shakldagi jurnalda"),
    ("faf9f830-fcad-4151-891f-8b406122a441", "b0252242-27f6-4f40-aaa6-bd277760de2a", ". qizil bo'yoq bilan o'chirib tashlanadi"),
    ("82ceb6bf-4a29-4823-b3cf-4f0fc30d7f1b", "15335cdf-64dc-4916-a2f7-1dcdaebe966a", "balandlikda ishlovchi ishchilarning xavfsizligini taminlash uchun"),
    ("90a4acd4-1cf5-411a-b475-03a3518a63c1", "54e53436-2aa2-42fb-bb2c-e423262b2996", "odamlarni o'chirilgan tok o'tkazuvchi qismlarda ishlayotganda xatolik bilan berilgan...")
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
