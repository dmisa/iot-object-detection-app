import tensorflow as tf
import os

def verify_paths():
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.abspath(os.path.join(current_dir, "..", "models"))
    output_path = os.path.abspath(os.path.join(current_dir, "..", "models", "model.tflite"))
    
    print("\nChecking paths:")
    print(f"Model directory: {model_dir}")
    print(f"Output path: {output_path}")
    
    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"Model directory not found at: {model_dir}")
        
    return model_dir, output_path

try:
    model_dir, output_path = verify_paths()
    print("\nStarting model conversion...")

    # Convert the model
    converter = tf.lite.TFLiteConverter.from_saved_model(model_dir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float32]

    tflite_model = converter.convert()

    # Save the model
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(tflite_model)
    print(f"\nModel successfully converted and saved to: {output_path}")

except Exception as e:
    print(f"\nError: {str(e)}")