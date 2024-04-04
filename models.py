from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    artist = Column(String(50), index=True)
    album = Column(String(50), index=True)
    content = Column(Text, unique=True, index=True)

class SongBase(BaseModel):
    title: str
    artist: str
    album: str
    content: str

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True