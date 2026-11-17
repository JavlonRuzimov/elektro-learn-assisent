import sys
import json
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# Check initial hearts
me = client.base_client.get('/progress/me')
initial_hearts = me.get('hearts', {}).get('heartsCount')
print(f"Starting hearts: {initial_hearts}/5")

batch_answers = [
    ("f429b70c-8cc3-4338-8c7d-0364dd92180c", "6fed1c67-f0ad-4617-a68a-d1bde38589e0", "qabul qilish-topshirish sinovlarida 6 kV kuchlanish va ishlatish mobay-nida esa 2 kV bilan"),
    ("aa8e2b23-12bb-49b8-97de-159b763d45ff", "288754ae-8a95-48bd-b25e-972a52962dd2", "man etiladi"),
    ("64ceb47a-3e56-4be4-92af-c2cf97cf4f04", "6e90aff0-fc96-47a6-995b-02854cc57c52", "izolyatsiya qismiga"),
    ("ece95fc5-5a99-499f-8b0a-f4cb7124c3c4", "7a4f4be4-cd57-4b31-9b95-0dea603f3696", "o'zgarmas tok bilan")
]

for qid, opt_id, desc in batch_answers:
    print(f"\nSubmitting for QID {qid}...")
    print(f"Selected option: {opt_id} ({desc})")
    
    time.sleep(1.5)
    res = client.progress.submit_answer(qid, opt_id, source="LESSON")
    
    # Check result
    is_correct = res.is_correct if hasattr(res, 'is_correct') else (res.get('isCorrect') if isinstance(res, dict) else getattr(res, 'isCorrect', False))
    print(f"Result: is_correct={is_correct}")
    
    # Check hearts after
    me_after = client.base_client.get('/progress/me')
    curr_hearts = me_after.get('hearts', {}).get('heartsCount')
    print(f"Hearts after submit: {curr_hearts}/5")
    
    if not is_correct:
        print("CRITICAL: Answer was marked INCORRECT! Halting immediately!")
        sys.exit(1)
        
    # Save to knowledge base
    kb.record_answer(qid, desc, opt_id, desc)
    print(f"Successfully saved {qid} -> {opt_id} to knowledge base.")

print("\nAll 4 questions submitted successfully!")
