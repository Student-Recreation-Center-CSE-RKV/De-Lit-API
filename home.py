from fastapi import APIRouter
import pymongo
import json

app = APIRouter()
url = "mongodb+srv://phanivutla2004:phaniphani@cluster0.gddku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(url, server_api=ServerApi('1'))
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