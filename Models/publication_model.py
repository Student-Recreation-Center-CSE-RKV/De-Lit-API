from pydantic import BaseModel
from typing import Optional
import datetime

class Publication(BaseModel):
    publication_name: str
    link: str
    description: str
    publication_type: str
    img_link: str
    created_at: datetime.datetime = datetime.datetime.now()


class update(BaseModel):
    publication_name: Optional[str]
    link: Optional[str]
    description: Optional[str]
    publication_type: Optional[str]
    img_link: Optional[str]