import os
from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
from matplotlib import pyplot as plt

app = Flask(__name__)

# Route for image enhancement
@app.route('/api/enhance', methods=['POST'])
def enhance_image():
    file = request.files['image']
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        # Load image
        image = cv2.imread(file_path, 0)

        # Perform enhancement (Gray-Level Slicing)
        min_gray = 100
        max_gray = 150
        output_image = np.zeros_like(image)
        output_image[(image >= min_gray) & (image <= max_gray)] = 255

        # Equalize histogram
        equalized_image = cv2.equalizeHist(image)

        # Save enhanced image
        enhanced_image_path = os.path.join('public', 'enhanced_image.jpg')
        cv2.imwrite(enhanced_image_path, equalized_image)

        return jsonify({'image_url': '/enhanced_image.jpg'})
    return jsonify({'error': 'No image provided'}), 400


if __name__ == '__main__':
    app.run()
