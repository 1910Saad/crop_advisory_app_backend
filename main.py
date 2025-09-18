from fastapi import FastAPI
from routers import chatbot, fertilizer, market, weather, pest

app = FastAPI(title="Smart Crop Advisory Backend")

# Register endpoints
app.include_router(chatbot.router)
app.include_router(fertilizer.router)
app.include_router(market.router)
app.include_router(weather.router)
app.include_router(pest.router)

@app.get("/")
async def root():
    return {"message": "Smart Crop Advisory Backend is running 🚀"}
