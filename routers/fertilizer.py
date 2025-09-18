from fastapi import APIRouter
from models.schema import FertilizerRequest, FertilizerResponse

router = APIRouter()

@router.post("/fertilizer/", response_model=FertilizerResponse)
async def fertilizer_advice(req: FertilizerRequest):
    if req.crop.lower() == "wheat" and req.soil.lower() == "loamy":
        advice = "Use NPK 120:60:40 for best yield."
    else:
        advice = "Apply organic manure and consult local agri office."
    return {"recommendation": advice}
