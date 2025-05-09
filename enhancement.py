<!-- enhancement.py -->
import cv2
import numpy as np
from flask import jsonify
import os
import base64

def gray_level_slicing(file, min_val, max_val):
    try:
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        img = cv2.imread(filepath, 0)  # Read as grayscale
        if img is None:
            return jsonify({"error": "Failed to read image"}), 400

        output_image = np.copy(img)  # Copy original image

        # Set pixels in the range [min_val, max_val] to 255
        output_image[(img >= min_val) & (img <= max_val)] = 255

        # Save the enhanced image
        base_name = os.path.splitext(file.filename)[0]
        output_filepath = os.path.join('outputs', f'{base_name}_gray_level_sliced.jpg')
        cv2.imwrite(output_filepath, output_image)

        # Read the processed image and convert to base64
        with open(output_filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "image": img_data,
            "filename": os.path.basename(output_filepath)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def histogram_equalization(file):
    try:
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        img = cv2.imread(filepath, 0)  # Read as grayscale
        if img is None:
            return jsonify({"error": "Failed to read image"}), 400

        equalized_image = cv2.equalizeHist(img)

        # Save the enhanced image
        base_name = os.path.splitext(file.filename)[0]
        output_filepath = os.path.join('outputs', f'{base_name}_histogram_equalized.jpg')
        cv2.imwrite(output_filepath, equalized_image)

        # Read the processed image and convert to base64
        with open(output_filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "image": img_data,
            "filename": os.path.basename(output_filepath)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def power_law_transformation(file, gamma=1.0):
    try:
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        # Read the image
        img = cv2.imread(filepath, 0)  # Read as grayscale
        if img is None:
            return jsonify({"error": "Failed to read image"}), 400
        
        # Apply power law transformation
        normalized = img / 255.0
        transformed = np.power(normalized, gamma)
        output_image = (transformed * 255).astype(np.uint8)

        # Save the enhanced image
        base_name = os.path.splitext(file.filename)[0]
        output_filepath = os.path.join('outputs', f'{base_name}_power_law.jpg')
        cv2.imwrite(output_filepath, output_image)

        # Read the processed image and convert to base64
        with open(output_filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "image": img_data,
            "filename": os.path.basename(output_filepath)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def negative_transformation(file):
    try:
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        # Read the image
        img = cv2.imread(filepath, 0)  # Read as grayscale
        if img is None:
            return jsonify({"error": "Failed to read image"}), 400
        
        # Apply negative transformation
        output_image = 255 - img

        # Save the enhanced image
        base_name = os.path.splitext(file.filename)[0]
        output_filepath = os.path.join('outputs', f'{base_name}_negative.jpg')
        cv2.imwrite(output_filepath, output_image)

        # Read the processed image and convert to base64
        with open(output_filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "image": img_data,
            "filename": os.path.basename(output_filepath)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500 