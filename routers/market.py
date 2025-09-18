from fastapi import APIRouter

router = APIRouter()

sample_data = {
    "prices": [
        {"crop": "Wheat", "price": "₹2000/quintal"},
        {"crop": "Rice", "price": "₹1800/quintal"},
        {"crop": "Cotton", "price": "₹5500/quintal"}
    ]
}

@router.get("/market/")
async def get_market_prices():
    return sample_data
