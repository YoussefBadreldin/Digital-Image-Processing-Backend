from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/enhance', methods=['POST'])
def enhance_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    result = process(file)
    return jsonify(result)

def process(file):
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    min_val, max_val = 100, 150
    output_image = gray_level_slicing(image, min_val, max_val)
    equalized_image = cv2.equalizeHist(image)
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

if __name__ == '__main__':
    app.run(debug=True)
