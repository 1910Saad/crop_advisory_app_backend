from fastapi import APIRouter
from models.schema import FertilizerRequest, FertilizerResponse

router = APIRouter()

@router.post("/fertilizer/", response_model=FertilizerResponse)
async def fertilizer_advice(req: FertilizerRequest):
    if req.crop.lower() == "wheat" and req.soil.lower() == "loam":
        advice = "Use NPK 120:60:40 for best yield."
    else:
        advice = "Apply organic manure and consult local agri office."

    return FertilizerResponse(recommendation=advice)
