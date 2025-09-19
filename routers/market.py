from fastapi import APIRouter, Query
from models.schema import MarketPrice

router = APIRouter()

# Dummy mandi price dataset
dummy_prices = [
    {"crop": "Wheat", "price": 2100, "location": "Ludhiana"},
    {"crop": "Rice", "price": 1800, "location": "Amritsar"},
    {"crop": "Maize", "price": 1600, "location": "Patiala"},
    {"crop": "Mustard", "price": 5200, "location": "Bathinda"},
]

@router.get("/market/", response_model=MarketPrice)
async def get_market_price(
    crop: str = Query(..., description="Crop name"),
    location: str = Query(..., description="Market location"),
):
    for item in dummy_prices:
        if item["crop"].lower() == crop.lower() and item["location"].lower() == location.lower():
            return item
    return {"crop": crop, "price_per_quintal": 2000, "location": location}
