import cv2

def thresholding_segmentation(image_path, threshold):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    adaptive_binary_image = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    binary_path = 'output_thresholded_binary.jpg'
    adaptive_path = 'output_thresholded_adaptive.jpg'
    cv2.imwrite(binary_path, binary_image)
    cv2.imwrite(adaptive_path, adaptive_binary_image)

    return binary_path, adaptive_path
