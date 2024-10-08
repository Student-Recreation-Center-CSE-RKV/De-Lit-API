from fastapi import APIRouter, HTTPException,File,UploadFile,Form
from pydantic import BaseModel
from utils import client
from functools import wraps
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId

app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home
fs=AsyncIOMotorGridFSBucket(mydb)

# pydantic model


class AllModel(BaseModel):
    name: str
    content: str
    link: str


blocks = {"contact", "about", "clubtalk", "blog", "publications"}

# This wrapper function to implement DRY principle to handle try-except block.


def handle_exception(function):
    @wraps(function)
    async def wrapper(*arguments, **kwargs):
        try:
            return await function(*arguments, **kwargs)
        except HTTPException as http_exce:
            raise http_exce
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unknown error occurred.{str(e)}")

    return wrapper


@app.get("/")
@handle_exception
async def get_all_blocks() -> list:
    """
    Retrieve data for all 4 blocks on the homepage.

    This function fetches data from the database, formats it, and returns a list of objects.
    Each object represents a block with the following structure:
    - name : The name of the block.
    - content: A description of the block.
    - link : The image link for the block.
    Returns :
        list: A list of dictionaries containing block data (name, content, and image link).
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
        dict: A dictionary containing the block's data (name, content, and image link).

    Raises:
        HTTPException: If the block name is invalid or the data is not found in the database.
    """
    name = name.lower()
    # Check if the block name is valid or not by comparing it against the blocks set.
    if name not in blocks:
        raise HTTPException(
            status_code=404, detail="Invalid block accessed. Check the name correctly.")
    result = await connection.find_one({"name": name})
    if not result:
        raise HTTPException(
            status_code=404, detail="Data not found in the database.")
    # Convert the MongoDB ObjectId to a string
    result["_id"] = str(result["_id"])
    return result


@app.put('/block1')
async def update_contact(data: AllModel):
    updated_data = data.dict()
    result = await connection.find_one({"name": "contact"})
    if result:
        await connection.update_one({"name": "contact"}, {"$set": updated_data})
        return {"message": "Contact updated successfully"}
    else:
        await connection.insert_one(updated_data)
        return {"message": "Contact created successfully"}


@app.put('/update_magazine')
async def update_magazine(data: AllModel):
    updated_data = data.dict()
    result = await connection.find_one({"name": "magazine"})
    if result:
        await connection.update_one({"name": "magazine"}, {"$set": updated_data})
        return {"message": "Magazine updated successfully"}
    else:
        await connection.insert_one(updated_data)
        return {"message": "Magazine created successfully"}


@app.put('/update_about')
async def update_about(data: AllModel):
    updated_data = data.dict()
    result = await connection.find_one({"name": "about"})
    if result:
        await connection.update_one({"name": "about"}, {"$set": updated_data})
        return {"message": "About section updated successfully"}
    else:
        await connection.insert_one(updated_data)
        return {"message": "About section created successfully"}


@app.put('/update_blog')
async def update_blog(data: AllModel):
    updated_data = data.dict()
    result = await connection.find_one({"name": "blog"})
    if result:
        await connection.update_one({"name": "blog"}, {"$set": updated_data})
        return {"message": "Blog updated successfully"}
    else:
        await connection.insert_one(updated_data)
        return {"message": "Blog created successfully"}


@app.put('/update_clubtalk')
async def update_clubtalk(data: AllModel):
    updated_data = data.dict()
    result = await connection.find_one({"name": "clubtalk"})
    if result:
        await connection.update_one({"name": "clubtalk"}, {"$set": updated_data})
        return {"message": "Clubtalk updated successfully"}
    else:
        await connection.insert_one(updated_data)
        return {"message": "Clubtalk created successfully"}
    
@app.put("/update_banner")
@handle_exception
async def update_banner(file:UploadFile=File(...)):
    """
    Updates the HomeBanner:
        This function is used to update the Banner in the home page in regular intervals,
        Here the image is uploaded from the user and the image is converted in string and stored in the database.
    """
   
    # reads the uploaded file
    file_content=await file.read()

    #stores the uploaded file in the database
    grid_in=fs.open_upload_stream(filename=file.filename)

    #writes the content in the file into chunks
    await grid_in.write(file_content)

    #Finalizes the file by closing
    await grid_in.close()
    #File Id
    file_id=grid_in._id  
   
    return{"message":"File Uploaded successfully","_id":str(file_id)} 

