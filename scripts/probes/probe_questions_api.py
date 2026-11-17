import requests
import json
from config import Config

token = Config.get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": Config.USER_AGENT
}

level5_id = "f15546e6-82ac-4d89-ad78-b9ef37009aea"
t1_id = "54778b29-a10e-4fb9-8b80-b4c36bc4d6dc" # 140 questions theory

print(f"=== TESTING ENDPOINTS FOR THEORY {t1_id} ===")

modes_to_test = [
    {"mode": "continue"},
    {"mode": "retry"},
    {"mode": "all"},
    {"mode": "exam"},
    {"mode": "full"},
    {"mode": "list"},
    {"mode": "continue", "limit": 200},
    {"mode": "all", "limit": 200},
    {"mode": "continue", "pageSize": 200},
    {"mode": "continue", "take": 200},
    {"mode": "continue", "perPage": 200},
]

for p in modes_to_test:
    r = requests.get(f"{Config.BASE_URL}/theories/{t1_id}/questions", headers=headers, params=p)
    if r.status_code == 200:
        data = r.json()
        qs = data.get("questions", [])
        print(f"Params {p} -> Status 200! Questions returned: {len(qs)}, total_questions in resp: {data.get('total_questions')}")
    else:
        print(f"Params {p} -> Status {r.status_code}")

# Other endpoints
endpoints_to_test = [
    f"/theories/{t1_id}",
    f"/theories/{t1_id}/full",
    f"/theories/{t1_id}/test",
    f"/theories/{t1_id}/exam",
    f"/theories/{t1_id}/all",
    "/questions",
    f"/questions?theoryId={t1_id}",
    f"/questions?levelId={level5_id}",
    "/exams",
    "/exams/live",
    "/exams/available",
    "/progress/level/" + level5_id,
]

print("\n=== TESTING OTHER DIRECT ENDPOINTS ===")
for ep in endpoints_to_test:
    r = requests.get(f"{Config.BASE_URL}{ep}", headers=headers)
    print(f"GET {ep} -> Status: {r.status_code}")
    if r.status_code == 200:
        try:
            d = r.json()
            if isinstance(d, list):
                print(f"   List response with {len(d)} items: {json.dumps(d[:2], ensure_ascii=False)[:200]}")
            elif isinstance(d, dict):
                keys = list(d.keys())
                print(f"   Dict response keys: {keys}")
                for k in ["questions", "theories", "exams"]:
                    if k in d:
                        print(f"      Key '{k}' has len {len(d[k])}")
        except Exception as e:
            print(f"   Response text: {r.text[:100]}")
