from fastapi import FastAPI
import home

app = FastAPI()
#connections
app.include_router(home.app, prefix="/home")