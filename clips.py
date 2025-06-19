from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_active_user
from fastapi.responses import FileResponse
import shutil
from datetime import datetime

router = APIRouter()

MEDIA_DIR = "media"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

@router.post("/", response_model=schemas.Clip)
def create_clip(
    anime_id: int,
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_active_user)
):
    # Check if anime exists
    anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(MEDIA_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create clip record
    clip_data = {
        "title": title,
        "filename": filename,
        "anime_id": anime_id,
        "preview_url": f"/static/{filename}"  # In a real app, you'd generate a thumbnail
    }
    
    db_clip = models.Clip(**clip_data)
    db.add(db_clip)
    db.commit()
    db.refresh(db_clip)
    
    return db_clip

@router.get("/", response_model=List[schemas.Clip])
def read_clips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clips = db.query(models.Clip).offset(skip).limit(limit).all()
    return clips

@router.get("/search/")
def search_clips(query: str, db: Session = Depends(get_db)):
    # Search by anime name or clip title
    results = db.query(models.Clip).join(models.Anime).filter(
        (models.Clip.title.ilike(f"%{query}%")) | 
        (models.Anime.name.ilike(f"%{query}%"))
    ).all()
    
    return results

@router.get("/{clip_id}/file")
def get_clip_file(clip_id: int, db: Session = Depends(get_db)):
    clip = db.query(models.Clip).filter(models.Clip.id == clip_id).first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    file_path = os.path.join(MEDIA_DIR, clip.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type="video/mp4", filename=clip.filename)