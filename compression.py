import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# --- Image Reading ---
img = cv2.imread('lossy_image.jpg')  # Replace with the actual image path
if img is None:
    raise FileNotFoundError("Image 'lossy_image.jpg' not found. Please ensure the file exists.")

# Convert from BGR to RGB for display
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# --- Image Compression (JPEG) ---
img_pil = Image.fromarray(img_rgb)
img_pil.save('compressed_jpeg.jpg', quality=50)  # Adjust quality (0-100) as needed

# Read the compressed JPEG image
img_jpeg = cv2.imread('compressed_jpeg.jpg')
if img_jpeg is None:
    raise FileNotFoundError("Compressed JPEG image 'compressed_jpeg.jpg' could not be created.")
img_jpeg_rgb = cv2.cvtColor(img_jpeg, cv2.COLOR_BGR2RGB)

# --- Image Compression (WebP) ---
img_pil.save('compressed_webp.webp', format='WebP', quality=75)  # Adjust quality (0-100) as needed

# Read the compressed WebP image
img_webp = cv2.imread('compressed_webp.webp')
if img_webp is None:
    raise FileNotFoundError("Compressed WebP image 'compressed_webp.webp' could not be created.")
img_webp_rgb = cv2.cvtColor(img_webp, cv2.COLOR_BGR2RGB)

# --- Display Images ---
plt.figure(figsize=(15, 5))

# Original Image
plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(img_rgb)
plt.axis('off')

# JPEG Compressed
plt.subplot(1, 3, 2)
plt.title('JPEG Compressed')
plt.imshow(img_jpeg_rgb)
plt.axis('off')

# WebP Compressed
plt.subplot(1, 3, 3)
plt.title('WebP Compressed')
plt.imshow(img_webp_rgb)
plt.axis('off')

plt.tight_layout()
plt.show()
