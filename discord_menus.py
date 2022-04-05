import os
import sys
import json
import requests
all_food = {}
paths = ["breakfast", "lunch", "dinner"]
for path in paths:
    full_path = "/home/ubuntu/menus/" + path
    f = open(full_path)
    all_food[path.capitalize()]=json.load(f)
print({"menu":all_food})
print("Sending json\n")
heads = {"X-API-KEY":os.environ['X-API-KEY']}
r = requests.post("https://auth.dilanxd.com/nu-discord/dining-menu", json={"menu":all_food}, headers=heads)
print("Status code: ")
print(str(r.status_code))
print("\n")
r.json()
