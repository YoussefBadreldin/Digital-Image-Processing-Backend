from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
from segmentation.watershed_segmentation import watershed_segmentation

router = APIRouter()

@router.post("/segment")
async def segment(file: UploadFile = File(...), type1: bool = False, type2: bool = False):
    image = Image.open(io.BytesIO(await file.read()))
    image_path = "uploaded_image.jpg"
    image.save(image_path)
    results = []
    if type1:
        watershed_result, _ = watershed_segmentation(image_path)
        results.append(watershed_result)
    if type2:
        _, img2 = watershed_segmentation(image_path)
        results.append(img2)
    
    response_data = {"segmented_images": []}
    for result in results:
        buf = io.BytesIO()
        result.save(buf, format="JPEG")
        response_data["segmented_images"].append(f"data:image/jpeg;base64,{buf.getvalue().hex()}")
    
    return JSONResponse(content=response_data)
