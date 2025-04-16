from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from PIL import Image
import io
import base64
from app.services.model_loader import interpreter, input_details, output_details
from app.services.label_loader import CATEGORY_INDEX
from app.utils.preprocess import preprocess_image
from app.utils.postprocess import process_detections

router = APIRouter()

@router.websocket("/ws/detect")
async def websocket_detect(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive a Base64-encoded image from the client
            data = await websocket.receive_text()
            image_data = base64.b64decode(data)  # Decode the Base64 string
            image = Image.open(io.BytesIO(image_data)).convert("RGB")  # Convert to PIL Image
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

            # Send the detections back to the client
            await websocket.send_json({"detections": detections})
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})