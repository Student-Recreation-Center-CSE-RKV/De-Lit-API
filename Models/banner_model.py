from pydantic import BaseModel
from typing import Optional
import datetime


class Banner_model(BaseModel):
    image_link: str