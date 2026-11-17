import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("82f20b9e-a63c-4879-b161-0143f6108dcd", "d941e90b-f895-4d1e-aa02-919e7b23f7bf", ". operativ ishlarni, o'lchov ishlarini, razryadnik detallarini o'rnatish va boshqa ishlarni bajarish uchun"),
    ("8ab70a2c-b878-44e7-9526-e1da0a96195e", "53b9e086-49d1-46ab-9881-6960bf5d79ab", ". 6-35 kV HL, OTQ va YoTQlarda kuchlanish bor-yo'qligini tekshirish"),
    ("b2a3fa1e-fa74-42fd-b2dd-42486c48fefc", "9a70313f-31b2-4f5d-b3b5-dc8e83f749e1", "tarmoq kuchlanishining 3 hissasiga teng bo'lgan kuchlanish bilan, lekin bu 40 kV dan kam bo'lmasligi lozim"),
    ("48f9b9ed-bfd6-4e08-8e8d-65b9fb693159", "e15e92d2-5fd6-4d73-9566-aeb786b0ba6e", "o'lchov asboblari ko'rsatishi hamda ko'rik natijalari bo'yicha")
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
