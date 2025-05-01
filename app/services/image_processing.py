import os
from PIL import Image
from typing import List
import numpy as np
import supervision as sv
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.models.model_loader import run_qwen_2_5_vl_inference, processor, model
import json

OUTPUT_DIR = "output"
SYSTEM_MESSAGE = None
COMMON_SIZE = (1024, 1024)  # You can change this to your model's expected input size

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_single_image(image_path: str, violation: str):
    """Process and annotate a single image."""
    box_annotator = sv.BoxAnnotator(color_lookup=sv.ColorLookup.INDEX)
    label_annotator = sv.LabelAnnotator(color_lookup=sv.ColorLookup.INDEX)

    try:
        PROMPT = """Detect and outline the position of all persons working at height. Additionally, identify if any worker is (1) smoking a cigarette or (2) using a mobile phone. Output all relevant coordinates and detected actions STRICTLY in JSON format."""
        # Load and resize image
        image = Image.open(image_path)
        original_size = image.size
        image = image.resize(COMMON_SIZE)
        #resolution_wh = image.size
        
        # Run inference
        response, input_wh = run_qwen_2_5_vl_inference(
            model=model,
            processor=processor,
            image=image,
            prompt=PROMPT,
            system_message = SYSTEM_MESSAGE
        )
        print(f"Results for {image_path}:")
        print(response)
        # Clean up the response if needed
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Could not parse JSON: {e}")
            print(f"Response was: {response!r}")
            data = None  # or handle as needed
        boxes = []
        labels = []
        for item in data:
            if "bbox_2d" in item and "label" in item:
                boxes.append(item["bbox_2d"])
                labels.append(item["label"])
        xyxy = np.array(boxes, dtype=np.float32)
        detections = sv.Detections(
            xyxy=xyxy,
            class_id=None,
            confidence=None,
            data={"class_name": labels}
        )
        # Annotate image
        annotated_image = np.array(image.copy())
        annotated_image = box_annotator.annotate(scene=annotated_image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
        # Save result
        output_path = os.path.join(OUTPUT_DIR, f"annotated_{os.path.basename(image_path)}")
        Image.fromarray(annotated_image).convert('RGB').save(output_path)
        print(f"Saved annotated image to {output_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")

def process_and_save_images(image_paths: List[str], violation: str, max_workers: int = 1):
    """Parallel image processing using threads."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_image, path, violation) for path in image_paths]
        for future in as_completed(futures):
            future.result()  # to raise any exceptions if occurred 