from pydantic import BaseModel
from typing import Optional
import datetime


class Publication(BaseModel):
    publication_name: str
    #pulication_link: str
    description: str
    publication_type: str
    #cover_image_link: str
    created_at: datetime.datetime = datetime.datetime.now()


class Update_publication(BaseModel):
    publication_name: Optional[str]
    description: Optional[str]
    publication_type: Optional[str]
   # cover_image_link: Optional[str]
