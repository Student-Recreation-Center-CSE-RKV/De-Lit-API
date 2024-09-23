from fastapi import APIRouter
from main import client
import json

app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home

@app.get("/get-info")
async def get_info():
    data = list(connection.find())
    for doc in data:
        doc["_id"] = str(doc["_id"])
    return data
