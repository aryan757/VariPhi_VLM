import cv2
import numpy as np

# Path to the image
image_path = "testing_image/imagee_18.jpg"
output_path = "output_imagee_18.jpg"

# Provided bounding boxes and labels
boxes = [
    [304, 235, 419, 418],
    [476, 255, 553, 442],
    [147, 319, 237, 428],
    [358, 162, 410, 229],
    [355, 31, 400, 140],
    [398, 26, 440, 130],
    [229, 106, 298, 169],
    [22, 84, 84, 150]
]
labels = [
    "persons working at height",
    "persons working at height",
    "persons working at height",
    "persons working at height",
    "persons working at height",
    "persons working at height",
    "persons working at height",
    "persons working at height"
]

def plot_bounding_boxes(image_path, boxes, labels, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open image: {image_path}")
    height, width = image.shape[:2]
    for box, label in zip(boxes, labels):
        x1, y1, x2, y2 = map(int, box)
        # Clip coordinates to image size
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width-1, x2), min(height-1, y2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Use a shorter label and smaller font
        short_label = label[:15] + "..." if len(label) > 15 else label
        font_scale = 0.5
        thickness = 1
        # Draw label inside the box
        cv2.putText(image, short_label, (x1 + 2, y1 + 15), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (36, 255, 12), thickness)
    cv2.imwrite(output_path, image)
    print(f"Saved result to {output_path}")

if __name__ == "__main__":
    plot_bounding_boxes(image_path, boxes, labels, output_path) 