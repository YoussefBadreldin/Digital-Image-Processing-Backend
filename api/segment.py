import os
from flask import Flask, request, jsonify
import cv2
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt

app = Flask(__name__)

# Route for image segmentation
@app.route('/api/segment', methods=['POST'])
def segment_image():
    file = request.files['image']
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        # Load image and convert to grayscale
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Thresholding for segmentation
        _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        # Apply watershed (for this example, we use simple thresholding)
        ret, markers = cv2.connectedComponents(binary_image)
        markers = markers + 1
        markers[binary_image == 255] = 0

        # Create segmented image
        segmented_image = image.copy()
        segmented_image[markers == -1] = 255  # Watershed boundaries

        segmented_image_path = os.path.join('public', 'segmented_image.jpg')
        cv2.imwrite(segmented_image_path, segmented_image)

        return jsonify({'image_url': '/segmented_image.jpg'})
    return jsonify({'error': 'No image provided'}), 400


if __name__ == '__main__':
    app.run()
