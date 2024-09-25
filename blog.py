from fastapi import APIRouter,HTTPException
import json
from pydantic import BaseModel
from bson import ObjectId
from utils import client
import datetime
from typing import Optional

app = APIRouter()
mydb = client['Delit-test']
blog_con = mydb.blog

class blog(BaseModel):
    author : str
    blog_name : str
    link : str
    content : str
    overview : str

class update(BaseModel):
    author : Optional[str]
    blog_name: Optional[str]
    link: Optional[str]
    content : Optional[str]
    overview : Optional[str]


#To upload the blog to database
@app.put("/blog_upload")
async def post_blog(blog:blog):
    try:
        blog=blog.model_dump()
        result = await blog_con.insert_one(blog)
        if result.inserted_id:
            blog["_id"] = str(result.inserted_id)
            return blog
    except Exception as e:
        return {"error": str(e)}


#To get all blogs
@app.get("/all_blogs")
async def get_blogs():
    try:
        blogs = []
        async for blog in blog_con.find():
            blog["_id"] = str(blog["_id"])
            blogs.append(blog)
        if not blogs:
            return {"error": "No blogs found. Please upload blogs before fetching."}
        return blogs
    except Exception as e:
        return {"error": str(e)}


#To get specified blog with id
@app.get("/{id}")
async def get_blog(id:str):
    try:
        if not ObjectId.is_valid(id):
            raise {"error":"Invalid ID format"}
        _blog = await blog_con.find_one({"_id":ObjectId(id)})
        if _blog is None:
            raise {"status_code=404": "Blog not found"}
        _blog["_id"]=str(_blog["_id"])
        return _blog
    except Exception as e :
        return {"Error":str(e)}


#To update the blog
@app.put("/update_blog/{id}")
async def update_blog(id: str, update_data: update):
    try:
        if not ObjectId.is_valid(id):
            raise {"error":"Invalid ID format"}       
 
        update_data = {k: v for k, v in update_data.dict().items() if v is not None}

        if not update_data:
            raise {"error": "No data provided for update"}
        result = await blog_con.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            return {"error": "No blog found with the given ID or no changes made"}
        return {"success": "blog updated successfully"}
    except Exception as e:
        raise {"status_code=500": f"An error occurred: {str(e)}"}
    
#To remove specific blog with id
@app.delete("/remove_blog/{blog_id}")
async def remove_blog(blog_id:str):
    try:
        if not ObjectId.is_valid(blog_id):
            raise {"error" :"Invalid blog ID format"}
        blog = await blog_con.find_one({"_id": ObjectId(blog_id)})
        if not blog:
            raise HTTPException(status_code=404, detail="blog not found")
        delete_result = await blog_con.delete_one({"_id": ObjectId(blog_id)})
        if delete_result.deleted_count == 1:
            return {"Success": f"blog with id {blog_id} is successfully deleted"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete the blog")
    except Exception as e:
        raise {"status_code=500": str(e)}