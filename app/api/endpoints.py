from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.image_processing import process_and_save_images 
from app.services.image_processing import process_single_image
from typing import List, Optional
from fastapi import Body

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
    file: UploadFile = File(None),
    #image_url: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
    violation: Optional[str] = Form(None)

):
    if file is not None:
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        print("this is the file location", file_location)
        process_single_image(file_location, violation)
        return {"message": "Image processed successfully (file)"}
    elif image_url is not None:
        process_single_image(image_url, violation)
        return {"message": "Image processed successfully (url)"}
    else:
        raise HTTPException(status_code=400, detail="Either file or image_url must be provided.")

