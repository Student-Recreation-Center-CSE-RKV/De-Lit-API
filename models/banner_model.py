from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime


class Banner_model(BaseModel):
    created_at:datetime = Field(default_factory=datetime.now)
    banner_id:str
    #Banner_link=link
    class config:
        arbitrary_types_allowed = True
   