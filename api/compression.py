from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
from compression.jpeg_compression import compress_jpeg
from compression.webp_compression import compress_webp

router = APIRouter()

@router.post("/compress")
async def compress(file: UploadFile = File(...), type1: bool = False, type2: bool = False):
    image = Image.open(io.BytesIO(await file.read()))
    results = []
    if type1:
        compressed_image = compress_jpeg(image, quality=50)
        results.append(compressed_image)
    if type2:
        compressed_image = compress_webp(image, quality=75)
        results.append(compressed_image)
    
    response_data = {"compressed_images": []}
    for result in results:
        buf = io.BytesIO()
        result.save(buf, format="JPEG")
        response_data["compressed_images"].append(f"data:image/jpeg;base64,{buf.getvalue().hex()}")
    
    return JSONResponse(content=response_data)
