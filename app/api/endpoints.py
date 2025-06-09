from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.image_processing import process_and_save_images 
from app.services.image_processing import process_single_image
from typing import List, Optional
from fastapi import Body
import cv2
import os
from PIL import Image

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

@router.post("/process_video/")
async def process_video(
    violation: Optional[str] = Form(None)
):
    # Hardcoded video file path
    file_location = "/home/ai/VLLM/VariPhi_VLM/app/api/Untitled.mp4"
    
    # Open video file directly from path
    cap = cv2.VideoCapture(file_location)
    frame_count = 0

    # Create output directory if it doesn't exist
    os.makedirs("output_inferencing", exist_ok=True)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process every 40th frame
        if frame_count % 400 != 0:
            frame_count += 1
            continue
            
        # Convert frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Save frame temporarily
        frame_path = f"temp/frame_{frame_count}.jpg"
        pil_image.save(frame_path)
        
        # Process frame
        process_single_image(frame_path, violation)
        
        frame_count += 1
        
    cap.release()
    return {"message": "Video processed successfully"}
