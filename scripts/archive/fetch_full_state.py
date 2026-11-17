import json
from api.client import BaseClient

client = BaseClient()
me = client.get("/progress/me")
daily = client.get("/mobile/daily-plan/today")

lb_org = None
try:
    lb_org = client.get("/leaderboard/organization", params={"limit": 10})
except Exception as e:
    lb_org = str(e)

lb_global = None
try:
    lb_global = client.get("/leaderboard/global", params={"limit": 10})
except Exception as e:
    lb_global = str(e)

levels = me.get("levels", [])
level_details = []
for lvl in levels:
    lvl_id = lvl.get("id")
    try:
        det = client.get(f"/progress/level/{lvl_id}")
        level_details.append(det)
    except Exception as e:
        level_details.append({"error": str(e), "id": lvl_id})

full_status = {
    "me": me,
    "daily": daily,
    "lb_org": lb_org,
    "lb_global": lb_global,
    "level_details": level_details
}

with open("data/current_live_state.json", "w", encoding="utf-8") as f:
    json.dump(full_status, f, ensure_ascii=False, indent=2)

print("Saved current live state to data/current_live_state.json")
