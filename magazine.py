from fastapi import APIRouter
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client


app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home

class Magazine(BaseModel):
    magazine_name:str
    author:str
    part:int

@app.get("/get-info")
async def get_info():
    data = await connection.find().to_list(length=None)
    for doc in data:
        doc["_id"] = str(doc["_id"])
    return data

@app.put("/magazine_upload")
async def post_magazine(mag:Magazine):
    book=mag.model_dump()
    try:
        result = await connection.insert_one(book)
        return {"_id":"Done"}
    except Exception as e:
        return {"error": str(e)}  # Return the error for easier debugging

