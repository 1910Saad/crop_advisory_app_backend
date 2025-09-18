from fastapi import APIRouter
from models.schema import ChatRequest, ChatResponse
from google.genai import Client
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

router = APIRouter()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = Client(api_key=GEMINI_API_KEY)

# Retry configuration
MAX_RETRIES = 3
DELAY = 2  # seconds

def generate_with_retry(prompt: str) -> str:
    """
    Generate response from Gemini with retries for 503 errors.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",  # You can change the model
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Check if it's a 503 error
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"Model overloaded, retrying... ({attempt+1}/{MAX_RETRIES})")
                time.sleep(DELAY)
            else:
                # Other errors, return as message
                return f"Error contacting Gemini: {str(e)}"
    return "Sorry, the AI model is temporarily unavailable. Please try again later."

@router.post("/chatbot/", response_model=ChatResponse)
async def chatbot_reply(req: ChatRequest):
    reply_text = generate_with_retry(req.query)
    return {"reply": reply_text}
