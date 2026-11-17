import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("191551ea-08ed-418a-b5a1-3d9e6e6a8e52", "e6c18e70-a900-4af8-aefb-3aa984bdc2c6", "jabrlanganning organizmiga xavfli va zararli omillar tasirini... bartaraf qilish..."),
    ("53882729-445a-4db1-bee7-88c51e212c0f", "a21c9f17-d8a0-4fbf-8957-db0849118e41", "zaharlanishlarda jabrlanuvchini darhol gazlangan zonadan olib chiqish..."),
    ("dbffc305-afa2-494e-83c9-38a886221bfd", "169b0541-9440-4500-82ca-914d65067f58", "boshi, bosh suyagi va miyasi... chalqancha yotqizib ko'chiriladi"),
    ("8347dc52-3816-473e-bbcc-3ce98d78a5fe", "88235e20-2faf-4cfb-bedc-c04e6864c57f", "kuyishlar uch xil bo'ladi, termik, kimyoviy va elektr kuyish")
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
