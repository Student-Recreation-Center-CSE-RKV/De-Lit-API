from fastapi import FastAPI
import home,publications,blog
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

app = FastAPI()
#connections
app.include_router(home.app, prefix="/home")
app.include_router(publications.app, prefix="/publications")
app.include_router(blog.app,prefix = "/blog")