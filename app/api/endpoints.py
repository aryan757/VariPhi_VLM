from fastapi import APIRouter, UploadFile, File, Form
from app.services.image_processing import process_and_save_images 
from app.services.image_processing import process_single_image
from typing import List, Optional

router = APIRouter()

@router.post("/process-images/")
async def process_images(
    files: List[UploadFile] = File(...),
    violation: Optional[str] = Form(None)
):
    image_paths = []
    for file in files:
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        image_paths.append(file_location)
    process_and_save_images(image_paths, violation)
    return {"message": "Images processed successfully"} 

@router.post("/process-image/")
async def process_image(
    file: UploadFile = File(...),
    violation: Optional[str] = Form(None)
):
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    process_single_image(file_location, violation)
    return {"message": "Image processed successfully"}

