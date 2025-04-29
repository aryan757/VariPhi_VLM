# FastAPI Image Annotation Application

This application is a FastAPI-based service for processing and annotating images using the Qwen2.5-VL model. It processes images in batches and outputs annotated images.

## Project Structure

```
vlms/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── image_processing.py
│   └── models/
│       ├── __init__.py
│       └── model_loader.py
│
├── requirements.txt
└── README.md
```

## Setup

1. **Install Dependencies**: Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**: Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API**: The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Usage

- **Endpoint**: `/process-images/`
  - **Method**: POST
  - **Description**: Upload images to be processed and annotated.
  - **Request**: Form-data with image files.
  - **Response**: JSON message indicating success.

## Notes

- Ensure the `temp` and `output` directories exist or are created at runtime for storing temporary and output files.
- The application uses threading for parallel image processing.

## License

This project is licensed under the MIT License.

## Code Flow

1. **Application Initialization**
   - **File**: `app/main.py`
   - **Purpose**: Initializes the FastAPI application and includes the API router from `endpoints.py`.
   - **Flow**: 
     - The FastAPI app is created.
     - The API router is included, registering all endpoints defined in `endpoints.py` with the app.

2. **API Endpoints**
   - **File**: `app/api/endpoints.py`
   - **Purpose**: Defines the API endpoints for the application.
   - **Flow**:
     - A POST endpoint `/process-images/` is defined.
     - Accepts multiple image files as input.
     - Images are saved temporarily, and their paths are passed to the `process_and_save_images` function for processing.

3. **Image Processing Logic**
   - **File**: `app/services/image_processing.py`
   - **Purpose**: Contains the logic for processing and annotating images.
   - **Flow**:
     - **`process_single_image` Function**: 
       - Loads an image.
       - Runs inference using the Qwen2.5-VL model to detect and annotate objects.
       - Annotates the image with bounding boxes and labels.
       - Saves the annotated image to the output directory.
     - **`process_and_save_images` Function**:
       - Uses a thread pool to process images in parallel.
       - Calls `process_single_image` for each image path.

4. **Model Loading and Inference**
   - **File**: `app/models/model_loader.py`
   - **Purpose**: Handles loading the model and running inference.
   - **Flow**:
     - The model is loaded once using the `load_model` function.
     - **`run_qwen_2_5_vl_inference` Function**:
       - Prepares the input for the model.
       - Runs the model to get predictions.
       - Returns the response and image dimensions.

5. **Setup and Execution**
   - **Setup**: 
     - Install dependencies using `requirements.txt`.
     - Run the application using Uvicorn.
   - **Execution**:
     - The FastAPI server listens for requests.
     - When a request is made to `/process-images/`, the images are processed and annotated.

6. **Output**
   - Annotated images are saved in the `output` directory.
   - The API responds with a success message once processing is complete. 