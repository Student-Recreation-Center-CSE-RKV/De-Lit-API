from fastapi import APIRouter,HTTPException
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client
import datetime

app = APIRouter()

class blog(BaseModel):
    name : str
    author : str

# @app.get("/all_blogs")
# async def get_blogs():
