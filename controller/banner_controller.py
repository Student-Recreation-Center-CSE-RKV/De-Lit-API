from fastapi import HTTPException, File, UploadFile, Form
from utilities.utils import client
from models.banner_model import Banner_model
from utilities.gtihub_utilities import upload_to_github,delete_file_from_github
from bson import ObjectId

mydb = client['Delit-test']
banner_db = mydb.Banners

class GetBanner() :
    @staticmethod
    async def execute() :
        """
        Retrieve all banner images from the database, sorted by creation date.

        This function fetches all banners from the database, sorted in descending order by `created_at`.
        
        If no banners are found, an HTTPException is raised.

        Returns:
            
            list: A list of banner documents, each with `_id` as a string for easier JSON serialization.

        Raises:
            
            HTTPException: If no banners are found in the database.
        """

        banners = []
        async for banner in banner_db.find().sort("created_at",-1):
            banner["_id"] = str(banner["_id"])
            banners.append(banner)
        if not banners :
            raise HTTPException(
                status_code = 404,
                detail = "No Banners Found.Please Upload the Banner before fetching"
            )
        return banners

class UploadBanner() :
    @staticmethod
    async def execute(banner_id : str = Form(...),banner_image : UploadFile = File(...) ) :
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

        banner = Banner_model(banner_id = banner_id)
        banner = banner.model_dump()

        banner_content = await banner_image.read()
        banner_response = await upload_to_github(banner_content, banner_image.filename)
        if banner_response.status_code == 201 :
            banner_url = banner_response.json().get("content", {}).get("html_url", "")
        else :
            raise HTTPException(
                status_code= 400,
                detail= "Error While Uploading into github"
            )
        banner["banner_link"] = banner_url
        result = await banner_db.insert_one(banner)
        if result.inserted_id :
            banner["_id"] = str(result.inserted_id)
            return {
                "Message":"Banner Uploaded Successfully",
                "_id" : str(result.inserted_id)
            }
        else :
            raise HTTPException(
                status_code= 400,
                detail = "Error While Uploading into Database"
            )

class UpdateBanner() :
    @staticmethod
    async def execute(id : str,banner_image: UploadFile = File(...)):
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
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code = 404,
                                detail = "Invalid Id Format.")
        
        banner = await banner_db.find_one({"_id":ObjectId(id)})

        if not banner :
            raise HTTPException(status_code = 404 , detail = "Banner not found with the given id.")
        
        #Deleting the old banner_image form the github
        banner_delete = await delete_file_from_github(banner["banner_link"])

        if banner_delete.status_code !=200 :
            raise HTTPException(
                status_code = 409,
                detail = "Conflict : Unalbe to upload the banner"
            )

        #uploading the new banner_image  into github
        banner_content = await banner_image.read()

        banner_response  = await upload_to_github(banner_content,banner_image.filename)

        if banner_response.status_code == 201:
            banner_url = banner_response.json().get("content", {}).get("html_url", "")
        else :
            raise HTTPException(
                status_code=400, detail="Error Uploading file into github"
            )

        banner_update = await banner_db.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"banner_link":banner_url}}
        )
        if banner_update.modified_count == 0:
            raise HTTPException(
                status_code = 400,
                detail = "banner_image isn't changed"
            )
        raise HTTPException(
            status_code = 201,
            detail = "banner_image updated successfully"
        )