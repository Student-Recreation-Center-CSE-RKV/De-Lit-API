from pydantic import BaseModel

class refresh_token_request(BaseModel):
    refresh_token : str
