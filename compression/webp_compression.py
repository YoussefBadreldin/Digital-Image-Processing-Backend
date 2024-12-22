from PIL import Image
import io

def compress_webp(image, quality=75):
    buf = io.BytesIO()
    image.save(buf, format="WEBP", quality=quality)
    buf.seek(0)
    return Image.open(buf)
