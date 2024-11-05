from fastapi import APIRouter, File, UploadFile, Form
from utilities.utils import client, handle_exception
from controller.banner_controller import (
    GetBanner,
    UploadBanner
)

app = APIRouter(tags=['Banner'])
mydb = client['Delit-test']
banner_db = mydb.Banners

@app.put("/new_function")
@handle_exception
async def upload_banner(banner_id : str = Form(...),banner_image : UploadFile = File(...) ):
    """
    Upload a new banner image to GitHub and store the banner details in the database.

    This function takes a `banner_id` and an image file, uploads the image to GitHub,
    
    retrieves the image URL, and stores the banner details, including the URL, in the database.
    
    Args:
    
        banner_id (str): The unique identifier for the banner.
    
        banner_image (UploadFile): The image file for the banner to be uploaded.

    Returns:
    
        dict: A dictionary containing a success message and the newly created banner's `_id`.
    
        For example: {"Message": "Banner Uploaded Successfully", "_id": "<banner_id>"}.

    Raises:
    
        HTTPException: If there is an error uploading the banner image to GitHub.
        
        HTTPException: If there is an error inserting the banner data into the database.
    """
    return await UploadBanner.execute(banner_id=banner_id, banner_image= banner_image)


@app.get("/")
@handle_exception
async def get_banner():
    """
    Retrieve all banner images from the database, sorted by creation date.

    This function fetches all banners from the database, sorted in descending order by `created_at`.
    
    If no banners are found, an HTTPException is raised.

    Returns:
        
        list: A list of banner documents, each with `_id` as a string for easier JSON serialization.

    Raises:
        
        HTTPException: If no banners are found in the database.
    """
    return await GetBanner.execute()

