import cv2
import numpy as np
from skimage import color
from skimage.segmentation import watershed
from skimage.filters import sobel

def handler(request):
    # Get the image path from the request
    image_path = request.json.get('image_path', 'image1.jpg')
    
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale and perform watershed segmentation
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gradient = sobel(grayscale_image)
    
    markers = np.zeros_like(grayscale_image)
    markers[grayscale_image < 50] = 1
    markers[grayscale_image > 200] = 2
    
    segmented_image = watershed(gradient, markers)
    
    # Save the segmented image
    segmented_image_path = '/tmp/segmented_image.jpg'
    cv2.imwrite(segmented_image_path, segmented_image)
    
    return {
        "statusCode": 200,
        "body": f"Segmented image saved at: {segmented_image_path}"
    }
