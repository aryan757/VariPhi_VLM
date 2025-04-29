from fastapi import APIRouter, UploadFile, File
from app.services.image_processing import process_and_save_images
from typing import List

router = APIRouter()

@router.post("/process-images/")
async def process_images(files: List[UploadFile] = File(...)):
    image_paths = []
    for file in files:
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        image_paths.append(file_location)
    process_and_save_images(image_paths)
    return {"message": "Images processed successfully"} 