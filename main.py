from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from uuid import uuid4
import os
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path


app = FastAPI()


UPLOAD_DIR: str = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ImageMetadata(BaseModel):
    id: str
    filename: str
    upload_date: datetime
    size: int


images_metadata: List[ImageMetadata] = []


@app.post("/upload/", status_code=201)
async def upload_image(file: UploadFile = File(...)) -> Dict[str, str]:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    image_id: str = str(uuid4())
    file_ext: str = Path(file.filename).suffix
    save_path: str = os.path.join(UPLOAD_DIR, f"{image_id}{file_ext}")

    with open(save_path, "wb") as f:
        f.write(await file.read())

    file_size: int = os.path.getsize(save_path)
    upload_date: datetime = datetime.now()

    metadata: ImageMetadata = ImageMetadata(
        id=image_id,
        filename=file.filename,
        upload_date=upload_date,
        size=file_size
    )
    images_metadata.append(metadata)

    return {"id": image_id}


@app.get("/images/", response_model=List[ImageMetadata])
def list_images(limit: int = 10, offset: int = 0) -> List[ImageMetadata]:
    return images_metadata[offset:offset + limit]


@app.get("/images/{image_id}")
def get_image(image_id: str) -> FileResponse:
    metadata: ImageMetadata = next((img for img in images_metadata if img.id == image_id), None)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Image not found")

    file_ext: str = Path(metadata.filename).suffix
    file_path: str = os.path.join(UPLOAD_DIR, f"{image_id}{file_ext}")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(file_path)
