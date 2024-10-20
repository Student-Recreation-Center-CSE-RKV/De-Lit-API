from pydantic import BaseModel
from typing import Optional
import datetime


class BlockModel(BaseModel):
    name: str
    content: str
    image_link: str
