from PIL import Image

def jpeg_compression(image_path, quality=50):
    img = Image.open(image_path)
    output_path = 'compressed_jpeg.jpg'
    img.save(output_path, 'JPEG', quality=quality)
    return output_path
