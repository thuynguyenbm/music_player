from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from database import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    artist = Column(String(50), index=True)
    album = Column(String(50), index=True)
    content = Column(Text, unique=False, index=True)


class SongBase(BaseModel):
    title: str
    artist: str
    album: str
    content: str

class SongDTO(SongBase):
    id: int

    class Config:
        orm_mode = True