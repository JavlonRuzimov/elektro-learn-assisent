import sys
import os
sys.path.insert(0, os.path.abspath("c:/Users/Administrator/Desktop/ElektroLearn"))
import requests
import re
from config import Config

url = "https://elektrolearn-mobile.uzbekistonmet.uz/assets/index-DGWZSvMV.js"
try:
    js = requests.get(url, headers={"User-Agent": Config.USER_AGENT}).text
    eps = re.findall(r'["\'](/(?:api/|auth/|progress/|theories/|daily-plan/|leaderboard/|exam/|certificates/|users/|mobile/)[^"\']*)["\']', js)
    for ep in sorted(set(eps)):
        print(" ", ep)
except Exception as e:
    print(e)
