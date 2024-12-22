from fastapi import FastAPI
from api.compression import router as compression_router
from api.enhancement import router as enhancement_router
from api.segmentation import router as segmentation_router

app = FastAPI()

app.include_router(compression_router, prefix="/api")
app.include_router(enhancement_router, prefix="/api")
app.include_router(segmentation_router, prefix="/api")
