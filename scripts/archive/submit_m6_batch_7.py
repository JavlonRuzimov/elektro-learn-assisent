import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("2aaf341e-ebef-4313-9cab-1b67f35716d0", "0df38541-c4c6-43b3-8463-9bd03aa3009f", "jarohatlar chuqurligi bo'yicha barcha kuyishlar to'rtta darajaga bo'linadi"),
    ("c0085f6f-97aa-45b7-aaeb-95d6728eceea", "c89ec24c-b6bd-4381-9545-cd6970328dfd", "begona jismlar tomoqqa, qizilo'ngachga, nafas yo'llariga, ko'zga, teri ostiga va hokozalarga tushishi mumkin"),
    ("94fbeae0-f084-472d-8b9a-8275cef71830", "d947c29c-55e8-4a6a-b2a9-558f72f71489", "rangi oqaradi, terida yopishqoq ter paydo bo'ladi, tez tez nafas oladi, puls tezlashadi va ovozi sekinlashadi"),
    ("3e1ee556-c7f3-4ea0-b407-4b267722a7aa", "bf8fb5b2-f58d-43ee-a38c-2a2616e914aa", "jabrlanuvchini o'tqazish, qon dimog'iga oqib tushmasligi uchun boshini oldinga engashtirish, yoqasini echib qo'yish...")
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
