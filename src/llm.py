from hidden.key import API_KEY
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from logs import *

client = genai.Client(api_key=API_KEY)

def get_description(link):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Da-mi o descriere de o propozitie a continutului: {link}",
            config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
            ),
        )
        return response.text
    except ClientError as e:
        if "RESOURCE_EXHAUSTED" in str(e):
            print(f"[Quota exceeded] Skipping article: {link}")
            logging.warning("Quota of requests exceeded - skipping...")
            return None
        else:
            print(f"[ClientError] Unexpected error: {e}")
            logging.error(f"Unexpected error: {e}...")
            return None