from pydantic import BaseModel
from typing import Optional
import datetime


class blog(BaseModel):
    author: str
    blog_name: str
    link: str
    content: str
    overview: str
    created_at: datetime.datetime = datetime.datetime.now()


class update(BaseModel):
    author: Optional[str]
    blog_name: Optional[str]
    link: Optional[str]
    content: Optional[str]
    overview: Optional[str]
