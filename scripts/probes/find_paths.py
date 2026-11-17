import requests
import re
from config import Config

url = "https://elektrolearn-mobile.uzbekistonmet.uz/assets/index-DGWZSvMV.js"
js = requests.get(url, headers={"User-Agent": Config.USER_AGENT}).text

# Look for axios or client base url / endpoints
urls = re.findall(r'`/[a-zA-Z0-9_\-\/]+`', js)
print("Template literals paths:")
for u in sorted(set(urls)):
    if any(k in u for k in ["progress", "heart", "exam", "lesson", "plan", "user", "auth", "theor"]):
        print(" ", u)

