from fastapi import APIRouter, Query
import requests
import os
import json
import re

router = APIRouter()

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

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

def fetch_crop_thresholds(crop: str):
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = (
        f"Provide optimal weather thresholds for growing {crop} in JSON format. "
        "Include max_temp, min_temp, max_humidity, min_humidity. Example: "
        '{"max_temp": 35, "min_temp": 10, "max_humidity": 80, "min_humidity": 30}'
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    try:
        match = re.search(r'\{.*\}', response.text, flags=re.DOTALL)
        if match:
            thresholds = json.loads(match.group())
            return thresholds
        else:
            return None
    except Exception:
        return None

def generate_advisory(weather_data: dict, thresholds: dict):
    if not thresholds:
        return ["No advisory available for this crop (thresholds missing)"]

    t = weather_data["temperature"]
    h = weather_data["humidity"]

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
async def get_weather(city: str = Query(...), crop: str = Query(...)):
    weather_data = fetch_weather(city)
    if "error" in weather_data:
        return weather_data

    thresholds = fetch_crop_thresholds(crop.lower())
    advisory = generate_advisory(weather_data, thresholds)
    return {
        "city": city,
        "crop": crop,
        "weather_data": weather_data,
        "thresholds": thresholds,
        "advisory": advisory
    }