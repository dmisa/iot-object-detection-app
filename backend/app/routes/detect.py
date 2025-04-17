from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io
from app.services.model_loader import interpreter, input_details, output_details
from app.services.label_loader import CATEGORY_INDEX
from app.utils.preprocess import preprocess_image
from app.utils.postprocess import process_detections
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

router = APIRouter()

@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        # Read the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        original_width, original_height = image.size

        # Preprocess the image
        input_data = preprocess_image(image, input_details)

        # Run inference
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Get the output
        output_data = interpreter.get_tensor(output_details[0]['index'])  # Bounding boxes
        class_data = interpreter.get_tensor(output_details[1]['index'])  # Class indices
        scores_data = interpreter.get_tensor(output_details[2]['index'])  # Confidence scores

        # Process the output
        detections = process_detections(output_data, class_data, scores_data, original_width, original_height, CATEGORY_INDEX)
        return {"detections": detections}
    except Exception as e:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )