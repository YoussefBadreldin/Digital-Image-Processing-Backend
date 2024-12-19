import cv2
import numpy as np
import base64

def process(file):
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    
    # Gray-Level Slicing
    min_val, max_val = 100, 150
    output_image = gray_level_slicing(image, min_val, max_val)
    
    # Histogram Equalization
    equalized_image = cv2.equalizeHist(image)
    
    # Encode images to base64
    encoded_output_image = encode_image(output_image)
    encoded_equalized_image = encode_image(equalized_image)
    
    return {
        'gray_level_sliced': 'data:image/png;base64,' + encoded_output_image,
        'equalized': 'data:image/png;base64,' + encoded_equalized_image
    }

def gray_level_slicing(image, min_val, max_val):
    output_image = np.zeros_like(image)
    output_image[(image >= min_val) & (image <= max_val)] = 255
    return output_image

def encode_image(image):
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')
