from fastapi import APIRouter

router = APIRouter()

@router.get("/weather/{city}")
async def get_weather(city: str):
    return {
        "city": city,
        "temperature": "30°C",
        "condition": "Sunny ☀️",
        "rainfall": "No rain today"
    }
