from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

url = "mongodb+srv://phanivutla2004:phaniphani@cluster0.gddku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(url,server_api=ServerApi('1'))