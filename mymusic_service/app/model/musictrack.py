from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MusicTrack(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    title: str
    artist: str
    release_date: Optional[datetime] = datetime.now()
    genre: str
