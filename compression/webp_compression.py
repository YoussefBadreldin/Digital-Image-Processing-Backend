from PIL import Image

def webp_compression(image_path, quality=75):
    img = Image.open(image_path)
    output_path = 'compressed_webp.webp'
    img.save(output_path, 'WEBP', quality=quality)
    return output_path
