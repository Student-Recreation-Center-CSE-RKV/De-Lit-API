from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from utils import client, handle_exception
from functools import wraps
from bson import ObjectId
from Models.home_model import BlockModel

app = APIRouter(tags=['Home'])
mydb = client["Delit-test"]
connection = mydb.home


@app.get("/")
@handle_exception
async def get_all_blocks() -> list:
    """
    Retrieve data for all 4 blocks on the homepage.

    This function fetches data from the database, formats it, and returns a list of objects.

    Each object represents a block with the following structure:
    - name : The name of the block.
    - content: A description of the block.
    - image_link : The image image_link for the block.

    Returns :
        list: A list of dictionaries containing block data (name, content, and image image_link).

    Raises:
        HTTPException: If no data is found in the database.
    """
    result = await connection.find().to_list(length=None)
    if not result:
        raise HTTPException(
            status_code=404, detail="Data Not found in the database")
    # Convert MongoDB ObjectId to string.
    for res in result:
        res["_id"] = str(res["_id"])
    return result


@app.get("/{name}")
@handle_exception
async def get_block_data(name: str) -> dict:
    """
    Retrieve data for a specific block by name.

    This function takes the block name as input, converts it to lowercase, checks if it exists in the predefined blocks list,
    and then retrieves the corresponding data from the database.

    If the block is invalid or not found in the database, an appropriate HTTPException is raised.

    Args:
        name (str): The name of the block to retrieve.

    Returns:
        dict: A dictionary containing the block's data (name, content, and image image_link).

    Raises:
        HTTPException: If the block name is invalid or the data is not found in the database.
    """
    name = name.lower()
    result = await connection.find_one({"name": name})
    if not result:
        raise HTTPException(
            status_code=404, detail="Data not found in the database.")
    # Convert the MongoDB ObjectId to a string
    result["_id"] = str(result["_id"])
    return result


@app.put("/{block_name}")
@handle_exception
async def update_block(block_name: str, data: BlockModel):
    """
    Update a specific block by its name.

    Args:
    - block_name (str): The name of the block to update.
    - data (BlockModel): The data to be updated.

    Returns:
    - result (dict): A dictionary containing the status of the update.
                    If the update is successful, it will contain {"success": "block updated successfully"}.
                    If the update is not successful, it will contain the error message.

    Raises:
    - HTTPException: If the block name is invalid or the data is not found in the database.
    """
    block_name = block_name.lower()
    result = await connection.find_one({"name": block_name})
    if not result:
        raise HTTPException(
            status_code=404, detail="Data not found in the database.")
    updated_data = data.model_dump()
    await connection.update_one({"name": block_name}, {"$set": updated_data})
    return {"message": "Block updated successfully"}


@app.delete("/{block_name}")
@handle_exception
async def delete_block(block_name: str):
    """
    Delete a specific block by its name.

    Args:
    - block_name (str): The name of the block to delete.

    Returns:
    - result (dict): A dictionary containing the status of the deletion.
                    If the deletion is successful, it will contain {"success": "block deleted successfully"}.
                    If the deletion is not successful, it will contain the error message.

    Raises:
    - HTTPException: If the block name is invalid or the data is not found in the database.
    """
    block_name = block_name.lower()
    result = await connection.find_one({"name": block_name})
    if not result:
        raise HTTPException(
            status_code=404, detail="Data not found in the database.")
    await connection.delete_one({"name": block_name})
    return {"message": "Block deleted successfully"}
