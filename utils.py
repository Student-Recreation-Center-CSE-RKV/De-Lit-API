from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

url = "mongodb+srv://phanivutla2004:phaniphani@cluster0.gddku.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true"
client = AsyncIOMotorClient(url,server_api=ServerApi('1'))