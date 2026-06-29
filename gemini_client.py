import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except ClientError as e:
        return (
            "ERROR: Gemini API quota exceeded.\n\n"
            "Please wait a minute and try again, or check your Gemini API quota."
        )