from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
from enhancement.gray_level_slicing import gray_level_slicing
from enhancement.histogram_equalization import equalize_hist
from segmentation.thresholding_segmentation import thresholding

router = APIRouter()

@router.post("/enhance")
async def enhance(file: UploadFile = File(...), type1: bool = False, type2: bool = False, type3: bool = False, type4: bool = False):
    image = Image.open(io.BytesIO(await file.read())).convert("L")
    image = np.array(image)
    results = []
    if type1:
        binary_image, _ = thresholding(image, 127)
        results.append(Image.fromarray(binary_image))
    if type2:
        _, adaptive_binary_image = thresholding(image, 127)
        results.append(Image.fromarray(adaptive_binary_image))
    if type3:
        output_image = gray_level_slicing(image, 100, 150)
        results.append(Image.fromarray(output_image))
    if type4:
        equalized_image = equalize_hist(image)
        results.append(Image.fromarray(equalized_image))
    
    response_data = {"enhanced_images": []}
    for result in results:
        buf = io.BytesIO()
        result.save(buf, format="JPEG")
        response_data["enhanced_images"].append(f"data:image/jpeg;base64,{buf.getvalue().hex()}")
    
    return JSONResponse(content=response_data)
