import cv2

def histogram_equalization(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    equalized_image = cv2.equalizeHist(image)
    result_path = 'output_histogram_equalized.jpg'
    cv2.imwrite(result_path, equalized_image)
    return result_path
