#!/usr/bin/env python
# coding: utf-8

# In[53]:


import cv2
from matplotlib import pyplot as plt

def thresholding(image, threshold):
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    
    adaptive_binary_image = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    plt.figure(figsize=(15, 10))

    plt.subplot(1, 3, 1)
    plt.title('Original Image')
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.title('Global Thresholded Image')
    plt.imshow(binary_image, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('Adaptive Thresholded Image')
    plt.imshow(adaptive_binary_image, cmap='gray')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return binary_image, adaptive_binary_image

image = cv2.imread("ma.jpg", cv2.IMREAD_GRAYSCALE)
binary_image, adaptive_binary_image = thresholding(image, 127)



# In[52]:


def watershed_segmentation(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read image.")
        return

    cells = img[:, :, 0] 
    plt.figure(figsize=(15, 12))

    plt.subplot(4, 3, 1)
    plt.imshow(cells, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
 
    ret1, threshold = cv2.threshold(cells, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.subplot(4, 3, 2)
    plt.imshow(threshold, cmap='gray')
    plt.title('Thresholded Image')
    plt.axis('off')


    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=1)
    opening = clear_border(opening)  # Remove objects touching border
    plt.subplot(4, 3, 3)
    plt.imshow(opening, cmap='gray')
    plt.title('After Morphological Opening')
    plt.axis('off')

  
    sure_background = cv2.dilate(opening, kernel, iterations=1)
    plt.subplot(4, 3, 4)
    plt.imshow(sure_background, cmap='gray')
    plt.title('Sure Background')
    plt.axis('off')

    # DT
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    plt.subplot(4, 3, 5)
    plt.imshow(dist_transform, cmap='gray')
    plt.title('Distance Transform')
    plt.axis('off')

    _, sure_foreground = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)
    sure_foreground = np.uint8(sure_foreground)
    plt.subplot(4, 3, 6)
    plt.imshow(sure_foreground, cmap='gray')
    plt.title('Sure Foreground')
    plt.axis('off')

    unknown = cv2.subtract(sure_background, sure_foreground)
    plt.subplot(4, 3, 7)
    plt.imshow(unknown, cmap='gray')
    plt.title('Unknown Region')
    plt.axis('off')

    _, markers = cv2.connectedComponents(sure_foreground)
    markers = markers + 1
    markers[unknown == 255] = 0
    plt.subplot(4, 3, 8)
    plt.imshow(markers, cmap='gray')
    plt.title('Markers')
    plt.axis('off')

    markers = cv2.watershed(img, markers)
    watershed_result = img.copy()
    watershed_result[markers == -1] = [0, 0, 255]  
    plt.subplot(4, 3, 9)
    plt.imshow(cv2.cvtColor(watershed_result, cv2.COLOR_BGR2RGB))
    plt.title('Segmented Image with Boundaries')
    plt.axis('off')

    plt.subplot(4, 3, 10)
    plt.title('Overlay on Original Image')
    plt.imshow(cv2.cvtColor(watershed_result, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    img2 = color.label2rgb(markers, bg_label=0)
    plt.subplot(4, 3, 11)
    plt.title('Colored Grains')
    plt.imshow(img2)
    plt.axis('off')
    
    
    plt.tight_layout()
    plt.show()
    return watershed_result,img2
#image_path = "ma.jpg"
watershed_result,img2=watershed_segmentation("ma.jpg")

plt.figure(figsize=(15, 10))
    

plt.subplot(1, 2, 1)
plt.title('watershed_result')
plt.imshow(watershed_result, cmap='gray')
plt.axis('off')
    
plt.subplot(1, 2, 2)
plt.title('Colored Grains')
plt.imshow(img2, cmap='gray')
plt.axis('off')


# In[ ]:





# In[ ]:




