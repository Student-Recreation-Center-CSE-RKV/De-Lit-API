from fastapi import APIRouter, HTTPException,File,UploadFile,Form
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client, handle_exception,upload_to_github
import datetime
from functools import wraps
from typing import Optional
from Models.publication_model import Publication, Update_publication

app = APIRouter(tags=['Publications'])
mydb = client['Delit-test']
publication_db = mydb.publication


@app.post("/")
@handle_exception
async def post_publication(
    publication_name : str = Form(...),
    publication_type: str = Form(...),
    description: str = Form(...),
    Publication_File : UploadFile = File(...),
    Cover_Image : UploadFile = File(...),
):
    """
Uploading publication file and cover image to GitHub and saving its metadata to MongoDB.


Args:
    publication_name (str): Name of the publication. Defaults to Form(...).

    publication_type (str): Type or category of the publication. Defaults to Form(...).

    description (str): Description of the publication. Defaults to Form(...).

    Publication_File (UploadFile): The file representing the publication (e.g., PDF, Word). Defaults to File(...).
    
    Cover_Image (UploadFile): The cover image for the publication (e.g., JPEG, PNG). Defaults to File(...).

Raises:
   
     HTTPException: 400 - Raised if there is an error while uploading the publication or cover image to GitHub.
   
     HTTPException: 400 - Raised if there is an error while saving the publication metadata to MongoDB.

Returns:
    
    dict: A dictionary containing a success message and the inserted MongoDB document's ID if the upload succeeds.
"""

   
    publication = Publication(
       publication_name = publication_name,
       description = description,
       publication_type = publication_type,
       created_at = datetime.datetime.now()
   )
    publication = publication.model_dump()
    # Content of the Publication
    pub_file_content = await Publication_File.read()
    # Content of the Cover Image
    cov_img_content = await Cover_Image.read()
    #uploading publication to github
    publication_response = await upload_to_github(pub_file_content,Publication_File.filename)
    #uploading coverimage to github
    cover_image_response = await upload_to_github(cov_img_content,Cover_Image.filename)
    if publication_response.status_code == 201 :
        publication_url = publication_response.json().get("content", {}).get("html_url", "")
    else :
        print(publication_response.content)
        raise HTTPException(
            status_code = 400,
            detail = "Error While Uploading Publication Into Github"
        )
    if cover_image_response.status_code == 201 :
        cover_image_url = cover_image_response.json().get("content", {}).get("html_url", "")
    else :
        print(cover_image_response.content)
        raise HTTPException(
            status_code = 400,
            detail = "Error While Uploading CoverImage into Github"
        )
    publication["publication_link"] = publication_url
    publication["cover_image_link"] = cover_image_url
    result = await publication_db.insert_one(publication)

    if result.inserted_id :
        publication["_id"] = str(result.inserted_id)
        return {"Message":"Publication Uploaded Successfully",
                "_id":str(result.inserted_id)
                }
    else :
        raise HTTPException(
            status_code = 400,
            detail = "Error While Uploading Publication Into the Database."
        )


@app.get("/")
@handle_exception
async def get_publication():
    """
    Retrieve all publications from the database.

    Returns:
    - publications (list): A list of dictionaries containing the fields publication_name, link, description, publication_type, img_link, and _id of each publication, sorted by creation date (latest first).

    Raises:
    - HTTPException: If no publications are found in the database.
    """
    mags = []
    async for mag in publication_db.find().sort("created_at", -1):
        mag["_id"] = str(mag["_id"])
        mags.append(mag)
    if not mags:
        raise HTTPException(
            status_code=404, detail="No publications found. Please upload publications before fetching.")
    return mags


@app.get("/{id}")
@handle_exception
async def get_publication(id: str):
    """
    Retrieve a specific publication by its unique MongoDB ObjectId.

    Args:
    - id (str): The ObjectId of the publication to be retrieved.

    Returns:
    - publication (dict): The retrieved publication with an additional "_id" field containing the MongoDB ObjectId of the publication.

    Raises:
    - HTTPException: If the id is invalid, the publication is not found, or the retrieval is not successful.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=404, detail="Invalid publication ID format")
    _publication = await publication_db.find_one({"_id": ObjectId(id)})
    if _publication is None:
        raise HTTPException(status_code=404, detail="publication not found")
    _publication["_id"] = str(_publication["_id"])
    return _publication


@app.put("/{id}")
@handle_exception
async def update_publication(id: str,
                              publication_name : Optional[str] = None,
                              description : Optional[str] = None,
                              publication_type : Optional[str] = None,
                              cover_image : Optional[UploadFile] = File(None)):
    """
    Update a specific publication by its ID.

    This function updates the details of a publication in the database, identified by its ID. 

    It allows updating the publication name, description, type, and optionally a cover image. 
    
    If a new cover image is provided, it uploads it to GitHub and stores the new URL in the database.

    Args:
    
        id (str): The ID of the publication to be updated. Must be a valid MongoDB ObjectId string.
        
        publication_name (Optional[str]): The new name of the publication (if updating).
        
        description (Optional[str]): The new description of the publication (if updating).
        
        publication_type (Optional[str]): The new type of the publication (if updating).
        
        cover_image (Optional[UploadFile]): The new cover image to upload and update (if updating).

    Returns:
        
        dict: A dictionary indicating the success or failure of the update.
              
              If successful, it returns {"success": "publication updated successfully"}.
              
              If no changes were made, it raises an HTTP exception.

    Raises:
       
        HTTPException: If the `id` is invalid or improperly formatted.
        
        HTTPException: If no data is provided for updating.
        
        HTTPException: If the cover image upload to GitHub fails.
        
        HTTPException: If the publication is not found or no modifications are made.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=404, detail="Invalid publication ID format")
    
    update_data = Update_publication (
        publication_name = publication_name,
        description = description,
        publication_type = publication_type,
    )
    update_data = update_data.model_dump()

    if cover_image and isinstance(cover_image,UploadFile) :
        
        cover_image_content = cover_image.read()
        cover_image_response = await upload_to_github(cover_image_content,cover_image.filename)
        if cover_image_response.status_code == 201 :
            cover_image_url = cover_image_response.json().get("content", {}).get("html_url", "")
            update_data['cover_image_url'] = cover_image_url
        else :
            raise HTTPException(
                status_code = 400,
                detail = "Error While changing the Cover Image"
            )



    update_data = {k: v for k, v in update_data.items()
                   if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=400, detail="No data provided for update")
    result = await publication_db.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="No publication found with the given ID or no changes made")
    raise HTTPException(
        status_code=201, detail="publication updated successfully")


@app.delete("/{id}")
@handle_exception
async def remove_publication(id: str):
    """
    Delete a specific publication by its id.

    Args:
    - id (str): The id of the publication to be deleted.

    Returns:
    - result (dict): A dictionary containing the status of the deletion.
                    If the deletion is successful, it will contain {"success": "publication with id {id} is successfully deleted"}.
                    If the deletion is not successful, it will contain the error message.

    Raises:
    - HTTPException: If the id is invalid, the publication is not found, or the deletion is not successful.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=404, detail="Invalid publication ID format")
    publication = await publication_db.find_one({"_id": ObjectId(id)})
    if not publication:
        raise HTTPException(status_code=404, detail="publication not found")
    delete_result = await publication_db.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        raise HTTPException(status_code=200,
                            detail=f"publication with id {id} is successfully deleted")
    else:
        raise HTTPException(
            status_code=500, detail="Failed to delete the publication")
