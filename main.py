from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Song, SongBase, Base
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

@app.post("/songs/", response_model=Song)
def create_song(song: SongBase, db: Session = Depends(get_db)):
    db_song = Song(title=song.title, artist=song.artist, album=song.album, content=song.content)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.get("/songs/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="song.html", context={"id": id}
    )

@app.get("/songs/{song_id}", response_model=Song)
def read_song(song_id: int, db: Session = Depends(get_db)):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song

@app.get("/songs/", response_model=list[Song])
def read_songs(offset: int = 0, limit: int = 1, db: Session = Depends(get_db)):
    # list_songs = db.query(Song).offset(offset).limit(limit).all()
    list_songs = db.query(Song).first
    return list_songs

@app.delete("/songs/{song_id}", response_model=Song)
def delete_song(song_id: int, db: Session = Depends(get_db)):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(db_song)
    db.commit()
    return db_song

