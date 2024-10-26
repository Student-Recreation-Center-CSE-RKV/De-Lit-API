from fastapi import APIRouter, HTTPException,File,UploadFile,Form
from bson import ObjectId
from utilities.utils import client, handle_exception
from utilities.gtihub_utilities import upload_to_github,delete_file_from_github
import datetime
from functools import wraps
from typing import Optional
from models.publication_model import Publication, Update_publication

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

    # Determines the length of the file
    pub_file_size = len(await Publication_File.read())
    max_length = 15*1024*1024
    if pub_file_size > max_length :
        raise HTTPException(status_code=413 , detail = "File Size Exceeds the limit 15 MB.")


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
    if publication_response.status_code == 201 and cover_image_response.status_code == 201  :
       
        publication_url = publication_response.json().get("content", {}).get("html_url", "")
       
        cover_image_url = cover_image_response.json().get("content", {}).get("html_url", "")
    else :
        print(publication_response.content)
        print(cover_image_response.content)
        raise HTTPException(
            status_code = 400,
            detail = "Error While Uploading The File Into Github"
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
    publication = await publication_db.find_one({"_id": ObjectId(id)})
    if publication is None:
        raise HTTPException(status_code=404, detail="publication not found")
    publication["_id"] = str(publication["_id"])
    return publication




@app.put("/{id}")
@handle_exception
async def update_publication(id: str,
                              publication_name : Optional[str] = None,
                              description : Optional[str] = None,
                              publication_type : Optional[str] = None,
                               ):
    """
    Update a specific publication by its ID.

    This function updates the details of a publication in the database, identified by its ID. 

    It allows updating the publication name, description, type . 
    
   
    Args:
    
        id (str): The ID of the publication to be updated. Must be a valid MongoDB ObjectId string.
        
        publication_name (Optional[str]): The new name of the publication (if updating).
        
        description (Optional[str]): The new description of the publication (if updating).
        
        publication_type (Optional[str]): The new type of the publication (if updating).
        
        

    Returns:
        
        dict: A dictionary indicating the success or failure of the update.
              
              If successful, it returns {"success": "publication updated successfully"}.
              
              If no changes were made, it raises an HTTP exception.

    Raises:
       
        HTTPException: If the `id` is invalid or improperly formatted.
        
        HTTPException: If no data is provided for updating.
        
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
    update_data =  update_data.model_dump()

     
    
    
       



    update_data = {k: v for k, v in update_data.items()
                   if v is not None}
    print(update_data)

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


@app.put("/update_image/{id}")
@handle_exception
async def update_publication_image(id: str , cover_image : UploadFile = File(...)):
    """
    Update the cover image of a specific publication by its ID.

    This function replaces the cover image of an existing publication with a new one.

    It verifies the publication ID, deletes the current cover image from GitHub, 
    
    uploads the new image, and updates the cover image link in the database.

    Args:
    
        id (str): The ID of the publication to be updated. Must be a valid MongoDB ObjectId string.
    
        cover_image (UploadFile): The new cover image file to upload and link to the publication.

    Returns:
    
        HTTPException: Raises a 201 status code exception upon successful update of the cover image.

    Raises:
    
        HTTPException: If the `id` is invalid or improperly formatted.
    
        HTTPException: If no publication is found with the given ID.
    
        HTTPException: If there is an error deleting the current cover image from GitHub.
    
        HTTPException: If there is an error uploading the new cover image.
    
        HTTPException: If the database update for the cover image link fails.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=404, detail="Invalid publication ID format")
    publication = await publication_db.find_one({"_id": ObjectId(id)})
    
    if not publication:
        raise HTTPException(status_code=404, detail="publication not found")
    #Deleting the old cover_image from the github
    cover_image_delete = await delete_file_from_github(publication["cover_image_link"])

    if cover_image_delete.status_code != 200 :
        raise HTTPException(status_code = 409 ,detail= "conflict : Unable to change the file")
    #Uploading the new cover_image into the github
    cover_image_content = await cover_image.read()
    cover_image_response = await upload_to_github(cover_image_content, cover_image.filename)

    if cover_image_response.status_code == 201:
        cover_image_url = cover_image_response.json().get("content", {}).get("html_url", "")
                
    else:
        raise HTTPException(status_code=400, detail="Error while uploading the cover image")
        
    publication_update = await publication_db.update_one(
        {"_id":ObjectId(id)},
        {"$set":{"cover_image_link":cover_image_url}}
    )
    if publication_update.modified_count == 0 :
        raise HTTPException(
            status_code = 400,
            detail = "cover_image isn't changed"
        )

    raise HTTPException(
        status_code=201 , detail="cover_image changed Successfully"
    )
        
        
        
        
    

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
    
    # Deleting publication from github
    pub_delete = await delete_file_from_github(publication["publication_link"])
    #Deleting coverimage form github
    cover_image_delete = await delete_file_from_github(publication["cover_image_link"])
    if pub_delete.status_code != 200 or cover_image_delete.status_code != 200 :
        raise HTTPException(status_code= 409, detail="Conflict:Unable to Delete the File.")

    delete_publication = await publication_db.delete_one({"_id": ObjectId(id)})
    if delete_publication.deleted_count == 1:
        raise HTTPException(status_code=200,
                            detail=f"publication with id {id} is successfully deleted")
    else:
        raise HTTPException(
            status_code=500, detail="Failed to delete the publication")
