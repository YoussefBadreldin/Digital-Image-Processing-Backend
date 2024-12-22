import cv2
import numpy as np
from flask import send_file
import os

def gray_level_slicing(file, min_val, max_val):
    # Save the uploaded file
    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    img = cv2.imread(filepath, 0)  # Read as grayscale
    output_image = np.zeros_like(img)

    output_image[(img >= min_val) & (img <= max_val)] = 255

    # Save the enhanced image with a descriptive name
    base_name = os.path.splitext(file.filename)[0]
    output_filepath = os.path.join('outputs', f'{base_name}_gray_level_sliced.jpg')
    cv2.imwrite(output_filepath, output_image)

    return send_file(output_filepath, mimetype='image/jpeg')

def histogram_equalization(file):
    # Save the uploaded file
    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    img = cv2.imread(filepath, 0)  # Read as grayscale
    equalized_image = cv2.equalizeHist(img)

    # Save the enhanced image with a descriptive name
    base_name = os.path.splitext(file.filename)[0]
    output_filepath = os.path.join('outputs', f'{base_name}_histogram_equalized.jpg')
    cv2.imwrite(output_filepath, equalized_image)

    return send_file(output_filepath, mimetype='image/jpeg')
