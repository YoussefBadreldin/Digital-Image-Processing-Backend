import cv2
import numpy as np
import base64
from PIL import Image
import io

def process(file):
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    buffer = io.BytesIO()
    img_pil.save(buffer, format="JPEG", quality=50)
    jpeg_bytes = buffer.getvalue()
    jpeg_image = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
    _, buffer = cv2.imencode('.jpg', jpeg_image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return 'data:image/jpeg;base64,' + encoded_image
