import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("721a0553-28fd-4b68-82f3-88b771788a84", "cfa45cdc-459d-4f4d-8b33-1019f086f424", "jabrlanuvchini eng yaqin tibbiy muassasaga etkazish choralarini ko'rish"),
    ("f34ae67a-7780-4e02-8035-e5f5bd98cdc2", "8ca9b83c-4c63-4695-87d6-5026efd62c5e", "cho'kishning turlari ikki xil bo'ladi: ko'kimtir turi (ko'k asfiksiya)..."),
    ("9169bb50-6360-4ce0-9330-650c463ff0bf", "76a228c1-53e9-4e44-8cab-ffbe105be5b2", "ko'zga narsa tushgan bo'lsa, uni ko'zni (stakandan, paxta yoki dokadan..."),
    ("b3597cf0-20c6-442f-9c05-583fedbb8ae4", "7d94773a-8da3-46c5-a81f-10b909f876df", "hushsiz odam tanasi qattiq terlaydi, qo'l-oyoqlari muzlaydi...")
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
