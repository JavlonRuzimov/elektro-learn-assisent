import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("110b4aba-2f1a-4ee9-a4b9-62790d9ee10b", "a1cec085-7d93-4393-8055-c193c2e5888c", "kamida 8 m. Masofaga"),
    ("62ea26ad-ffa0-4cc4-a2b1-0d8f0a099e3b", "dfec8da3-0866-48cc-96e3-bea34bfd019e", "zaharli ilon va hasharotlar chaqganda bosh aylanishi, ko'ngil aynishi, qayt etish..."),
    ("432249f2-b2ac-40a8-935b-b59938fcac0a", "d595e5a6-205e-450c-9708-2d5cde51bcf6", "charchagan odamning ko'lini oldinga cho'zib, bilagi tagiga elkasini tutishi va «bras» usuli bilan suzib..."),
    ("0ec4aee6-6e6d-40b6-ae24-f6456e276cc8", "154da0c1-ffcd-47d8-8700-186418b8dd24", "kokshal kasalligiga karshi emlash uchun shifokorga murojaat kilish kerak")
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
