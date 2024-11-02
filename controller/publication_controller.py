from utilities.utils import client
from fastapi import HTTPException , File, UploadFile
from bson import ObjectId
from models.publication_model import Publication, Update_publication
from utilities.gtihub_utilities import upload_to_github, delete_file_from_github
from typing import Optional
import datetime

mydb = client['Delit-test']
publication_db = mydb.publication

class GetAllPublications():
    @staticmethod
    async def execute():
        """
        Retrieve all publications from the database.
        Returns: 
            Publications (list): A list of dictionaries containing the fields publication_name, link, description, publication_type, img_link, and _id of each publication, sorted by creation date (latest first).
        Raises:
            HTTPException: If no publications are found in the database.
        """
        mags = []
        async for mag in publication_db.find().sort("created_at", -1):
            mag["_id"] = str(mag["_id"])
            mags.append(mag)
        if not mags:
            raise HTTPException(
                status_code=404, detail="No publications found. Please upload publications before fetching.")
        return mags

class GetPublicationByID():
    @staticmethod
    async def execute(id : str):
        """
        Retrieve a specific publication by its unique MongoDB ObjectId.
        Args:
            id (str): The ObjectId of the publication to be retrieved.
        Returns:
            publication (dict): The retrieved publication with an additional "_id" field containing the MongoDB ObjectId of the publication.
        Raises:
            HTTPException: If the id is invalid, the publication is not found, or the retrieval is not successful.
        """
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=404, detail="Invalid publication ID format")
        publication = await publication_db.find_one({"_id": ObjectId(id)})
        
        if publication is None:
            raise HTTPException(status_code=404, detail="publication not found")
        publication["_id"] = str(publication["_id"])
        return publication

