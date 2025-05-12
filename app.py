from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from enhancement import gray_level_slicing, histogram_equalization, power_law_transformation, negative_transformation

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up upload and output directories
UPLOAD_FOLDER = 'Uploads'
OUTPUT_FOLDER = 'outputs'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/')
def index():
    return jsonify({"status": "API is running"})

@app.route('/enhance/gray_level_slicing', methods=['POST'])
def gray_level_slicing_route():
    file = request.files.get('image')
    min_val = int(request.form.get('min_val', 100))
    max_val = int(request.form.get('max_val', 150))
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    return gray_level_slicing(file, min_val, max_val)

@app.route('/enhance/histogram_equalization', methods=['POST'])
def histogram_equalization_route():
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    return histogram_equalization(file)

@app.route('/enhance/power_law', methods=['POST'])
def power_law_route():
    file = request.files.get('image')
    gamma = float(request.form.get('gamma', 0.5))  # Default gamma value changed to 0.5
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    return power_law_transformation(file, gamma)

@app.route('/enhance/negative', methods=['POST'])
def negative_route():
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    return negative_transformation(file)

@app.route('/outputs/<filename>')
def serve_output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# For local development
if __name__ == '__main__':
    app.run(debug=True)