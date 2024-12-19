import cv2
import matplotlib.pyplot as plt
from PIL import Image

def compress_image(input_path, output_dir):
    """
    Compress the input image using JPEG and WebP formats.

    Args:
        input_path (str): Path to the input image.
        output_dir (str): Directory to save compressed images.

    Returns:
        dict: Paths to the compressed images.
    """
    # --- Image Reading ---
    img = cv2.imread(input_path)  # Read input image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for display

    # --- Image Compression (JPEG) ---
    img_pil = Image.fromarray(img_rgb)  # Convert NumPy array to PIL image
    jpeg_path = f"{output_dir}/compressed_jpeg.jpg"
    img_pil.save(jpeg_path, quality=50)  # Save as JPEG with specified quality
    img_jpeg = cv2.imread(jpeg_path)
    img_jpeg_rgb = cv2.cvtColor(img_jpeg, cv2.COLOR_BGR2RGB)

    # --- Image Compression (WebP) ---
    webp_path = f"{output_dir}/compressed_webp.webp"
    img_pil.save(webp_path, format="WebP", quality=75)  # Save as WebP with specified quality
    img_webp = cv2.imread(webp_path)
    img_webp_rgb = cv2.cvtColor(img_webp, cv2.COLOR_BGR2RGB)

    # --- Display Images (Optional: Can be removed in production) ---
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(img_rgb)
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("JPEG Compressed")
    plt.imshow(img_jpeg_rgb)
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("WebP Compressed")
    plt.imshow(img_webp_rgb)
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    # Return paths to compressed images
    return {
        "jpeg": jpeg_path,
        "webp": webp_path,
    }


# Example usage
if __name__ == "__main__":
    input_image_path = "lossy_image.jpg"  # Update with the correct image path
    output_directory = "processed"  # Update with your desired output directory
    compressed_images = compress_image(input_image_path, output_directory)
    print("Compressed images saved at:", compressed_images)
