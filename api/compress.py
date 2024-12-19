import cv2
import numpy as np
import os

def handler(request):
    # Get the image from the request
    image_path = request.json.get('image_path', 'image1.jpg')
    
    # Read the image
    image = cv2.imread(image_path)
    
    # Perform compression (simple quality-based JPEG compression)
    compressed_image_path = '/tmp/compressed_image.jpg'
    cv2.imwrite(compressed_image_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    
    return {
        "statusCode": 200,
        "body": f"Image compressed and saved at: {compressed_image_path}"
    }
