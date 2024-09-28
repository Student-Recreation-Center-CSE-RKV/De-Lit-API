from fastapi import APIRouter
from pydantic import BaseModel
from utils import client

app = APIRouter()
mydb = client['Delit-test']
connection = mydb.home

#pydantic model
class AllModel(BaseModel):
    name: str
    content: str
    link: str

blocks = {"contact","about","clubtalk","blog","publications"}

@app.get("/")
async def get_all():
    try:
        result = await connection.find().to_list(length=None)
        if not result:
            return {"error 404": "Data Not found in database"}
        for res in result:
            res["_id"] = str(res["_id"])
        return result
    except Exception as e:
        return {"error 500":f"An unexpected error occured {e}"}

@app.get("/{name}")
async def get_data(name:str):
    try :
        name = name.lower()
        if name not in blocks:
            return {"error 404":"Invalid block accessed.Check the name correctly"}
        result = await connection.find({"name":name})
        if not result:
            return {"error 404": "Data Not found in database"}
        result["_id"] = str(result["_id"])
        return result
    except Exception as e:
        return {"error 500":f"An unexpected error occured {e}"}

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