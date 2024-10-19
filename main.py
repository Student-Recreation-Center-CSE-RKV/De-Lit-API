from fastapi import FastAPI
import Routes.home as home
import Routes.publications as publications
import Routes.blog as blog
import Routes.banner as banner
import Routes.gallery as gallery
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

app = FastAPI()
# connections
app.include_router(home.app, prefix="/home")
app.include_router(publications.app, prefix="/publications")
app.include_router(blog.app, prefix="/blog")
app.include_router(gallery.app, prefix="/gallery")
app.include_router(banner.app, prefix="/banner")


@app.get("/")
async def root_message():
    return {"message": "Welcome to the Delit-test API. Use the docs to get started. http://localhost:8000/docs"}
