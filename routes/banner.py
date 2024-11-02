from fastapi import APIRouter, File, UploadFile, Form
from utilities.utils import client, handle_exception
from controller.banner_controller import (
    GetBanner,
    UploadBanner,
    UpdateBanner
)

app = APIRouter(tags=['Banner'])
mydb = client['Delit-test']
banner_db = mydb.Banners

@app.post("/")
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


@app.put("/")
@handle_exception
async def update_banner(id : str,banner_image: UploadFile = File(...)):
    """
    Update an existing banner's image in the database.

    This function updates a banner's image by first validating the banner ID, deleting the existing banner image from GitHub,
    
    uploading the new image, and updating the image link in the MongoDB database.

    Args:
    
        id (str): The ID of the banner to update. Must be a valid MongoDB ObjectId string.
    
        banner_image (UploadFile): The new banner image file to upload and link to the banner.

    Returns:
    
        HTTPException: Raises a 201 status code exception upon successful update with a message indicating success.

    Raises:
    
        HTTPException: If the `id` is invalid or improperly formatted.
    
        HTTPException: If no banner is found with the given ID.
    
        HTTPException: If there is a conflict or error when deleting the current banner image from GitHub.
    
        HTTPException: If there is an error uploading the new banner image to GitHub.
    
        HTTPException: If the database update for the banner image link fails.
    """
    
    return await UpdateBanner.execute(id = id , banner_image = banner_image)