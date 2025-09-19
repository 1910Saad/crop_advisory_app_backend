from fastapi import FastAPI
from routers import chatbot, fertilizer, market, weather, pest

app = FastAPI(title="Smart Crop Advisory Backend")

# Register routers with prefixes
app.include_router(chatbot.router, prefix="/api/chatbot")
app.include_router(fertilizer.router, prefix="/api/fertilizer")
app.include_router(market.router, prefix="/api/market")
app.include_router(weather.router, prefix="/api/weather")
app.include_router(pest.router, prefix="/api/pest")

@app.get("/")
async def root():
    return {"message": "Smart Crop Advisory Backend is running 🚀"}
