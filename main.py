from fastapi import FastAPI
import Routes.home as home
import Routes.publications as publications
import Routes.blog as blog
import Routes.banner as banner
import Routes.gallery as gallery
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
app.include_router(home.app, prefix="/home",tags=["Home"])
app.include_router(publications.app, prefix="/publications",tags=["Publications"])
app.include_router(blog.app, prefix="/blog",tags=["Blog"])
app.include_router(gallery.app, prefix="/gallery",tags=["Gallery"])
app.include_router(banner.app, prefix="/banner",tags=["Banner"])


@app.get("/",tags=["Root"])
async def root_message():
    return {"message": "Welcome to the Delit-test API. Use the docs to get started."}
