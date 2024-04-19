import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from database import database as database
from database.database import MusicTrackDB
from model.musictrack import MusicTrack

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/get_tracks")
async def get_tracks(db: db_dependency):
    try:
        result = db.query(MusicTrackDB).limit(100).all()
        return result
    except Exception as e:
        return "Cant access database!"


@app.get("/get_track_by_id")
async def get_track_by_id(track_id: int, db: db_dependency):
    try:
        result = db.query(MusicTrackDB).filter(MusicTrackDB.id == track_id).first()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Track not found")


@app.post("/add_track")
async def add_track(track: MusicTrack, db: db_dependency):
    try:
        track_db = MusicTrackDB(
            id=track.id,
            title=track.title,
            artist=track.artist,
            release_date=track.release_date,
            genre=track.genre
        )
        db.add(track_db)
        db.commit()
        return track_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Track not found")


@app.delete("/delete_track")
async def delete_track(track_id: int, db: db_dependency):
    try:
        track_db = db.query(MusicTrackDB).filter(MusicTrackDB.id == track_id).first()
        db.delete(track_db)
        db.commit()
        return "Success"
    except Exception as e:
        return "Cant find track"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
