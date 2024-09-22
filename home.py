from fastapi import APIRouter
import pymongo
import json

app = APIRouter()
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = client['phani']
connection = mydb.Phani

#end
@app.get('/get_contact')
async def get_contact():
    data = list(connection.find())
    for doc in data:
        doc["_id"] = str(doc["_id"])
    return data

# "https://raw.githubusercontent.com/venkataPhanindraVutla/Demo-Names/blob/main/images/R200026.jpg"