from fastapi import HTTPException
from bson import ObjectId
from utilities.utils import client
import datetime
from models.blog_model import blog, update

mydb = client['Delit-test']
blog_con = mydb.blog

class GetAllBlogs() :
    @staticmethod
    async def execute() :
        """
        Retrieve all blogs from the database.

        Returns:
        - blogs (list): List of blogs with each blog as a dictionary containing the fields author, blog_name, link, content, overview, and _id.

        Raises:
        - HTTPException: If there is an error while fetching the blogs.
        """

        blogs = []
        async for blog in blog_con.find().sort("created_at", -1):
            blog["_id"] = str(blog["_id"])
            blogs.append(blog)
        if not blogs:
            raise HTTPException(
                status_code=404, detail="No blogs found. Please upload blogs before fetching.")
        return blogs


class GetBlogById() :
    @staticmethod
    async def execute(id : str) :
        """
        Retrieve a specific blog by its id.

        Arguments:
        - id (str): The id of the blog to be get.

        Returns:
        - blog (dict): The get blog with fields author, blog_name, link, content, overview, and _id.

        Raises:
        - HTTPException: one if the id is invalid or The blog is not found.
        """

        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=404, detail="Invalid blog ID format")
        _blog = await blog_con.find_one({"_id": ObjectId(id)})
        if _blog is None:
            raise HTTPException(status_code=404, detail="Blog not found")

        _blog["_id"] = str(_blog["_id"])
        return _blog


class UploadBlog() :
    @staticmethod
    async def execute(blog: blog) -> blog:
        """
        Upload a blog to the database.

        Structure of blog:
            {
                "author": "string",
                "blog_name": "string",
                "link": "string",
                "content": "string",
                "overview": "string"
                "created_at": "datetime"(automatically added at the time of uploading)
            }

        Args:
        - blog (blog): Pydantic model of the blog to be uploaded.

        Returns:
        - blog (dict): The uploaded blog with an additional "_id" field containing the MongoDB ObjectId of the blog.

        Raises:
        - HTTPException: If there is an error while uploading the blog.
        """
        blog = blog.model_dump()
        blog["created_at"] = datetime.datetime.now()
        result = await blog_con.insert_one(blog)
        if result.inserted_id:
            blog["_id"] = str(result.inserted_id)
            return blog
        else:
            raise HTTPException(
                status_code=400, detail=f"Can't upload the data into Database")


class UpdateBlog() :
    @staticmethod
    async def execute(id: str, update_data: update):
        """
        Update a specific blog by its id.

        Args:
        - id (str): The id of the blog to be updated.
        - update_data (update): The data to be updated. The fields that are not provided will not be updated.

        Returns:
        - result (dict): A dictionary containing the status of the update.
                        If the update is successful, it will contain {"success": "blog updated successfully"}.
                        If the update is not successful, it will contain the error message.

        Raises:
        - HTTPException: If the id is invalid, the blog is not found, or no data is provided for update.
        """
        try:
            if not ObjectId.is_valid(id):
                raise {"error": "Invalid ID format"}

            update_data = {k: v for k, v in update_data.dict().items()
                        if v is not None}

            if not update_data:
                raise {"error": "No data provided for update"}
            result = await blog_con.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            if result.modified_count == 0:
                return {"error": "No blog found with the given ID or no changes made"}

            raise HTTPException(
                status_code=200, detail="Blog updated successfully")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unknown error occurred: {str(e)}")


class DeleteBlog() :
    @staticmethod
    async def execute(blog_id: str):
        """
        Delete a specific blog by its id.

        Args:
        - blog_id (str): The id of the blog to be deleted.

        Returns:
        - result (dict): A dictionary containing the status of the deletion.
                        If the deletion is successful, it will contain {"Success": f"blog with id {blog_id} is successfully deleted"}.
                        If the deletion is not successful, it will contain the error message.

        Raises:
        - HTTPException: If the id is invalid, the blog is not found, or the deletion is not successful.
        """

        if not ObjectId.is_valid(blog_id):
            raise HTTPException(status_code=404, detail="Invalid blog ID format")
        blog = await blog_con.find_one({"_id": ObjectId(blog_id)})
        if not blog:
            raise HTTPException(status_code=404, detail="blog not found")
        delete_result = await blog_con.delete_one({"_id": ObjectId(blog_id)})
        if delete_result.deleted_count == 1:
            raise HTTPException(status_code=200,
                                detail=f"blog with id {blog_id} is successfully deleted")
        else:
            raise HTTPException(
                status_code=500, detail="Failed to delete the blog")
