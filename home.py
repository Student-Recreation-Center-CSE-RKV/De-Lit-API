from fastapi import APIRouter
import pymongo
import json
from main import client

app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home

#endpoint
@app.get('/get_contact')
async def get_contact():
    data = list(connection.find())
    for doc in data:
        doc["_id"] = str(doc["_id"])
    return data

# "https://raw.githubusercontent.com/venkataPhanindraVutla/Demo-Names/blob/main/images/R200026.jpg"