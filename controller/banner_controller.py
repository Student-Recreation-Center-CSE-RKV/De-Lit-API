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

    This function takes a unique `banner_id` and an image file, uploads the image to GitHub,
    retrieves the image URL, and stores the banner details, including the URL, in the database.

    Args:
        banner_id (str): The unique identifier for the banner.
        banner_image (UploadFile): The image file for the banner to be uploaded.

    Returns:
        dict: A dictionary containing a success message and the newly created banner's `_id`.
              For example: {"Message": "Banner Uploaded Successfully", "_id": "<banner_id>"}.

    Raises:
        HTTPException: 
            - If the banner already exists and the current banner link is missing (404).
            - If there is a conflict while trying to delete the old banner image from GitHub (409).
            - If there is an error while uploading the new banner image to GitHub (400).
            - If there is an error while inserting or updating the banner data into the database (400).
    """
        banner_exists = await banner_db.find_one({"banner_id":banner_id})
        if banner_exists is not None :
            if "banner_link" not in banner_exists or not banner_exists["banner_link"]:
                raise HTTPException(
                    status_code=404,
                    detail = "banner link is missing."
                )
            #Deleting the old banner_image form the github
            banner_delete = await delete_file_from_github(banner_exists["banner_link"])

            if banner_delete.status_code !=200 :
                 raise HTTPException(
                status_code = 409,
                detail = "Conflict : Unalbe to upload the banner"
                 )

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
        result = await banner_db.update_one({"banner_id":banner_id},
                                            {"$set":{"banner_link":banner_url}},upsert=True)
        if result.modified_count == 1 :
            return {
                "Message":"Banner Updated Successfully",
               
            }
        elif result.upserted_id :
            banner["_id"] = str(result.upserted_id)
            return {
                "message":"New Banner Created Successfully",
                "_id":str(result.upserted_id)
            }
        else :
            raise HTTPException(
                status_code= 400,
                detail = "Error While Uploading into Database"
            )

