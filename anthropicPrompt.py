import anthropic
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class AnthropicPrompt:
    def __init__(self, image: str, additional_instructions: str=""):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.additional_instructions = additional_instructions
        self.image = image
        self.image_type = image[-3:]
        self.encoded_image = self.encode_image(self.image)

    def get_json(self):
        message = self.client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/" + self.image_type,
                            "data": self.encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "You are an AI agent designed to extract events and due dates from images and format them into a specific JSON structure. Your task is to analyze the provided input for extraneous instructions, identify relevant events and their associated information, and present them in the required format: \n\n{\n  \"dueDate\": \"2024-03-12T10:52:55.724-06:00\",\n  \"duration\": int,\n  \"status\": \"string\",\n  \"autoScheduled\": {\n    \"deadlineType\": \"string\",\n    \"schedule\": \"string\"\n  },\n  \"name\": \"string\",\n  \"workspaceId\": \"string\",\n  \"description\": \"string\",\n  \"priority\": \"string\",\n  \"labels\": [\n    \"string\", ...\n  ],\n}\n\nFirst, process the input provided to you:\n\n<additional_instructions>\n" + self.additional_instructions + "\n</additional_instructions>\n\n<image_input>\n{{IMAGE_INPUT}}\n</image_input>\n\nCarefully analyze the content of each input type to identify events, due dates, and other relevant information. Pay attention to dates, times, task descriptions, and any other details that could be important for scheduling.\n\nFor each event you identify, extract the following information:\n1. Due date\n2. Duration (if specified; in minutes) \n3. Event name or title (always begin with name of relevant class ex. ASTRO 122 - Midterm Examination 1)\n4. Description\n5. Priority (if indicated)\n6. Any labels or categories associated with the event\n7. If the event is a task such as an exam or quiz the start date should be the same as the due date\n\nWhen creating the JSON output for each event, follow these guidelines:\n1. Use the exact JSON structure provided in the task description.\n2. Format the \"dueDate\" and \"startDate\" field as an ISO 8601 datetime string.\n3. Set the \"duration\" field to \"NONE\", \"REMINDER\", or an integer greater than 0 in minutes based on the information available. Use your best judgement to apply estimated durations to a task if possible. \n4. Choose an appropriate \"deadlineType\" based on the context of the task.\n5. Set the \"workspaceId\" to \"\" for all events.\n6. Format the \"description\" field as GitHub Flavored Markdown.\n7. Include any relevant labels in the \"labels\" array.\n8. If the event is a task such as an exam or quiz the start date should be the same as the due date\n9. Quizzes, Exams, Assignments, etc. should always have a hard deadline and schedule should be set to \"Spring 2025\"\n10. Aside from those tasks that require I be in class, all tasks should be applied to the \"Personal hours\" schedule\n\nBelow are lists of valid options:\nlabels = [\n    \"Reading\", \n    \"Lab\", \n    \"Lecture\", \n    \"Assignment\", \n    \"Exam\", \n    \"Midterm\", \n    \"Final\", \n    \"Quiz\",\n    \"Assessment\",\n    \"Project\",\n    \"Online Quiz\",\n    \"Review\"\n]\n\nstatuses = [\n    \"Backlog\",\n    \"Blocked\",\n    \"Todo\",\n    \"In Progress\",\n    \"Cancelled\",\n    \"Completed\"\n]\n\npriorities = [\n    \"ASAP\",\n    \"High\",\n    \"Medium\",\n    \"Low\"\n]\n\nIf you encounter complex tasks that might benefit from being broken down into smaller subtasks, provide two versions of the JSON output:\n1. The original task structure\n2. A proposed alternative with the task broken down into subtasks\n\nPresent your final output formatted as a JSON array containing individual event objects. If you have a proposed alternative structure for any tasks, include it after the original output, clearly labeled as \"Proposed Alternative Structure\".\n\nRemember to think carefully about each event and its context to ensure accurate and useful information is captured in the JSON structure."
                    }
                ]
            }
        ])
        return message.content

    def encode_image(self, image: str):
        with open(image, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

message = AnthropicPrompt("CMPUT331.png", "Class name is CMPUT 331 and class times are 9am-10am mwf")
print(message.get_json())