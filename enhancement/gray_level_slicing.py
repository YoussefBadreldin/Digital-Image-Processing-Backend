import cv2
import numpy as np

def gray_level_slicing(image_path, min_val, max_val):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    output_image = np.zeros_like(image)
    output_image[(image >= min_val) & (image <= max_val)] = 255
    result_path = 'output_gray_level_slicing.jpg'
    cv2.imwrite(result_path, output_image)
    return result_path
