from flask import Flask, request, jsonify
from api.compression import jpeg_compression, webp_compression
from api.enhancement import gray_level_slicing, histogram_equalization
from api.segmentation import thresholding_segmentation, watershed_segmentation

app = Flask(__name__)

# Define the routes for your backend APIs

@app.route('/compress/jpg', methods=['POST'])
def compress_jpg():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400
    # Call your compression logic here
    compressed_image = jpeg_compression(image)
    return jsonify({"message": "JPEG compression applied!"})

@app.route('/compress/webp', methods=['POST'])
def compress_webp():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400
    # Call your compression logic here
    compressed_image = webp_compression(image)
    return jsonify({"message": "WebP compression applied!"})

@app.route('/enhance/gray_level_slicing', methods=['POST'])
def enhance_gray_level_slicing():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400
    # Call your enhancement logic here
    enhanced_image = gray_level_slicing(image)
    return jsonify({"message": "Gray-level slicing applied!"})

@app.route('/enhance/histogram_equalization', methods=['POST'])
def enhance_histogram_equalization():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400
    # Call your enhancement logic here
    enhanced_image = histogram_equalization(image)
    return jsonify({"message": "Histogram equalization applied!"})

@app.route('/segment/thresholding', methods=['POST'])
def segment_thresholding():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400
    # Call your segmentation logic here
    segmented_image = thresholding_segmentation(image)
    return jsonify({"message": "Thresholding segmentation applied!"})

@app.route('/segment/watershed', methods=['POST'])
def segment_watershed():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400
    # Call your segmentation logic here
    segmented_image = watershed_segmentation(image)
    return jsonify({"message": "Watershed segmentation applied!"})

if __name__ == '__main__':
    app.run(debug=True)
