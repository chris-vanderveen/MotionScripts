from taskPost import get_workspace_id
from dotenv import load_dotenv
import os
import requests

load_dotenv()

class Task:
    """
    A class to represent a task
    """
    headers: dict
    def __init__(self, payload):
        self.payload = payload
        self.headers = {
            "Accept": "application/json",
            "X-API-Key": os.getenv("API_KEY")
            }
        self.workspace_id = get_workspace_id(self.headers)

    def get_payload(self):
        """
        Get the payload for the task

        :return: The payload for the task
        :rtype: dict
        """
        return self.payload
    
    def get_workspace_id(self) -> str:
        """
        Get the workspace ID from the workspace

        :param headers: The headers to use for the request
        :type headers: dict
        :return: The workspace ID
        :rtype: str
        """
        url = os.getenv("MOTION_SERVER") + "/workspaces"
        response = requests.get(url, headers=self.headers)
        return response.json()["workspaces"][0]["id"]