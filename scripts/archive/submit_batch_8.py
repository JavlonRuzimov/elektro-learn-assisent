import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("35865ffd-7dea-492d-833e-67896ddeeb07", "892d9bbc-dea6-408f-a173-81664701a215", "Ishchi qism, zaryadlovchi uskuna va 110 kV kuchlanishli izolyatsiyalovchi teleskopik shtangadan"),
    ("dee2c98b-49aa-488c-8350-544c6eabdd73", "1b1d2cf1-a701-4e26-88eb-be2ce66145e2", "kuchlanish ostida bo'lgan tok o'tkazuvchi qismiga yaqinlashtirilgan sari chastotasi ko'payib boruvchi uzuq-uzuq yorug'lik signali beradi"),
    ("d34a416c-3481-44de-a9f6-39f83ad0fd5e", "83e7d33b-5096-4718-b919-38107c540acf", "ikki qutbli va sig'im toki tasirida ishlaydigan bir qutbli kuchlanish ko'rsatkichidan")
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
