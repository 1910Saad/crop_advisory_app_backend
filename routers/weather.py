from fastapi import APIRouter, Query
import requests

router = APIRouter()

# Directly declare your OpenWeatherMap API key
API_KEY = "11af4d539c4a1c02758024a29171351f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Crop-specific thresholds for advisories
CROP_THRESHOLDS = {
    "wheat": {
        "max_temp": 35,
        "min_temp": 10,
        "max_humidity": 80,
        "min_humidity": 30
    },
    "rice": {
        "max_temp": 38,
        "min_temp": 20,
        "max_humidity": 90,
        "min_humidity": 50
    },
    "cotton": {
        "max_temp": 40,
        "min_temp": 18,
        "max_humidity": 70,
        "min_humidity": 30
    }
}

def fetch_weather(city: str):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    res = requests.get(BASE_URL, params=params)
    if res.status_code != 200:
        return {"error": "City not found or API error"}
    data = res.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

def generate_advisory(crop: str, weather_data: dict):
    if crop not in CROP_THRESHOLDS:
        return "No advisory available for this crop"
    
    t = weather_data["temperature"]
    h = weather_data["humidity"]
    thresholds = CROP_THRESHOLDS[crop]

    advisories = []

    if t > thresholds["max_temp"]:
        advisories.append("High temperature: cover or irrigate crop to prevent heat stress")
    elif t < thresholds["min_temp"]:
        advisories.append("Low temperature: protect crop from frost or cold stress")

    if h > thresholds["max_humidity"]:
        advisories.append("High humidity: watch for fungal diseases")
    elif h < thresholds["min_humidity"]:
        advisories.append("Low humidity: irrigation recommended")

    if "rain" in weather_data["weather"].lower():
        advisories.append("Rain expected: delay pesticide/fertilizer spraying")

    if not advisories:
        advisories.append("Weather conditions are ideal today")

    return advisories

@router.get("/weather/")
async def get_weather(city: str = Query(...), crop: str = Query("wheat")):
    weather_data = fetch_weather(city)
    if "error" in weather_data:
        return weather_data
    
    advisory = generate_advisory(crop.lower(), weather_data)
    return {
        "city": city,
        "crop": crop,
        "weather_data": weather_data,
        "advisory": advisory
    }
