from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime


class Banner_model(BaseModel):
    created_at:datetime = Field(default_factory = datetime.now)
    image_id:str
    #link=link
    class config:
        arbitrary_types_allowed=True