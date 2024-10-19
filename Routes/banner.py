from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from utils import client, handle_exception
from functools import wraps
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from typing import Optional
from Models.banner_model import Banner_model

app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home
fs = AsyncIOMotorGridFSBucket(mydb)


@app.put("/update_banner")
@handle_exception
async def update_banner(file: UploadFile = File(...)):
    """
    Uploads a banner to the database. The file is stored in the GridFS of the MongoDB database.

    Args:
    - file (UploadFile): The file to be uploaded.

    Returns:
    - dict: A dictionary containing the message "File Uploaded successfully" and the "_id" of the file in the database.

    Raises:
    - HTTPException: If there is an error while uploading the file.
    """

    file_content = await file.read()

    # stores the uploaded file in the database
    grid_in = fs.open_upload_stream(filename=file.filename)

    # writes the content in the file into chunks
    await grid_in.write(file_content)

    # Finalizes the file by closing
    await grid_in.close()
    # File Id
    file_id = grid_in._id
    raise HTTPException(
        status_code=200, detail=f"File Uploaded successfully with _id: {str(file_id)}")
