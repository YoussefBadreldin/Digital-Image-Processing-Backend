from flask import Flask, request, jsonify
from compression.jpeg_compression import jpeg_compression
from compression.webp_compression import webp_compression

app = Flask(__name__)

@app.route('/compress/jpg', methods=['POST'])
def compress_jpeg():
    file = request.files['image']
    quality = int(request.form.get('quality', 50))  # Default to 50% quality if not provided
    file.save("input_image.jpg")
    output_path = jpeg_compression("input_image.jpg", quality)
    return jsonify({"compressed_image_path": output_path})

@app.route('/compress/webp', methods=['POST'])
def compress_webp():
    file = request.files['image']
    quality = int(request.form.get('quality', 75))  # Default to 75% quality if not provided
    file.save("input_image.jpg")
    output_path = webp_compression("input_image.jpg", quality)
    return jsonify({"compressed_image_path": output_path})

if __name__ == "__main__":
    app.run(debug=True)
