import requests
from dotenv import load_dotenv
import os
import json
import time
import sys
load_dotenv()

labels = [
    "Reading", 
    "Lab", 
    "Lecture", 
    "Assignment", 
    "Exam", 
    "Midterm", 
    "Final", 
    "Quiz",
    "Assessment",
    "Project",
    "Online Quiz",
    "Review"
]

statuses = [
    "Backlog",
    "Blocked",
    "Todo",
    "In Progress",
    "Cancelled",
    "Completed"
]

priorities = [
    "ASAP",
    "High",
    "Medium",
    "Low"
]

headers = {
    "Accept": "application/json",
    "X-API-Key": os.getenv("API_KEY"),
}

def get_workspace_id(headers) -> str:
    """
    Get the workspace ID from the workspace

    :param headers: The headers to use for the request
    :type headers: dict
    :return: The workspace ID
    :rtype: str
    """
    url = "https://api.usemotion.com/v1/workspaces"
    response = requests.get(url, headers=headers)
    return response.json()["workspaces"][0]["id"]

def post_task(payload, headers) -> dict:
    """
    Post a task to the workspace

    :param payload: The task to post
    :type payload: dict
    :param headers: The headers to use for the request
    :type headers: dict
    :return: The response from the request
    :rtype: dict
    """
    url = "https://api.usemotion.com/v1/tasks"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def get_tasks(headers) -> list[dict]:
    """
    Get all tasks from the workspace

    :param headers: The headers to use for the request
    :type headers: dict
    :return: The tasks from the workspace
    :rtype: list[dict]
    """
    url = "https://api.usemotion.com/v1/tasks"
    response = requests.get(url, headers=headers)
    return response.json()

# REMINDER: Rate limit is 12 requests per minute
if __name__ == "__main__":
    if len(sys.argv) == 1:
        tasks = get_tasks(headers)
        print(tasks)
        exit()
    elif len(sys.argv) == 2:  
        target = sys.argv[1]

    with open(target, "r") as json_tasks:
        tasks = json_tasks.read()
        tasks = json.loads(tasks)

    for task in tasks:
        task["workspaceId"] = get_workspace_id(headers)
        print(task)
        if input("Continue? (y/n) ") == "n":
            # Modify the task if needed
            # TODO: Add code to modify the task
            pass
        else:
            response = post_task(task, headers)
            print(response)
            # Post every tenth of a second to avoid rate limiting
            time.sleep(1/10)

    # TODO: Add code to handle errors
    # TODO: Add code to handle success
    # TODO: Add code to handle logging
    # TODO: Add code to handle user input for workspace ID
    # TODO: Add code to handle user input for task file
    # TODO: Add code to handle user input for rate limit
