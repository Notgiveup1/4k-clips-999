from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Anime)
def create_anime(anime: schemas.AnimeCreate, db: Session = Depends(get_db)):
    db_anime = models.Anime(**anime.dict())
    db.add(db_anime)
    db.commit()
    db.refresh(db_anime)
    return db_anime

@router.get("/", response_model=List[schemas.Anime])
def read_animes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    animes = db.query(models.Anime).offset(skip).limit(limit).all()
    return animes

@router.get("/{anime_id}", response_model=schemas.Anime)
def read_anime(anime_id: int, db: Session = Depends(get_db)):
    anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return anime