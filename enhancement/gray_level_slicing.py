import numpy as np

def gray_level_slicing(image, min_val, max_val):
    output_image = np.zeros_like(image)
    output_image[(image >= min_val) & (image <= max_val)] = 255
    return output_image
