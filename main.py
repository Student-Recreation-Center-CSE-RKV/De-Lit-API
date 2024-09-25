from fastapi import FastAPI
import home,magazine,blog
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

app = FastAPI()
url = "mongodb+srv://phanivutla2004:phaniphani@cluster0.gddku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(url, server_api=ServerApi('1'))
#connections
app.include_router(home.app, prefix="/home")
app.include_router(magazine.app, prefix="/magazine")
app.include_router(blog.app,prefix = "/blog")