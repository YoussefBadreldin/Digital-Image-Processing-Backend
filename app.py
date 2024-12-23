from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
from segmentation import watershed_segmentation, thresholding
from compression import compress_jpeg, compress_webp
from enhancement import gray_level_slicing, histogram_equalization

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up upload and output directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/compress/jpeg', methods=['POST'])
def compress_jpeg_route():
    file = request.files.get('image')
    if not file:
        return "No file uploaded", 400
    return compress_jpeg(file)

@app.route('/compress/webp', methods=['POST'])
def compress_webp_route():
    file = request.files.get('image')
    if not file:
        return "No file uploaded", 400
    return compress_webp(file)

@app.route('/enhance/gray-slice', methods=['POST'])
def gray_level_slicing_route():
    file = request.files.get('image')
    min_val = int(request.form.get('min_val', 100))
    max_val = int(request.form.get('max_val', 150))
    if not file:
        return "No file uploaded", 400
    return gray_level_slicing(file, min_val, max_val)

@app.route('/enhance/histogram', methods=['POST'])
def histogram_equalization_route():
    file = request.files.get('image')
    if not file:
        return "No file uploaded", 400
    return histogram_equalization(file)

@app.route('/segment/global-threshold', methods=['POST'])
def global_thresholding_route():
    file = request.files.get('image')
    threshold_value = int(request.form.get('threshold', 127))  # Default threshold value
    if not file:
        return "No file uploaded", 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Read the saved file
    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    global_threshold_image_path, adaptive_threshold_image_path = thresholding(image, threshold_value, file.filename)

    # Return URLs for both thresholding results
    return jsonify({
        "global_threshold_image_url": f'/outputs/{os.path.basename(global_threshold_image_path)}',
        "adaptive_threshold_image_url": f'/outputs/{os.path.basename(adaptive_threshold_image_path)}',
    })

@app.route('/segment/watershed-segmentation', methods=['POST'])
def watershed_segmentation_route():
    file = request.files.get('image')
    if not file:
        return "No file uploaded", 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Perform watershed segmentation
    watershed_segmented_image_path = watershed_segmentation(filepath)

    # Return URL for the segmented image
    return jsonify({
        "watershed_segmented_image_url": f'/outputs/{os.path.basename(watershed_segmented_image_path)}',
    })

# Serve files from the outputs directory
@app.route('/outputs/<filename>')
def serve_output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
