import os
from flask import Flask, request, jsonify
from PIL import Image
import cv2

app = Flask(__name__)

# Route for image compression
@app.route('/api/compress', methods=['POST'])
def compress_image():
    file = request.files['image']
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        # Open the image using PIL
        img = Image.open(file_path)
        
        # Save compressed JPEG and WebP images
        compressed_jpeg_path = os.path.join('public', 'compressed_jpeg.jpg')
        img.save(compressed_jpeg_path, 'JPEG', quality=50)

        compressed_webp_path = os.path.join('public', 'compressed_webp.webp')
        img.save(compressed_webp_path, 'WebP', quality=75)

        return jsonify({
            'jpeg_image_url': '/compressed_jpeg.jpg',
            'webp_image_url': '/compressed_webp.webp'
        })
    return jsonify({'error': 'No image provided'}), 400


if __name__ == '__main__':
    app.run()
