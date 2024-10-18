from fastapi import APIRouter , HTTPException, File, UploadFile, Form 
import httpx
from pydantic import BaseModel
from bson import ObjectId
from functools import wraps
import datetime
from typing import Optional
import base64
import re
from utils import client
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

app = APIRouter()

mydb = client['Delit-test']
gallery_db = mydb.gallery

REPO_OWNER = "N-Harsha-Vardhan-Dev"
REPO_NAME = "De-Lit-API"
FOLDER_PATH = "Resources/Gallery"  # Path to the folder in your repo where files are stored


class Image(BaseModel):
    event_name: str
    image_id : str
    # link: str
    date: str
    description: str
    created_at: datetime.datetime = datetime.datetime.now()

class ImageUpdateModel(BaseModel):
    event_name: Optional[str] = None
    image_id: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None

#Functions

def handle_exception(function):
# This wrapper function to implement DRY principle to handle try-except block.
    @wraps(function)
    async def wrapper(*arguments, **kwargs):
        try:
            return await function(*arguments, **kwargs)
        except HTTPException as http_exce:
            raise http_exce
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unknown error occurred.{str(e)}")
    return wrapper

async def upload_to_github(file_content, file_name):
    """ Uploading the actual image file into github repository

    Args:
        file_content ( File ): actual file 
        file_name ( str ): name of the file

    Returns:
        object : httpx.Response object
    """    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FOLDER_PATH}/{file_name}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Get current time for commit message
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "message": f"Add {file_name} at {now}",
        "content": base64.b64encode(file_content).decode("utf-8") # Encode image content into base64
    }
    response = httpx.put(url, json=data, headers=headers)
    return response

async def delete_file_from_github(link:str):
    """ Delete the file from github repository

    Args:
        link (str): path of the file 

    Raises:
        HTTPException: 404 (if repository not found)

    Returns:
        object : httpx.Response object
    """    
    pattern = r"blob/[^/]+/(.+)"
    match = re.search(pattern, link)
    if not match:
        HTTPException(
            status_code=404, detail="Link Not Found"
        )
    file_path = match.group(1)
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(
            status_code=404, detail="Folder not found"
        )
    sha = response.json()["sha"]
    data = {
        "message": f"Delete {file_path}",
        "sha": sha
    }
    response = httpx.delete(url, params=data, headers=headers)
    return response


#API END POINTS
@app.get("/")
@handle_exception
async def get_gallery() :
    """
    Retrieve all images from the database.

    Returns:
    - images (list): List of images with each image as a dictionary containing the fields event_name, image_id, link, date, description, _id.

    Raises:
    - HTTPException: If there is an error while fetching the images (gallery).
    """
    images = []
    async for image in gallery_db.find().sort("created_at", -1) :
        image["_id"] = str(image["_id"])
        images.append(image)
    if not images :
        raise HTTPException(
            status_code=404, detail="No images found. Please Upload images."
        )
    return images

@app.get("/{id}")
@handle_exception
async def get_single_image(id:str):
    """
    Retrieve a single image that have id

    Args:
        id (str): unique _id of the image in database

    Raises:
        HTTPException: 400 (Invalid image ID format)
        HTTPException: 404 (Image not found in database)

    Returns:
        image : image meta data (image details))
    """    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid image ID format")
    image = await gallery_db.find_one({"_id": ObjectId(id)})
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image["_id"] = str(image["_id"])
    return image

@app.post("/")
@handle_exception
async def upload_image(
    event_name: str = Form(...),
    image_id: str = Form(...),
    # link: str = Form(...),
    date: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),  
    # form is used when we include basemodel with upload file
) :
    """ Uploading image in github and its meta data in mongodb database

    Args:
        event_name (str, optional): Name of the event. Defaults to Form(...).
        image_id (str, optional): Image number . Defaults to Form(...).
        # link (str, optional): No Need. Defaults to Form(...).
        date (str, optional): Event date. Defaults to Form(...).
        description (str, optional): Description of the image. Defaults to Form(...).
        file (UploadFile, optional): Actual image . Defaults to File(...).

    Raises:
        HTTPException: 400 (if error in uploading image in github or meta data of image in database)

    Returns:
        image : image meta data (image details)
    """    
    
    image = Image( # Manually done
        event_name=event_name,
        image_id=image_id,
        # link=link,
        date=date,
        description=description,
        created_at=datetime.datetime.now()  # Automatically set the created_at timestamp
    )
    file_content = await file.read()
    image = image.model_dump()
    # Upload the file to GitHub
    response = await upload_to_github(file_content, file.filename)
    if response.status_code == 201:
        file_url = response.json().get("content", {}).get("html_url", "")
    else:
        raise HTTPException(status_code=400, detail="Error uploading file to GitHub")
    image["link"] = file_url
    image["created_at"] = datetime.datetime.now()
    result = await gallery_db.insert_one(image)
    if result.inserted_id :
        image["_id"] = str(result.inserted_id)
        return image
    else :
        raise HTTPException(
            status_code=400, detail="Can't upload image document into database"
        )

@app.put("/{id}")
@handle_exception
async def update_image(id: str, update_data: ImageUpdateModel):    
    """ Update an existing image document in the database

    Args:
        id (str): unique _id of image document
        update_data (ImageUpdateModel): A Pydantic model containing fields to be updated 

    Raises:
        HTTPException: 404 (Invalid image id format or if document not found )
        HTTPException: 400 (No new details provided)

    Returns:
        - dict: A dictionary with a success status and a message if the document is updated successfully.

    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Invalid image ID format")
    # Convert the update_data to a dictionary and remove None values
    update_data_dict = {k: v for k, v in update_data.dict().items() if (v.strip() != "" and v != "string")}
    
    if not update_data_dict:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_data_dict['created_at'] = datetime.datetime.now()
    result = await gallery_db.update_one(
        {"_id": ObjectId(id)},  # Filter by the provided _id
        {"$set": update_data_dict}  # Set the fields to be updated
    )

    if result.modified_count :
        return {"status": "success", "message": "Document updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Document not found or no changes made")

@app.delete("/{id}")
@handle_exception
async def remove_image(id: str):
    """ Deleting an existing image in Github and image data in Mongodb

    Args:
        id (str): unique _id of image document

    Raises:
        HTTPException: 404 (if Invalid image ID format or if image not found)
        HTTPException: 409 (if Unable to delete the image in github)
        HTTPException: 500 (if Failed to delete the image document in database)
        HTTPException: 200 (if image is successfully deleted)
    """    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Invalid image ID format")
    image = await gallery_db.find_one({"_id": ObjectId(id)})
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    response = await delete_file_from_github(image["link"])
    if response.status_code != 200 : 
        raise HTTPException(
            status_code=409, detail="Conflict: Unable to delete the image"
        )
    delete_result = await gallery_db.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        raise HTTPException(
            status_code=200, detail=f"image with id {id} is successfully deleted")
    else:
        raise HTTPException(
            status_code=500, detail="Failed to delete the image")
