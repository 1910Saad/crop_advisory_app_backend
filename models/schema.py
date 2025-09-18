from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    reply: str

class FertilizerRequest(BaseModel):
    crop: str
    soil: str

class FertilizerResponse(BaseModel):
    recommendation: str
