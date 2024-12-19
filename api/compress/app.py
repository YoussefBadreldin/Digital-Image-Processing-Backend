from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/compress', methods=['POST'])
def compress_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    result = process(file)
    return jsonify({'result': result})

def process(file):
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    buffer = io.BytesIO()
    img_pil.save(buffer, format="JPEG", quality=50)
    jpeg_bytes = buffer.getvalue()
    jpeg_image = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
    _, buffer = cv2.imencode('.jpg', jpeg_image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return 'data:image/jpeg;base64,' + encoded_image

if __name__ == '__main__':
    app.run(debug=True)
