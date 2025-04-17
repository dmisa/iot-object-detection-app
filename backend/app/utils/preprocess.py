import numpy as np

def preprocess_image(image, input_details):
    """
    Preprocess the input image based on model input requirements.

    Parameters:
        image (PIL.Image): The input image to preprocess.
        input_details (list): Model input details containing 'shape' and 'dtype'.

    Returns:
        np.ndarray: The preprocessed image in the correct shape and dtype.
    """
    try:
        input_shape = input_details[0]['shape']
        image_resized = image.resize((input_shape[1], input_shape[2]))
        
        # Ensure image data type is handled correctly
        if input_details[0]['dtype'] == np.uint8:
            return np.expand_dims(np.array(image_resized, dtype=np.uint8), axis=0)
        elif input_details[0]['dtype'] == np.float32:
            return np.expand_dims(np.array(image_resized, dtype=np.float32) / 255.0, axis=0)
        else:
            raise ValueError("Unsupported dtype in input details")
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")