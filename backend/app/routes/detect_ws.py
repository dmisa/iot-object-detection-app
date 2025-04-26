from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from PIL import Image, UnidentifiedImageError
import io
import base64
import asyncio

from app.services.model_loader import interpreter, input_details, output_details
from app.services.label_loader import CATEGORY_INDEX
from app.utils.preprocess import preprocess_image
from app.utils.postprocess import process_detections

router = APIRouter()
interpreter_lock = asyncio.Lock()

@router.websocket("/ws/detect")
async def websocket_detect(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()

            # Input validation: ensure it's long enough to resemble Base64-encoded image
            if not data or len(data) < 100:
                await websocket.send_json({"error": "Invalid or too short image data"})
                continue

            try:
                # Decode the Base64 string safely
                image_data = base64.b64decode(data)
                image = Image.open(io.BytesIO(image_data)).convert("RGB")
                original_width, original_height = image.size
            except (base64.binascii.Error, UnidentifiedImageError) as decode_error:
                await websocket.send_json({"error": f"Failed to decode or open image: {str(decode_error)}"})
                continue

            # Preprocess the image
            input_data = preprocess_image(image, input_details)

            # Ensure only one inference at a time
            async with interpreter_lock:
                interpreter.set_tensor(input_details[0]['index'], input_data)
                interpreter.invoke()
                output_data = interpreter.get_tensor(output_details[0]['index'])  # Bounding boxes
                class_data = interpreter.get_tensor(output_details[1]['index'])  # Class indices
                scores_data = interpreter.get_tensor(output_details[2]['index'])  # Confidence scores

            # Process the output
            detections = process_detections(
                output_data, class_data, scores_data,
                original_width, original_height, CATEGORY_INDEX
            )

            # Send detections back to client
            await websocket.send_json({"detections": detections})

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        await websocket.send_json({"error": f"Unexpected error: {str(e)}"})
