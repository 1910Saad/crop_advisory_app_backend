from fastapi import APIRouter
from models.schema import ChatRequest, ChatResponse
from google import genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

router = APIRouter()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Retry configuration
MAX_RETRIES = 3
DELAY = 2  # seconds

# System context for agriculture
SYSTEM_PROMPT = """
You are Krishi Mitra, a smart farming assistant for Indian farmers.
Your job is to provide helpful, simple, and practical advice about:
- Crop management
- Soil health and fertilizer use
- Pest and disease control
- Water management and irrigation
- Weather-based crop planning
- Market prices and mandi trends

Rules:
- Only answer agriculture-related queries. If farmer asks something else (e.g., politics, sports), politely refuse.
- Reply in the same language as the farmer’s query.
- Keep answers short, clear, and farmer-friendly.
- If giving instructions (like fertilizer dose), provide safe, practical guidelines.
"""

def generate_with_retry(user_query: str) -> str:
    """
    Generate response from Gemini with retries for 503 errors.
    """
    for attempt in range(MAX_RETRIES):
        try:
            # Inject system + user context
            prompt = f"{SYSTEM_PROMPT}\n\nFarmer’s Query: {user_query}\n\nAnswer:"
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"Model overloaded, retrying... ({attempt+1}/{MAX_RETRIES})")
                time.sleep(DELAY)
            else:
                return f"Error contacting Gemini: {str(e)}"
    return "Sorry, the AI model is temporarily unavailable. Please try again later."

@router.post("/chatbot/", response_model=ChatResponse)
async def chatbot_reply(req: ChatRequest):
    reply_text = generate_with_retry(req.query)
    return {"reply": reply_text}
