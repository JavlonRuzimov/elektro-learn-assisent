import sys
import os
sys.path.insert(0, os.path.abspath("."))
from api import ElektroLearnClient

client = ElektroLearnClient()

# Check user profile & progress
prog = client.base_client.get("/progress/me")
print("Progress Me:", prog)

# Check hearts
hearts = client.base_client.get("/hearts/me")
print("\nHearts:", hearts)

# Check daily plan
dp = client.daily_plan.get_today()
print("\nDaily Plan:", dp)

# Check leaderboard GLOBAL ALL_TIME
lb_all = client.base_client.get("/leaderboard?type=GLOBAL&period=ALL_TIME&limit=5")
print("\nLeaderboard Top 5 ALL_TIME:", lb_all)

# Check leaderboard GLOBAL WEEKLY / MONTHLY
lb_week = client.base_client.get("/leaderboard?type=GLOBAL&period=WEEKLY&limit=5")
print("\nLeaderboard Top 5 WEEKLY:", lb_week)

# Check leaderboard ORGANIZATION
lb_org = client.base_client.get("/leaderboard?type=ORGANIZATION&period=ALL_TIME&limit=5")
print("\nLeaderboard Top 5 ORG:", lb_org)

# Check my rank in leaderboard
lb_me = client.base_client.get("/leaderboard/me?type=GLOBAL&period=ALL_TIME")
print("\nLeaderboard Me (GLOBAL ALL_TIME):", lb_me)

lb_me_org = client.base_client.get("/leaderboard/me?type=ORGANIZATION&period=ALL_TIME")
print("\nLeaderboard Me (ORG ALL_TIME):", lb_me_org)
