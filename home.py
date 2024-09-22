from fastapi import APIRouter
app = APIRouter()
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = client['phani']
connection = client['home_details']

#endpoint
@app.get('get_contact')
async def get_contact():
    return None
# "https://raw.githubusercontent.com/venkataPhanindraVutla/Demo-Names/blob/main/images/R200026.jpg"