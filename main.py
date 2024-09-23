from fastapi import FastAPI
import home
import pymongo

app = FastAPI()
app = APIRouter()
url = "mongodb+srv://phanivutla2004:phaniphani@cluster0.gddku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(url, server_api=ServerApi('1'))
#connections
app.include_router(home.app, prefix="/home")
app.include_router(magazine.app,prefix="/magazine")