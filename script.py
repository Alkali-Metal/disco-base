import requests, os

#https://developer.github.com/v3/gists/#get-a-single-gist


base_url = "https://api.github.com/gists/274ba7bc979bc4dbddeceef0e1c8c973"

headers = {
    "Authorization": "token ab080627bef11fe4d17876a5bd3abc85f8c07adb"
}

data = requests.get(
    base_url,
    headers=headers
).json()["files"]

for file in data:
    with open(file, 'w') as potato:
        potato.write(data[file]["content"])