from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client, handle_exception
import datetime
from functools import wraps
from typing import Optional
from models.publication_model import Publication, update

app = APIRouter()
mydb = client['Delit-test']
mag_con = mydb.publication


@app.post("/")
@handle_exception
async def post_publication(mag: Publication):
    """
    Uploads a publication to the database.

    Args:
    - mag (Publication): Pydantic model of the publication to be uploaded.

    Returns:
    - publication (dict): The uploaded publication with an additional "_id" field containing the MongoDB ObjectId of the publication.

    Raises:
    - HTTPException: If there is an error while uploading the publication.
    """
    publication = mag.model_dump()
    publication["created_at"] = datetime.datetime.now()
    result = await mag_con.insert_one(publication)
    if result.inserted_id:
        publication["_id"] = str(result.inserted_id)
        return publication
    else:
        raise HTTPException(
            status_code=400, detail=f"Can't upload the data into Database")


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
    async for mag in mag_con.find().sort("created_at", -1):
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
    _publication = await mag_con.find_one({"_id": ObjectId(id)})
    if _publication is None:
        raise HTTPException(status_code=404, detail="publication not found")
    _publication["_id"] = str(_publication["_id"])
    return _publication


@app.put("/{id}")
@handle_exception
async def update_publication(id: str, update_data: update):
    """
    Update a specific publication by its id.

    Args:
    - id (str): The id of the publication to be updated.
    - update_data (update): The data to be updated. The fields that are not provided will not be updated.

    Returns:
    - result (dict): A dictionary containing the status of the update.
                    If the update is successful, it will contain {"success": "publication updated successfully"}.
                    If the update is not successful, it will contain the error message.

    Raises:
    - HTTPException: If the id is invalid, the publication is not found, or no data is provided for update.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=404, detail="Invalid publication ID format")
    update_data = {k: v for k, v in update_data.dict().items()
                   if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=400, detail="No data provided for update")
    result = await mag_con.update_one(
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
    publication = await mag_con.find_one({"_id": ObjectId(id)})
    if not publication:
        raise HTTPException(status_code=404, detail="publication not found")
    delete_result = await mag_con.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        raise HTTPException(status_code=200,
                            detail=f"publication with id {id} is successfully deleted")
    else:
        raise HTTPException(
            status_code=500, detail="Failed to delete the publication")
