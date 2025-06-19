from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_active_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/anime/", response_model=schemas.Anime)
def admin_create_anime(
    anime: schemas.AnimeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_active_user)
):
    return create_anime(anime, db)

# Reuse other endpoints but with admin protection
from .anime import create_anime
from .clips import create_clip