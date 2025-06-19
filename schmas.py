from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AnimeBase(BaseModel):
    name: str
    description: Optional[str] = None

class AnimeCreate(AnimeBase):
    pass

class Anime(AnimeBase):
    id: int
    preview_image: Optional[str] = None

    class Config:
        from_attributes = True

class ClipBase(BaseModel):
    title: str
    anime_id: int

class ClipCreate(ClipBase):
    pass

class Clip(ClipBase):
    id: int
    filename: str
    preview_url: str

    class Config:
        from_attributes = True

class VoteAnimeBase(BaseModel):
    name: str
    submitted_by: Optional[str] = None

class VoteAnimeCreate(VoteAnimeBase):
    pass

class VoteAnime(VoteAnimeBase):
    id: int
    votes: int

    class Config:
        from_attributes = True

class User(BaseModel):
    username: str

class UserInDB(User):
    password: str