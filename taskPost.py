import requests
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    "Accept": "application/json",
    "X-API-Key": os.getenv("API_KEY"),
}

def get_workspace_id(headers) -> str:
    url = "https://api.usemotion.com/v1/workspaces"
    response = requests.get(url, headers=headers)
    return response.json()[0]['id']

def post_task(payload, headers) -> dict:
    url = "https://api.usemotion.com/v1/tasks"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# REMINDER: Rate limit is 12 requests per minute
if __name__ == "__main__":
    workspace_id = get_workspace_id(headers)
    # TODO: Add code to post tasks to the workspace
    # TODO: Add code to handle rate limiting
    # TODO: Add code to handle errors
    # TODO: Add code to handle success
    # TODO: Add code to handle logging
    # TODO: Add code to handle user input
    # TODO: Add code to handle user input for workspace ID
    # TODO: Add code to handle user input for task file
    # TODO: Add code to handle user input for rate limit
