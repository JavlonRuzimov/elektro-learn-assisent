import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("9ec0807c-e26d-4ee3-8165-a66103385ce5", "996e685a-df13-486c-a2ff-ed25993f1bba", "muzlab qolish, bu past haroratning tasiri ostida to'qimalarning shikast-lanishidir"),
    ("63058688-34b1-4155-b0ab-832974cbb84e", "e821b13d-8c08-410f-9d4f-7f8e2b978301", "boshini yon tomonga burib yotqizib qo'yish kerak"),
    ("4321fe83-e68e-49f5-8f99-6f18d64699b1", "3dd11328-98d5-401a-a0ad-9bde36aa33be", "azot oksidlari bilan zaharlanishda jabrlanuvchiga ichimlik sodasi qo'shilgan issiq sut ichirish kerak"),
    ("367c6999-f452-410d-8cf7-4726b849ca4d", "8a676403-5273-4aa3-940f-3e4b70893182", "jabrlanuvchini zambilda, joydan – joyga ko'chirishda buyruq bo'yicha...")
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
