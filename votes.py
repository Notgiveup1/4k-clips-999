from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/submit", response_model=schemas.VoteAnime)
def submit_anime(anime: schemas.VoteAnimeCreate, db: Session = Depends(get_db)):
    # Check if anime already exists in voting list
    db_anime = db.query(models.VoteAnime).filter(models.VoteAnime.name == anime.name).first()
    if db_anime:
        raise HTTPException(status_code=400, detail="Anime already in voting list")
    
    db_anime = models.VoteAnime(**anime.dict())
    db.add(db_anime)
    db.commit()
    db.refresh(db_anime)
    return db_anime

@router.post("/{anime_id}/vote", response_model=schemas.VoteAnime)
def vote_anime(anime_id: int, db: Session = Depends(get_db)):
    db_anime = db.query(models.VoteAnime).filter(models.VoteAnime.id == anime_id).first()
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found in voting list")
    
    db_anime.votes += 1
    db.commit()
    db.refresh(db_anime)
    return db_anime

@router.get("/", response_model=List[schemas.VoteAnime])
def get_vote_animes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    animes = db.query(models.VoteAnime).order_by(models.VoteAnime.votes.desc()).offset(skip).limit(limit).all()
    return animes