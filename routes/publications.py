from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from bson import ObjectId
from utilities.utils import client, handle_exception
from typing import Optional
from controller.publication_controller import (
    GetAllPublications,
    GetPublicationByID,
    UpdatePublication,
    DeletePublication,
    CreatePublication,
)

app = APIRouter(tags=["Publications"])
mydb = client["Delit-test"]
publication_db = mydb.publication


@app.post("/")
@handle_exception
async def post_publication(
    publication_name: str = Form(...),
    publication_type: str = Form(...),
    description: str = Form(...),
    Publication_File: UploadFile = File(...),
    Cover_Image: UploadFile = File(...),
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

    return await CreatePublication.execute(
        publication_name=publication_name,
        publication_type=publication_type,
        description=description,
        Publication_File=Publication_File,
        Cover_Image=Cover_Image,
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
    return await GetAllPublications.execute()


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
    return await GetPublicationByID.execute(id)


@app.put("/{id}")
@handle_exception
async def update_publication(
    id: str,
    publication_name: Optional[str] = None,
    description: Optional[str] = None,
    publication_type: Optional[str] = None,
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

    return await UpdatePublication.update_details(
        id, publication_name, description, publication_type
    )


@app.put("/update_image/{id}")
@handle_exception
async def update_publication_image(id: str, cover_image: UploadFile = File(...)):
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
    return await UpdatePublication.Update_image(id, cover_image)


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

    return DeletePublication.execute(id)
