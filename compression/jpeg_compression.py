from PIL import Image
import io

def compress_jpeg(image, quality=50):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return Image.open(buf)
