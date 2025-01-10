import requests

url = "https://api.usemotion.com/v1/workspaces"

headers = {
    "Accept": "application/json",
    "X-API-Key": ""
}

response = requests.get(url, headers=headers)

print(response.json())
