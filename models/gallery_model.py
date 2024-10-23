from pydantic import BaseModel
from typing import Optional
import datetime


class Image(BaseModel):
    event_name: str
    image_id: str
    # link: str
    date: str
    description: str
    created_at: datetime.datetime = datetime.datetime.now()


class ImageUpdateModel(BaseModel):
    event_name: Optional[str] = None
    image_id: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
