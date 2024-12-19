import cv2
import numpy as np
import matplotlib.pyplot as plt


def gray_level_slicing(image, min_val, max_val):
    """
    Perform gray-level slicing on the input image.

    Args:
        image (ndarray): Grayscale image as a NumPy array.
        min_val (int): Minimum gray-level value to slice.
        max_val (int): Maximum gray-level value to slice.

    Returns:
        ndarray: Image with the specified gray-level range enhanced.
    """
    output_image = np.zeros_like(image)
    output_image[(image >= min_val) & (image <= max_val)] = 255
    return output_image


def enhance_image(input_path, output_dir):
    """
    Enhance the input image using gray-level slicing and histogram equalization.

    Args:
        input_path (str): Path to the input image.
        output_dir (str): Directory to save enhanced images.

    Returns:
        dict: Paths to the processed images.
    """
    # Read the input image
    image = cv2.imread(input_path, 0)

    # Gray-Level Slicing
    min_gray = 100
    max_gray = 150
    sliced_image = gray_level_slicing(image, min_gray, max_gray)
    sliced_image_path = f"{output_dir}/sliced_image.png"
    cv2.imwrite(sliced_image_path, sliced_image)

    # Histogram Equalization
    equalized_image = cv2.equalizeHist(image)
    equalized_image_path = f"{output_dir}/equalized_image.png"
    cv2.imwrite(equalized_image_path, equalized_image)

    # Visualization (Optional: can be removed in production)
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    plt.imshow(image, cmap="gray")
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.imshow(sliced_image, cmap="gray")
    plt.title("Enhanced: Gray-Level Slicing")
    plt.axis("off")

    plt.subplot(2, 2, 4)
    plt.imshow(equalized_image, cmap="gray")
    plt.title("Enhanced: Equalized Image")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    # Return paths to processed images
    return {
        "sliced_image": sliced_image_path,
        "equalized_image": equalized_image_path,
    }


# Example usage
if __name__ == "__main__":
    input_image_path = "image1.jpg"  # Update this with the correct path
    output_directory = "processed"  # Update this with the desired output directory
    processed_images = enhance_image(input_image_path, output_directory)
    print("Processed images saved at:", processed_images)
