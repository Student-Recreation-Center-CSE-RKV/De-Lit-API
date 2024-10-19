from fastapi import FastAPI
import routes.home as home
import routes.publications as publications
import routes.blog as blog
import routes.banner as banner
import routes.gallery as gallery
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify a list of origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(home.app, prefix="/home")
app.include_router(publications.app, prefix="/publications")
app.include_router(blog.app, prefix="/blog")
app.include_router(gallery.app, prefix="/gallery")
app.include_router(banner.app, prefix="/banner")


@app.get("/")
async def root_message():
    return {"message": "Welcome to the Delit-test API. Use the docs to get started. "}
