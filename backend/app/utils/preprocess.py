import numpy as np

def preprocess_image(image, input_details):
    input_shape = input_details[0]['shape']
    image_resized = image.resize((input_shape[1], input_shape[2]))
    
    if input_details[0]['dtype'] == np.uint8:
        return np.expand_dims(np.array(image_resized, dtype=np.uint8), axis=0)
    else:
        return np.expand_dims(np.array(image_resized, dtype=np.float32) / 255.0, axis=0)