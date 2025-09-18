from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/pest/")
async def detect_pest(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "prediction": "Detected: Aphid 🐛",
        "confidence": "92%"
    }
