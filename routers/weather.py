from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class WeatherResponse(BaseModel):
    city: str
    temperature: str
    condition: str
    rainfall: str

# Dummy data variations
weather_data = [
    {"temperature": "30°C", "condition": "Sunny ☀️", "rainfall": "No rain today"},
    {"temperature": "25°C", "condition": "Cloudy ☁️", "rainfall": "Light showers expected"},
    {"temperature": "20°C", "condition": "Rainy 🌧️", "rainfall": "Heavy rainfall likely"},
]

@router.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    forecast = random.choice(weather_data)  # pick one randomly
    return {"city": city.title(), **forecast}
