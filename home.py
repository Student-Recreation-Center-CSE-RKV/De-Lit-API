from fastapi import APIRouter
import pymongo
import json
from utils import client

app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home

#endpoint
@app.get('/get_contact')
async def get_contact():
    result = connection.find_one({"name":"contact"})
    result["_id"] = str(result["_id"])
    return result

@app.get('/get_magazine')
async def get_magazine():
    result = connection.find_one({"name":"magazine"})
    result["_id"] = str(result["_id"])
    return result

@app.get('/get_about')
async def get_about():
    result = connection.find_one({"name":"about"})
    result["_id"] = str(result["_id"])
    return result

@app.get('/get_blog')
async def get_blog():
    result = connection.find_one({"name":"blog"})
    result["_id"] = str(result["_id"])
    return result