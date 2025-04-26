import os
import logging
from tflite_runtime.interpreter import Interpreter  # Correct import for tflite_runtime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_tflite_model(model_path: str):
    """Loads a TensorFlow Lite model and returns interpreter and tensor details."""
    if not os.path.exists(model_path):
        logger.error(f"❌ Model file not found: {model_path}")
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        logger.info(f"📦 Loading model from: {model_path}")
        interpreter = Interpreter(model_path=model_path)  # Use the correct Interpreter class
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        logger.info("✅ Model loaded and tensors allocated successfully.")
        return interpreter, input_details, output_details
    except Exception as e:
        logger.exception("💥 Failed to load and initialize the TFLite model.")
        raise RuntimeError(f"Failed to load TFLite model: {str(e)}")

MODEL_PATH = os.getenv("MODEL_PATH")
interpreter, input_details, output_details = load_tflite_model(MODEL_PATH)