import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("f0540503-ea4b-4700-969a-9d03cb5d17a3", "1da9a025-52fe-4b9e-9afe-a7adb54f37ec", ". izolyatsiyalovchi shtangalar, izolyatsiyalovchi va elektr o'lchovchi qisqichlar, kuchlanish ko'rsatgichlari, fazalarni sozlash uchun aniqlovchi kuchlanish ko'rsatgichlari, elektr montyorlar havo elektr uzatish tarmoqlarida bevosita tok o'tkazuvchi qismlarga tegib turib tamirlash ishlarini olib borishda ko'llaniladigan izolyatsiyalovchi qurilma va asbob-uskunalar"),
    ("b57d2e7c-cb91-4680-8bbc-78d10ad57379", "e72348d1-33ea-4fe4-a149-d3c49f2d3374", "elektr sxemasi gazorazryadli indikator lampadan, lampaga parallel ulan-gan rezistor, qo'shimcha rezistorlar va kontakt-uchliklardan")
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

print("\nAll 2 submitted successfully!")
