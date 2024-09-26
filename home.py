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

#contact  endpoints
@app.get('/get_contact')
async def get_contact():
    result = await connection.find_one({"name": "contact"})
    if not result:
        return {"error": "contact section not found"}
    result["_id"] = str(result["_id"])
    return result

@app.put('/update_contact')
async def update_contact(data: AllModel):
    updated_data = data.dict()
    result = await connection.find_one({"name": "contact"})
    if result:
        await connection.update_one({"name": "contact"}, {"$set": updated_data})
        return {"message": "Contact updated successfully"}
    else:
        await connection.insert_one(updated_data)
        return {"message": "Contact created successfully"}

#magazine endpoints
@app.get('/get_magazine')
async def get_magazine():
    result = await connection.find_one({"name": "magazine"})
    if not result:
        return {"error": "magazine section not found"}
    result["_id"] = str(result["_id"])
    return result

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

#about_endpoints
@app.get('/get_about')
async def get_about():
    result = await connection.find_one({"name": "about"})
    if not result:
        return {"error": "about section not found"}
    result["_id"] = str(result["_id"])
    return result

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

#blog endpoints
@app.get('/get_blog')
async def get_blog():
    result = await connection.find_one({"name": "blog"})
    if not result:
        return {"error": "blog section not found"}
    result["_id"] = str(result["_id"])
    return result

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

#clubtalk endpoints
@app.get('/get_clubtalk')
async def get_clubtalk():
    result = await connection.find_one({"name": "clubtalk"})
    if not result:
        return {"error": "clubtalk section not found"}
    result["_id"] = str(result["_id"])
    return result

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