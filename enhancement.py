#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt


# In[5]:





# In[12]:


import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image in grayscale mode
image = cv2.imread('image1.jpg', 0)

# Define the gray-level slicing function
def gray_level_slicing(image, min_val, max_val):
    output_image = np.zeros_like(image)
    output_image[(image >= min_val) & (image <= max_val)] = 255  # Apply slicing
    return output_image

# Define the range for gray-level slicing
min_gray = 100  
max_gray = 150  

# Perform gray-level slicing
output_image = gray_level_slicing(image, min_gray, max_gray)

# Display the original and processed images side by side
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(output_image, cmap='gray')
plt.title('Enhanced: Gray-Level Slicing')
plt.axis('off')

plt.show()


# In[11]:


image = cv2.imread('image1.jpg', 0)

equalized_image = cv2.equalizeHist(image)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(equalized_image, cmap='gray')
plt.title('Enhanced: Equalized Image')
plt.axis('off')

plt.show()


# In[ ]:




