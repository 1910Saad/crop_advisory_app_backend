from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    reply: str

class FertilizerRequest(BaseModel):
    crop: str
    soil: str
    region: str

class FertilizerResponse(BaseModel):
    recommendation: str


class MarketPrice(BaseModel):
    crop: str
    price_per_quintal: int
    location: str

class MarketPriceResponse(BaseModel):
    prices: List[MarketPrice]

