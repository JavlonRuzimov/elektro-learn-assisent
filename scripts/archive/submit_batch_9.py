import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("086c20fb-0d1d-400d-bf5d-b5df502317b1", "0e5dc9a0-b642-42a8-99e7-620b76ec9061", ". izolyatsiyalovchi qisqichlar saqlagichlar bilan ishlash uchun, izolyatsiyalovchi qoplamalar va to'siqlarni o'rnatish hamda olish va shunga o'xshash ishlarni bajarishda"),
    ("da5753cd-b6d9-4d4c-9ddc-1076352d49ee", "edcbbcbc-ad84-4522-bbd3-57b0e6cf13d8", "qo'shimcha rezistorli gazorazryadli indikator lampadan, kontakt-uchlikdan va operatorning qo'li tegib turuvchi korpusning yon tomoniga joylashgan kontaktdan"),
    ("0ca1ed61-dd41-4d2d-a922-937160be31ce", "0577ff5b-66e4-4acb-abf4-c0f9d02356b7", ". korxona bosh muhandisi yoki tuman elektr tarmoqlari boshlig'i tomoni-dan"),
    ("da2c0b4a-1527-406c-9f31-bf82b525ffae", "70fdf887-14b4-4ebc-b1a9-817d2c9e9618", "elektr sxemasi elementlari joylashgan bir korpusdan")
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
