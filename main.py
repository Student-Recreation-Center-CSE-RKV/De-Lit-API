from fastapi import FastAPI
import routes.home as home
import routes.publications as publications
import routes.blog as blog
import routes.banner as banner
import routes.gallery as gallery
import routes.mail as mail
import routes.file_upload as file_upload
import routes.footer as footer
import routes.login as login
import routes.users as users
from fastapi.middleware.cors import CORSMiddleware
from utilities.middleware_utilities import JWTMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify a list of origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Adding custom middleware for JWTAuthentication
app.add_middleware(JWTMiddleware)

# routers
app.include_router(home.app, prefix="/home",tags=["Home"])
app.include_router(publications.app, prefix="/publications",tags=["Publications"])
app.include_router(blog.app, prefix="/blog",tags=["Blog"])
app.include_router(gallery.app, prefix="/gallery",tags=["Gallery"])
app.include_router(banner.app, prefix="/banner",tags=["Banner"])
app.include_router(footer.app, prefix="/footer", tags=["Footer"])
app.include_router(file_upload.app, prefix="/file_upload",tags=["File Upload"])
app.include_router(mail.app, prefix="/mail",tags=["Mail"])
app.include_router(login.app, prefix="/login",tags=["Login"])
app.include_router(users.app, prefix = "/users",tags=["User"])

@app.get("/",tags=["Root"])
async def root_message():
    return {"message": "Welcome to the Delit-test API. Use the docs to get started."}
