import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("ceb9a7fa-6a52-4d6c-ba8e-84f6413afab3", "f6273c48-9146-41f0-9ffc-0c22d5f168cb", "teshilish, elektr yoy bilan chokni qoplab o'tishlar va yuzadagi razryadlar sodir bo'lganda, sizib kamayish toki qiymati meyordan oshganda, dielektrik yo'qotish natijasida mahalliy qizishlar sodir bo'lsa"),
    ("a09e6ef8-3048-4efa-a9b3-9e15f197e51b", "1c206eb5-74fe-41fa-be74-82c2f21da723", "inventar raqami"),
    ("5b19d4dc-d1cb-45f1-a640-eec8233ca621", "fde7160a-c05b-4523-95e3-bb5385ad5283", "o'lchami, but va rasoligi, jihozlanganligi, izolyatsion yuzasining holati-ni tekshirish uchun tashqi ko'rikdan o'tkazilishi kerak")
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