class CreatePublication():
    @staticmethod
    async def execute(
            publication_name: str ,
            publication_type: str ,
            description: str ,
            Publication_File: UploadFile = File(...),
            Cover_Image: UploadFile = File(...),
        ):
        """
        Uploading publication file and cover image to GitHub and saving its metadata to MongoDB.
        Args:
            publication_name (str): Name of the publication.
            publication_type (str): Type or category of the publication.
            description (str): Description of the publication.
            Publication_File (UploadFile): The file representing the publication (e.g., PDF, Word).
            Cover_Image (UploadFile): The cover image for the publication (e.g., JPEG, PNG).
        Raises:
            HTTPException: 400 - Raised if there is an error while uploading the publication or cover image to GitHub.
            HTTPException: 400 - Raised if there is an error while saving the publication metadata to MongoDB.
        Returns:
            dict: A dictionary containing a success message and the inserted MongoDB document's ID if the upload succeeds.
        """
        pub_file_size = len(await Publication_File.read())
        max_length = 20*1024*1024
        if pub_file_size > max_length:
            raise HTTPException(status_code=413, detail="File Size Exceeds the limit 20 MB.")

        publication = Publication(
            publication_name=publication_name,
            description=description,
            publication_type=publication_type,
            created_at=datetime.datetime.now()
        )
        publication = publication.model_dump()
        # Content of the Publication
        pub_file_content = await Publication_File.read()
        # Content of the Cover Image
        cov_img_content = await Cover_Image.read()
        # uploading publication to github
        publication_response = await upload_to_github(pub_file_content, Publication_File.filename)
        # uploading coverimage to github
        cover_image_response = await upload_to_github(cov_img_content, Cover_Image.filename)
        if publication_response.status_code == 201 and cover_image_response.status_code == 201:
            publication_url = publication_response.json().get("content", {}).get("html_url", "")
            cover_image_url = cover_image_response.json().get("content", {}).get("html_url", "")
        
        else:
            print(publication_response.content)
            print(cover_image_response.content)
            raise HTTPException(status_code=400,detail="Error While Uploading The File Into Github")

        publication["publication_link"] = publication_url
        publication["cover_image_link"] = cover_image_url
        result = await publication_db.insert_one(publication)

        if result.inserted_id:
            publication["_id"] = str(result.inserted_id)
            return {"Message": "Publication Uploaded Successfully","_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=400,detail="Error While Uploading Publication Into the Database.")
        
class UpdatePublication():
    @staticmethod
    async def update_details(
            id : str,
            publication_name : Optional[str] = None,
            description : Optional[str] = None,
            publication_type : Optional[str] = None
        ):
        """
        Update a specific publication by its ID.
        Args:
            id (str): The ID of the publication to be updated. Must be a valid MongoDB ObjectId string.
            publication_name : The new name of the publication (if updating).
            description : The new description of the publication (if updating).
            publication_type : The new type of the publication (if updating).
        Returns:
            A dictionary indicating the success or failure of the update.
        Raises:
            HTTPException: If the `id` is invalid or improperly formatted.
                If no data is provided for updating.
                If the publication is not found or no modifications are made.
        """
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=404, detail="Invalid publication ID format")

        update_data = Update_publication(
            publication_name=publication_name,
            description=description,
            publication_type=publication_type,
        )
        
        update_data = update_data.model_dump()

        update_data = {k: v for k, v in update_data.items()if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided for update")
        result = await publication_db.update_one( {"_id": ObjectId(id)}, {"$set": update_data} )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="No publication found with the given ID or no changes made")
        
        raise HTTPException(status_code=201, detail="publication updated successfully")
    
    @staticmethod
    async def Update_image(id : str, cover_image : UploadFile = File(...)):
        """
        Update the cover image of a specific publication by its ID.
        Args:
            id (str): The ID of the publication to be updated. Must be a valid MongoDB ObjectId string.
            cover_image (UploadFile): The new cover image file to upload and link to the publication.
        Returns:
            Raises a 201 status code exception upon successful update of the cover image.
        Raises:
            HTTPException , if any error occurs while updating the cover image.
        """
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=404, detail="Invalid publication ID format")
        publication = await publication_db.find_one({"_id": ObjectId(id)})

        if not publication:
            raise HTTPException(status_code=404, detail="publication not found")
        # Deleting the old cover_image from the github
        cover_image_delete = await delete_file_from_github(publication["cover_image_link"])

        if cover_image_delete.status_code != 200:
            raise HTTPException(status_code=409, detail="conflict : Unable to change the file")
        # Uploading the new cover_image into the github
        cover_image_content = await cover_image.read()
        cover_image_response = await upload_to_github(cover_image_content, cover_image.filename)
        print(cover_image_response.status_code)
        if cover_image_response.status_code == 201:
            cover_image_url = cover_image_response.json().get("content", {}).get("html_url", "")

        else:
            raise HTTPException(status_code=400, detail="Error while uploading the cover image")

        publication_update = await publication_db.update_one({"_id": ObjectId(id)},{"$set": {"cover_image_link": cover_image_url}})
        if publication_update.modified_count == 0:
            raise HTTPException(status_code=400,detail="cover_image isn't changed")

        raise HTTPException(status_code=201, detail="cover_image changed Successfully")
    
class DeletePublication():
    @staticmethod
    async def execute(id : str):
        """
        Delete a specific publication by its id.
        Args:
            id (str): The id of the publication to be deleted.
        Returns:
            result (dict): A dictionary containing the status of the deletion.
        Raises:
            HTTPException: If the id is invalid, the publication is not found, or the deletion is not successful.
        """
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=404, detail="Invalid publication ID format")
        publication = await publication_db.find_one({"_id": ObjectId(id)})

        if not publication:
            raise HTTPException(status_code=404, detail="publication not found")

        # Deleting publication from github
        pub_delete = await delete_file_from_github(publication["publication_link"])
        # Deleting coverimage form github
        cover_image_delete = await delete_file_from_github(publication["cover_image_link"])
        if pub_delete.status_code != 200 or cover_image_delete.status_code != 200:
            raise HTTPException(
                status_code=409, detail="Conflict:Unable to Delete the File.")

        delete_publication = await publication_db.delete_one({"_id": ObjectId(id)})
        if delete_publication.deleted_count == 1:
            raise HTTPException(status_code=200,
                                detail=f"publication with id {id} is successfully deleted")
        else:
            raise HTTPException(
                status_code=500, detail="Failed to delete the publication")
