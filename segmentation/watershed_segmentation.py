import cv2
import numpy as np
from skimage import color
from skimage.segmentation import clear_border

def watershed_segmentation(image_path):
    img = cv2.imread(image_path)
    cells = img[:, :, 0]  # Assuming the image has some features in the first channel
    
    ret1, threshold = cv2.threshold(cells, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=1)
    opening = clear_border(opening)

    sure_background = cv2.dilate(opening, kernel, iterations=1)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_foreground = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)
    
    unknown = cv2.subtract(sure_background, sure_foreground)
    _, markers = cv2.connectedComponents(np.uint8(sure_foreground))
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [0, 0, 255]  # Mark boundaries in red
    
    watershed_result_path = 'output_watershed_result.jpg'
    colored_grains_path = 'output_colored_grains.jpg'

    cv2.imwrite(watershed_result_path, img)
    img2 = color.label2rgb(markers, bg_label=0)
    cv2.imwrite(colored_grains_path, img2)

    return watershed_result_path, colored_grains_path
