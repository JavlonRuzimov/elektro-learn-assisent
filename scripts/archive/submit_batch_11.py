import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("b125afe3-0053-421c-aff1-ddce714c1873", "e3db13d1-1997-4c3f-962a-1a6eeabb79b8", "tuzilish printsipi erga ulashni taqozo etuvchi hollardan tashqari, boshqa barcha holatlarda erga ulanmaydi"),
    ("2aabcf12-3145-4323-8f92-ca0715dc7ebb", "dc21a1f1-5507-4395-90a8-5b54a744f4a2", "4"),
    ("f57450bd-1a4f-4e11-bd88-e8984ee5f564", "a1921a7f-a6d3-4713-ad9e-1c92fa0d316c", "elektr sxemasi elementlari joylashgan ikki korpusdan"),
    ("e816aadc-2902-4d24-8b10-d51fafd89ce2", "46597e67-f6fd-4a6c-9ae8-1d821a2ea41d", ". izolyatsiyalovchi shtangalar, izolyatsiyalovchi va elektr o'lchovchi qisqichlar, kuchlanish ko'rsatgichlari, dielektrik qo'lqoplar, izolyatsiyalovchi dastakli chilangarlik-yig'uv asboblari")
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
