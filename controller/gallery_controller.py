from fastapi import HTTPException, File, UploadFile, Form
import datetime
from bson import ObjectId
from utilities.utils import client
from models.gallery_model import Image, ImageUpdateModel
from utilities.gtihub_utilities import upload_to_github, delete_file_from_github

mydb = client['Delit-test']
gallery_db = mydb.gallery

class GetAllImages() :
    @staticmethod
    async def execute() :
        """
        Summary :
        
            Retrieve all images from the database.

        Returns:
        
            images (list): List of images with each image as a dictionary containing the fields event_name, image_id, link, date, description, _id.

        Raises:
        
            HTTPException: If there is an error while fetching the images (gallery).
        """
        images = []
        async for image in gallery_db.find().sort("created_at", -1):
            image["_id"] = str(image["_id"])
            images.append(image)
        if not images:
            raise HTTPException(
                status_code=404, detail="No images found. Please Upload images."
            )
        return images

class GetImageById() :
    @staticmethod
    async def execute(id : str) :
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
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid image ID format")
        image = await gallery_db.find_one({"_id": ObjectId(id)})
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")

        image["_id"] = str(image["_id"])
        return image

class UploadImage() :
    @staticmethod
    async def execute(
            event_name: str = Form(...),
            image_id: str = Form(...),
            date: str = Form(...),
            description: str = Form(...),
            file: UploadFile = File(...),  
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

class UpdateImage() :
    @staticmethod
    async def execute(id: str, update_data: ImageUpdateModel) :
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

        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=404, detail="Invalid image ID format")
        # Convert the update_data to a dictionary and remove None values
        update_data_dict = {k: v for k, v in update_data.dict(
        ).items() if (v.strip() != "" and v != "string")}

        if not update_data_dict:
            raise HTTPException(
                status_code=400, detail="No fields provided for update")

        update_data_dict['created_at'] = datetime.datetime.now()
        result = await gallery_db.update_one(
            {"_id": ObjectId(id)},  # Filter by the provided _id
            {"$set": update_data_dict}  # Set the fields to be updated
        )

        if result.modified_count:
            return {"status": "success", "message": "Document updated successfully"}
        else:
            raise HTTPException(
                status_code=404, detail="Document not found or no changes made")

class DeleteImage() :
    @staticmethod
    async def execute(id : str) :
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
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=404, detail="Invalid image ID format")
        image = await gallery_db.find_one({"_id": ObjectId(id)})
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        response = await delete_file_from_github(image["link"])
        if response.status_code != 200:
            raise HTTPException(
                status_code=409, detail="Conflict: Unable to delete the image"
            )
        delete_result = await gallery_db.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return {"status": "success", "message": f"Image with ID {id} successfully deleted"}
        else:
            raise HTTPException(
                status_code=500, detail="Failed to delete the image")