from fastapi import APIRouter,HTTPException
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client
import datetime
from typing import Optional

app = APIRouter()
mydb = client['Delit-test']
mag_con = mydb.publication

class Publication(BaseModel):
    publication_name : str
    link : str
    description : str
    publication_type : str
    # date : datetime.date
    # image : str

class update(BaseModel):
    publication_name: Optional[str]
    link: Optional[str]
    description: Optional[str]
    # date: Optional[datetime.date]

@app.post("/")
async def post_publication(mag:Publication):
    try:
        book = mag.model_dump()
        result = await mag_con.insert_one(book)
        if result.inserted_id:
            book["_id"] = str(result.inserted_id)
            return book
        else :
            raise HTTPException(status_code = 400 , detail = f"Can't upload the data into Database")
    except Exception as e:
        raise HTTPException(status_code = 500 , detail = f"An unknown error occurred. {str(object=e)}")

@app.get("/")
async def get_publication():
    try:
        mags = []
        async for mag in mag_con.find():
            mag["_id"] = str(mag["_id"])
            mags.append(mag)
        if not mags:
            return {"error": "No publications found. Please upload publications before fetching."}
        return mags
    except Exception as e:
        return {"error": str(e)}

@app.get("/{id}")
async def get_publication(id:str):
    try:
        if not ObjectId.is_valid(id):
            raise {"error":"Invalid ID format"}
        _publication = await mag_con.find_one({"_id":ObjectId(id)})
        if _publication is None:
            raise {"status_code=404": "publication not found"}
        _publication["_id"]=str(_publication["_id"])
        return _publication
    except Exception as e :
        return {"Error":str(e)}

@app.put("/{id}")
async def update_publication(id: str, update_data: update):
    try:
        if not ObjectId.is_valid(id):
            raise {"error":"Invalid ID format"}       
 
        update_data = {k: v for k, v in update_data.dict().items() if v is not None}

        if not update_data:
            raise {"error": "No data provided for update"}
        result = await mag_con.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            return {"error": "No publication found with the given ID or no changes made"}
        return {"success": "publication updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@app.delete("/{id}")
async def remove_publication(id:str):
    try:
        if not ObjectId.is_valid(id):
            raise {"error" :"Invalid publication ID format"}
        publication = await mag_con.find_one({"_id": ObjectId(id)})
        if not publication:
            raise HTTPException(status_code=404, detail="publication not found")
        delete_result = await mag_con.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return {"Success": f"publication with id {id} is successfully deleted"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete the publication")
    except Exception as e:
        raise {"status_code=500": str(e)}