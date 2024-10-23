from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from utils import client, handle_exception,upload_to_github
from functools import wraps
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from typing import Optional
from Models.banner_model import Banner_model
from bson import ObjectId

app = APIRouter(tags=['Banner'])
mydb = client['Delit-test']
banner_db = mydb.Banners



@app.put("/")
@handle_exception
async def update_banner(
    image_id : str = Form(...),
    file: UploadFile = File(...)):
    """
    Uploads a banner to the database. The file is stored in the GitHub and Link of the File is stored in the MongoDB database.

    Args:
    - file (UploadFile): The file to be uploaded.
    - image_id : The Manual Id of the image given by the user.

    Returns:
    - dict: A dictionary containing the message "Banner Changed successfully" and the "_id" of the file in the database.

    Raises:
    - HTTPException: If there is an error while uploading the file.
    """

    file_content = await file.read()

    banner = Banner_model(image_id = image_id)
    banner = banner.model_dump()
    #uploading file to github
    response = await upload_to_github(file_content,file.filename)

    if response.status_code == 201:
         file_url = response.json().get("content", {}).get("html_url", "")
    else :
        raise HTTPException(
            status_code=400, detail="Error Uploading file into github"
        )
    banner["link"]=file_url
    result = await banner_db.insert_one(banner)
    if result.inserted_id :
        banner["_id"] = str(result.inserted_id)
        return {"Message":"Banner Changed Successfully",
                "Banner_id":str(result.inserted_id)}
    else :
        raise HTTPException(
            status_code = 400,
            detail = "Can't Upload image into Database"
        )




