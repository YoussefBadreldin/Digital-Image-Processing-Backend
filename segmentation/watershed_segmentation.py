import cv2
import numpy as np
from skimage.segmentation import clear_border
from skimage import color
from PIL import Image

def watershed_segmentation(image_path):
    img = cv2.imread(image_path)
    cells = img[:, :, 0]
    ret1, threshold = cv2.threshold(cells, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=1)
    opening = clear_border(opening)
    sure_background = cv2.dilate(opening, kernel, iterations=1)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_foreground = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)
    sure_foreground = np.uint8(sure_foreground)
    unknown = cv2.subtract(sure_background, sure_foreground)
    _, markers = cv2.connectedComponents(sure_foreground)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    watershed_result = img.copy()
    watershed_result[markers == -1] = [0, 0, 255]
    img2 = color.label2rgb(markers, bg_label=0)
    return Image.fromarray(watershed_result), Image.fromarray(img2)
