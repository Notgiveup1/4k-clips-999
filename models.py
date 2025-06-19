from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    preview_image = Column(String, nullable=True)
    
    clips = relationship("Clip", back_populates="anime")

class Clip(Base):
    __tablename__ = "clips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    filename = Column(String)
    anime_id = Column(Integer, ForeignKey("animes.id"))
    preview_url = Column(String)
    
    anime = relationship("Anime", back_populates="clips")

class VoteAnime(Base):
    __tablename__ = "vote_animes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    votes = Column(Integer, default=0)
    submitted_by = Column(String, nullable=True)