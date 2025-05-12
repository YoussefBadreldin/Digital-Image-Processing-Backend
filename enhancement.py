import os
import cv2
import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive 'Agg'
import matplotlib.pyplot as plt
import base64
import numpy as np
from flask import jsonify
from datetime import datetime

def load_image(file, filepath):
    """Helper function to load and convert image to grayscale if needed"""
    # Read image
    img = cv2.imread(filepath)
    if img is None:
        return None, "Failed to read image"
    
    # Convert to grayscale if RGB
    if len(img.shape) == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = img
    
    return gray_img, None

def get_unique_filename(original_filename, operation):
    """Generate unique filename using timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(original_filename)[0]
    return f"{base_name}_{operation}_{timestamp}"

def histogram_equalization(file):
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(file.filename)[0]
        unique_id = f"{base_name}_hist_eq_{timestamp}"
        
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        # Load and convert image
        img, error = load_image(file, filepath)
        if error:
            return jsonify({"error": error}), 400

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
        hist_original_path = os.path.join('outputs', f'{unique_id}_histogram_original.png')
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
        hist_equalized_path = os.path.join('outputs', f'{unique_id}_histogram_equalized.png')
        plt.savefig(hist_equalized_path)
        plt.close()

        # Save the enhanced image
        output_filepath = os.path.join('outputs', f'{unique_id}.jpg')
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

def gray_level_slicing(file, min_val=0, max_val=255):
    try:
        # Generate unique filename
        unique_id = get_unique_filename(file.filename, "gray_slice")
        
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        # Load and convert image
        img, error = load_image(file, filepath)
        if error:
            return jsonify({"error": error}), 400

        # Apply gray level slicing
        output_image = np.copy(img)
        output_image[(img >= min_val) & (img <= max_val)] = 255

        # Save the enhanced image
        output_filepath = os.path.join('outputs', f'{unique_id}.jpg')
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

def power_law_transformation(file, gamma=0.5):
    try:
        # Generate unique filename
        unique_id = get_unique_filename(file.filename, "power_law")
        
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        # Load and convert image
        img, error = load_image(file, filepath)
        if error:
            return jsonify({"error": error}), 400
        
        # Apply power law transformation
        # Convert to float32 to avoid overflow
        img_float = img.astype(np.float32)
        # Normalize to [0,1]
        normalized = img_float / 255.0
        # Apply gamma correction (using gamma directly, not 1/gamma)
        transformed = np.power(normalized, gamma)
        # Scale back to [0,255] and convert to uint8
        output_image = np.clip(transformed * 255.0, 0, 255).astype(np.uint8)

        # Save the enhanced image
        output_filepath = os.path.join('outputs', f'{unique_id}.jpg')
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
        # Generate unique filename
        unique_id = get_unique_filename(file.filename, "negative")
        
        # Save the uploaded file
        filepath = os.path.join('Uploads', file.filename)
        file.save(filepath)

        # Load and convert image
        img, error = load_image(file, filepath)
        if error:
            return jsonify({"error": error}), 400

        # Invert the image (simple negative)
        output_image = 255 - img

        # Save the enhanced image as PNG to avoid compression artifacts
        output_filepath = os.path.join('outputs', f'{unique_id}.png')
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