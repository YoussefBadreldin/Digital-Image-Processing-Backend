import cv2
import numpy as np
import os
from flask import send_file

def thresholding(image, threshold, file_name):
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    adaptive_binary_image = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Save the results with descriptive names
    base_name = os.path.splitext(file_name)[0]
    binary_image_path = os.path.join('outputs', f'{base_name}_global_thresholding.png')
    adaptive_binary_image_path = os.path.join('outputs', f'{base_name}_adaptive_thresholding.png')
    cv2.imwrite(binary_image_path, binary_image)
    cv2.imwrite(adaptive_binary_image_path, adaptive_binary_image)

    return binary_image_path, adaptive_binary_image_path


def watershed_segmentation(image_path):
    img = cv2.imread(image_path)
    original_img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binary thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # sure background
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # sure foreground
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # unknown region
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # watershed
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [0, 0, 255]  # Mark boundaries in red

    # Save the result with a descriptive name
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    segmented_image_path = os.path.join('outputs', f'{base_name}_watershed_segmented.png')
    cv2.imwrite(segmented_image_path, img)

    return segmented_image_path
