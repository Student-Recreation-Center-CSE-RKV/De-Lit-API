from fastapi import APIRouter,HTTPException
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client
import datetime
from typing import Optional

app = APIRouter()
mydb = client['Delit-test']
mag_con = mydb.magazine

class Magazine(BaseModel):
    magazine_name : str
    link : str
    description : str
    # date : datetime.date
    # image : str

class update(BaseModel):
    magazine_name: Optional[str]
    link: Optional[str]
    description: Optional[str]
    # date: Optional[datetime.date]

@app.put("/magazine_upload")
async def post_magazine(mag:Magazine):
    try:
        book=mag.model_dump()
        result = await mag_con.insert_one(book)
        if result.inserted_id:
            book["_id"] = str(result.inserted_id)
            return book
    except Exception as e:
        return {"error": str(e)}

@app.get("/all_mags")
async def get_magazine():
    try:
        mags = []
        async for mag in mag_con.find():
            mag["_id"] = str(mag["_id"])
            mags.append(mag)
        if not mags:
            return {"error": "No magazines found. Please upload magazines before fetching."}
        return mags
    except Exception as e:
        return {"error": str(e)}

@app.get("/{id}")
async def get_magazine(id:str):
    try:
        if not ObjectId.is_valid(id):
            raise {"error":"Invalid ID format"}
        _magazine = await mag_con.find_one({"_id":ObjectId(id)})
        if _magazine is None:
            raise {"status_code=404": "magazine not found"}
        _magazine["_id"]=str(_magazine["_id"])
        return _magazine
    except Exception as e :
        return {"Error":str(e)}

@app.put("/update_mag/{id}")
async def update_magazine(id: str, update_data: update):
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
            return {"error": "No magazine found with the given ID or no changes made"}
        return {"success": "Magazine updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@app.delete("/remove_magazine/{magazine_id}")
async def remove_magazine(magazine_id:str):
    try:
        if not ObjectId.is_valid(magazine_id):
            raise {"error" :"Invalid magazine ID format"}
        magazine = await mag_con.find_one({"_id": ObjectId(magazine_id)})
        if not magazine:
            raise HTTPException(status_code=404, detail="Magazine not found")
        delete_result = await mag_con.delete_one({"_id": ObjectId(magazine_id)})
        if delete_result.deleted_count == 1:
            return {"Success": f"Magazine with id {magazine_id} is successfully deleted"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete the magazine")
    except Exception as e:
        raise {"status_code=500": str(e)}