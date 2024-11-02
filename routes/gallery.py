from fastapi import APIRouter, File, UploadFile, Form
import datetime
from bson import ObjectId
from utilities.utils import client, handle_exception
from models.gallery_model import Image, ImageUpdateModel
from controller.gallery_controller import (
    GetAllImages,
    GetImageById,
    UploadImage,
    UpdateImage,
    DeleteImage
)

app = APIRouter()

mydb = client['Delit-test']
gallery_db = mydb.gallery


# API END POINTS
@app.get("/")
@handle_exception
async def get_gallery():
    """
    Summary :
    
        Retrieve all images from the database.

    Returns:
    
        images (list): List of images with each image as a dictionary containing the fields event_name, image_id, link, date, description, _id.

    Raises:
    
        HTTPException: If there is an error while fetching the images (gallery).
    """
    return await GetAllImages.execute()


@app.get("/{id}")
@handle_exception
async def get_individual_image(id: str):
    """
    Summary :
    
        Retrieve a single image that have id

    Args:
        
        id (str): unique _id of the image in database

    Raises:
        
        HTTPException: 400 (Invalid image ID format)
        HTTPException: 404 (Image not found in database)

    Returns:
        
        image : image meta data (image details))
    """
    return await GetImageById.execute(id)

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
    """
    Summary :
        
        Uploading image in github and its meta data in mongodb database.

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
    return await UploadImage.execute(
        event_name = event_name,
        image_id = image_id,
        date = date,
        description = description,
        file = file,   
    )

@app.put("/{id}")
@handle_exception
async def update_image(id: str, update_data: ImageUpdateModel):
    """ 
    Summary :
    
        Update an existing image document in the database

    Args:
    
        id (str): unique _id of image document
        update_data (ImageUpdateModel): A Pydantic model containing fields to be updated 

    Raises:
    
        HTTPException: 404 (Invalid image id format or if document not found )
        HTTPException: 400 (No new details provided)

    Returns:
    
        - dict: A dictionary with a success status and a message if the document is updated successfully.

    """
    return await UpdateImage.execute(
        id = id,
        update_data = update_data
    )


@app.delete("/{id}")
@handle_exception
async def remove_image(id: str):
    """
    Summary :
    
        Deleting an existing image in Github and image data in Mongodb

    Args:
    
        id (str): unique _id of image document

    Raises:
    
        HTTPException: 404 (if Invalid image ID format or if image not found)
        HTTPException: 409 (if Unable to delete the image in github)
        HTTPException: 500 (if Failed to delete the image document in database)
        HTTPException: 200 (if image is successfully deleted)
    """
    return await DeleteImage.execute(id = id)