from fastapi import FastAPI
import home,magazine
import pymongo

app = FastAPI()
#connections
app.include_router(home.app, prefix="/home")
app.include_router(magazine.app,prefix="/magazine")