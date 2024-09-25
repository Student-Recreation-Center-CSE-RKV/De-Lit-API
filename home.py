from fastapi import APIRouter
import json
from utils import client

app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home

#endpoint
@app.get('/get_contact')
async def get_contact():
    result =await connection.find_one({"name":"contact"})
    result["_id"] = str(result["_id"])
    return result

@app.get('/get_magazine')
async def get_magazine():
    result =await connection.find_one({"name":"magazine"})
    result["_id"] = str(result["_id"])
    return result

@app.get('/get_about')
async def get_about():
    result =await connection.find_one({"name":"about"})
    result["_id"] = str(result["_id"])
    return result

@app.get('/get_blog')
async def get_blog():
    result =await connection.find_one({"name":"blog"})
    result["_id"] = str(result["_id"])
    return result

@app.get('/get_clubtalk')
async def get_clubtalk():
    result =await connection.find_one({"name":"clubtalk"})
    for res in result:
        if res:
            res["_id"]=str(res["_id"])
    return result