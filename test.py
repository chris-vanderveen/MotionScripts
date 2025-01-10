import requests

url = "https://api.usemotion.com/v1/workspaces"

headers = {
    "Accept": "application/json",
    "X-API-Key": "rD+qm05oziQltkZAxagyYKv7BNH2MkZ9sQNYK49Plhc="
}

response = requests.get(url, headers=headers)

print(response.json())