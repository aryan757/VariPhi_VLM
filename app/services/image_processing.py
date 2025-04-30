import os
from PIL import Image
from typing import List
import numpy as np
import supervision as sv
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.models.model_loader import run_qwen_2_5_vl_inference, processor, model

OUTPUT_DIR = "output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_single_image(image_path: str):
    """Process and annotate a single image."""
    box_annotator = sv.BoxAnnotator(color_lookup=sv.ColorLookup.INDEX)
    label_annotator = sv.LabelAnnotator(color_lookup=sv.ColorLookup.INDEX)

    try:
        # PROMPT = """Outline the position of all the person that are working on some height and output all the coordinates in STRICTLY in JSON format."""
        PROMPT = """Detect and outline the position of all persons working at height. Additionally, identify if any worker is (1) smoking a cigarette or (2) using a mobile phone. Output all relevant coordinates and detected actions STRICTLY in JSON format."""


        # Load image
        image = Image.open(image_path)
        resolution_wh = image.size

        # Run inference
        response, input_wh = run_qwen_2_5_vl_inference(
            model=model,
            processor=processor,
            image=image,
            prompt=PROMPT
        )

        print(f"Results for {image_path}:")
        print(response)

        # Parse detections
        detections = sv.Detections.from_vlm(
            vlm=sv.VLM.QWEN_2_5_VL,
            result=response,
            input_wh=input_wh,
            resolution_wh=resolution_wh
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


def process_and_save_images(image_paths: List[str], max_workers: int = 1):
    """Parallel image processing using threads."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_image, path) for path in image_paths]
        for future in as_completed(futures):
            future.result()  # to raise any exceptions if occurred 