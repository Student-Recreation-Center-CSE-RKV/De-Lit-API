from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi import HTTPException
from functools import wraps

url = "mongodb+srv://phanivutla2004:phaniphani@cluster0.gddku.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true"
client = AsyncIOMotorClient(url, server_api=ServerApi("1"), connectTimeoutMS=50000)

GITHUB_TOKEN = ""
REPO_OWNER = "venkataPhanindraVutla"
REPO_NAME = "bar_code"
FOLDER_PATH = "pics"

def handle_exception(function):
    @wraps(function)
    async def wrapper(*arguments, **kwargs):
        try:
            return await function(*arguments, **kwargs)
        except HTTPException as http_exce:
            raise http_exce
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unknown error occurred.{str(e)}"
            )

    return wrapper
