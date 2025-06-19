from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from . import models
from .database import engine, SessionLocal
from .endpoints import anime, clips, votes, admin
from .auth import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anime Clip API", version="0.1.0")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(anime.router, prefix="/anime", tags=["anime"])
app.include_router(clips.router, prefix="/clips", tags=["clips"])
app.include_router(votes.router, prefix="/votes", tags=["votes"])
app.include_router(admin.router, tags=["admin"])

# Mount static files
app.mount("/static", StaticFiles(directory="media"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Anime Clip API"}