from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Song, SongBase, SongDTO
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/songs/", response_model=SongDTO)
def create_song(song: SongBase, db: Session = Depends(get_db)):
    new_song = Song(title=song.title, artist=song.artist, album=song.album, content=song.content)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


@app.get("/songs/{song_id}", response_model=SongDTO, response_class=HTMLResponse)
def read_song(song_id: int, request: Request, db: Session = Depends(get_db)):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return templates.TemplateResponse(
        request=request, name="song.html", context={"song": db_song}
    )

@app.get("/songs/", response_model=list[SongDTO])
def read_songs(offset: int = 0, limit: int = 1, db: Session = Depends(get_db)):
    return db.query(Song).offset(offset).limit(limit).all()

@app.delete("/songs/{song_id}", response_model=SongDTO)
def delete_song(song_id: int, db: Session = Depends(get_db)):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(db_song)
    db.commit()
    return db_song

