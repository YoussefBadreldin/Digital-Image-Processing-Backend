import cv2
import numpy as np
from matplotlib import pyplot as plt

def handler(request):
    # Read the image from request body (this could be a file upload)
    image_path = request.json.get('image_path', 'image1.jpg')
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Perform some image enhancement (e.g., equalize histogram)
    enhanced_image = cv2.equalizeHist(image)
    
    # Save the enhanced image to send back as a response
    output_path = '/tmp/enhanced_image.jpg'
    cv2.imwrite(output_path, enhanced_image)
    
    return {
        "statusCode": 200,
        "body": "Enhanced image saved at: " + output_path
    }
