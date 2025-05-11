from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response
import os
import shutil

router = APIRouter()

MEDIA_DIR = "media"

@router.post("/upload-video/", response_model=dict)
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(MEDIA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "path": file_path}

@router.get("/media/{filename}")
async def get_video(filename: str):
    file_path = os.path.join(MEDIA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    with open(file_path, "rb") as video_file:
        return Response(content=video_file.read(), media_type="video/mp4")