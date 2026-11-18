import sys
import os
import json
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase

client = ElektroLearnClient()
kb = KnowledgeBase()

# 1. User & Progress
me = client.base_client.get("/progress/me")
user = client.auth.get_me()

# 2. Daily Plan
try:
    daily = client.daily_plan.get_daily_plan()
except Exception as e:
    daily = str(e)

# 3. Leaderboard
try:
    lb = client.leaderboard.get_leaderboard()
except Exception as e:
    lb = str(e)

# 4. Overall Levels Progress
prog = client.progress.get_progress()

# 5. KB metrics
kb_count = len(kb.data.get("questions", {}))

out = {
    "user": {
        "id": user.id if hasattr(user, "id") else getattr(user, "user_id", "N/A"),
        "full_name": getattr(user, "full_name", f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}"),
        "username": getattr(user, "username", "N/A"),
        "role": getattr(user, "role", "N/A"),
        "xp": me.get("totalXp"),
        "hearts": me.get("hearts"),
        "streak": me.get("streakDays", 0),
    },
    "daily_plan": {
        "is_completed": getattr(daily, "is_completed", None),
        "total": getattr(daily, "total_questions", None),
        "answered": getattr(daily, "answered_questions", None),
        "reward_claimed": getattr(daily, "reward_claimed", None)
    },
    "levels": [
        {
            "order": l.order_index,
            "title": l.title,
            "completed": l.is_completed,
            "locked": l.is_locked
        }
        for l in prog.levels
    ],
    "kb_count": kb_count,
    "leaderboard_preview": lb if isinstance(lb, list) else getattr(lb, "rankings", str(lb))[:3] if hasattr(lb, "rankings") else str(lb)[:200]
}

print(json.dumps(out, indent=2, ensure_ascii=False))
