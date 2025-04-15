import tensorflow as tf

# Path to your saved_model folder (the one containing saved_model.pb and variables/)
saved_model_dir = "models"

# Path to output .tflite file
tflite_model_path = "models/detect_2.tflite"

# Create converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Optional: enable optimizations

# Convert the model
tflite_model = converter.convert()

# Save to file
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)

print(f"✅ TFLite model saved to {tflite_model_path}")
