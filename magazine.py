from fastapi import APIRouter,HTTPException
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client
import datetime


app = APIRouter()
mydb = client['Delit-test']
mag_con = mydb.magazine

class Magazine(BaseModel):
    magazine_name : str
    link : str
    description : str
    date : datetime.date

class update(BaseModel):
    magazine_name : str|None
    link : str | None
    description : str | None
    date : datetime.date | None

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
    
@app.put("/update_mag/{id}")
async def update_magazine(id: str, update_data: update):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")       
 
        update_data = {k: v for k, v in update_data.dict().items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided for update")
        result = await mag_con.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            return {"error": "No magazine found with the given ID or no changes made"}
        return {"success": "Magazine updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")