import os
import cv2
import matplotlib.pyplot as plt
import base64
import numpy as np
from flask import jsonify

def histogram_equalization(file):
    try:
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        img = cv2.imread(filepath, 0)  # Read as grayscale
        if img is None:
            return jsonify({"error": "Failed to read image"}), 400

        # Calculate original histogram
        hist_original = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_original = hist_original.flatten() / hist_original.sum()
        
        # Create histogram plot for original image
        plt.figure(figsize=(8, 4))
        plt.plot(hist_original)
        plt.title('Original Image Histogram')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Normalized Frequency')
        plt.grid(True)
        
        # Save original histogram
        base_name = os.path.splitext(file.filename)[0]
        hist_original_path = os.path.join('outputs', f'{base_name}_histogram_original.png')
        plt.savefig(hist_original_path)
        plt.close()

        # Apply histogram equalization
        equalized_image = cv2.equalizeHist(img)

        # Calculate equalized histogram
        hist_equalized = cv2.calcHist([equalized_image], [0], None, [256], [0, 256])
        hist_equalized = hist_equalized.flatten() / hist_equalized.sum()
        
        # Create histogram plot for equalized image
        plt.figure(figsize=(8, 4))
        plt.plot(hist_equalized)
        plt.title('Equalized Image Histogram')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Normalized Frequency')
        plt.grid(True)
        
        # Save equalized histogram
        hist_equalized_path = os.path.join('outputs', f'{base_name}_histogram_equalized.png')
        plt.savefig(hist_equalized_path)
        plt.close()

        # Save the enhanced image
        output_filepath = os.path.join('outputs', f'{base_name}_histogram_equalized.jpg')
        cv2.imwrite(output_filepath, equalized_image)

        # Read all images and convert to base64
        with open(output_filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        with open(hist_original_path, 'rb') as hist_file:
            hist_original_data = base64.b64encode(hist_file.read()).decode('utf-8')
        with open(hist_equalized_path, 'rb') as hist_file:
            hist_equalized_data = base64.b64encode(hist_file.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "image": img_data,
            "histogram_original": hist_original_data,
            "histogram_equalized": hist_equalized_data,
            "filename": os.path.basename(output_filepath)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def gray_level_slicing(file, min_val, max_val):
    try:
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        img = cv2.imread(filepath, 0)  # Read as grayscale
        if img is None:
            return jsonify({"error": "Failed to read image"}), 400

        output_image = np.copy(img)  # Copy original image
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

        # Read the image as grayscale
        img = cv2.imread(filepath, 0)
        if img is None:
            return jsonify({"error": "Failed to read image"}), 400

        # Invert the image (simple negative)
        output_image = 255 - img

        # Save the enhanced image as PNG to avoid compression artifacts
        base_name = os.path.splitext(file.filename)[0]
        output_filepath = os.path.join('outputs', f'{base_name}_negative.png')
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