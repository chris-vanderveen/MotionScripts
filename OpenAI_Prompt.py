from openai import OpenAI
import base64
import sys

class OpenAI_Prompt:
    def __init__(self, image: str, additional_instructions: str=""):
        self.file_type = image.split(".")[-1]
        self.image = self.encode_image(image)
        self.additional_instructions = additional_instructions
        self.client = OpenAI()

    def encode_image(self, image: str):
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def extract_text(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "developer",
                "content": [
                    {
                    "type": "text",
                    "text": "Extract text from a given image of a table and return it as formatted text.\n\nTo ensure optimal results, follow these guidelines:\n\n- The input will be an image file containing a table.\n- The output should accurately reflect the table's structure, converting rows and columns into a readable text format.\n- Ensure all text is extracted correctly, preserving any table headers or footnotes present in the image.\n\n# Steps\n\n1. **Image Processing:**\n   - Load the image and apply any necessary pre-processing (e.g., scaling or grayscale conversion) to improve text recognition accuracy.\n\n2. **Text Extraction:**\n   - Use Optical Character Recognition (OCR) technology to capture the text from the image.\n   - Ensure the extracted text maintains the integrity of columns and rows as seen in the input image.\n\n3. **Text Formatting:**\n   - Convert the extracted text into a structured format, such as CSV or Markdown table, ensuring readability.\n\n# Output Format\n\n- Present the extracted text in a clear and structured form, for instance, as a Markdown table or CSV format aligning with the table's original layout.\n\n# Examples\n\n**Example:** [Image of Table] contains:\n- Header: Name, Age, Occupation\n- Data: John Doe, 30, Engineer; Jane Smith, 25, Artist\n\n**Expected Output:**\n\n```\n| Name     | Age | Occupation |\n|----------|-----|------------|\n| John Doe | 30  | Engineer   |\n| Jane Smith | 25 | Artist     |\n```\n\n# Notes\n\n- Ensure any non-standard characters or formatting from the image are accurately captured.\n- If text extraction errors occur, handle them gracefully and provide a note in the output if any text is unextractable.\n- Ensure the agent's underlying OCR model is up-to-date for optimal performance."
                    }
                ]
                },
                {
                "role": "user",
                "content": self.additional_instructions
                },
                {
                "role": "user",
                "content": [
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{self.file_type};base64,{self.image}",
                    }
                    }
                ]
                }
            ],
            response_format={
                "type": "text"
            },
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        return response.choices[0].message.content
    
if __name__ == "__main__":
    image = sys.argv[1]
    additional_instructions = input("Enter additional instructions: ")
    openai_prompt = OpenAI_Prompt(image, additional_instructions)
    print(openai_prompt.extract_text())