import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

submissions = [
    ("2260a881-dc9f-4379-b8dd-fdbbc7bc74e3", "77955ada-543c-43a6-bd7a-0b46a39b8a06", "fakat ishkor va kislota bilan ishlanadigan ish joylarda"),
    ("fe3755c2-9fb3-493a-923c-bd8940bedeed", "da16f70f-ed64-4dbd-8acb-1a6b2875b8fe", "jabrlanuvchini joydan-joyga ko'chirishda uni qulay holatda bo'lishini kuzatib turish va silkitmasdan olib yurish kerak"),
    ("c024f1a0-f4cb-4802-aeb1-d2a56acb42ea", "22628c0c-bc63-4b3a-abee-4508c237ef7e", "hayotiy muxim funkiyalarining buzilishining asosiy alomatlarini, jabr-lanuvchini zararli va xavfli omillardan xalos etishni..."),
    ("97a62409-c6da-4557-bc46-360fe69f2f36", "fb600d57-ad65-427a-8d4a-cab8e77b20d1", "oftob urishi odam boshiga hech narsa kiymay uzoq vaqt davomida bevosita quyosh nurlari ostida bo'lganida sodir bo'ladi")
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
