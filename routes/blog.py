from fastapi import APIRouter
from utilities.utils import client, handle_exception
from models.blog_model import blog, update
from controller.blog_controller import (
    GetAllBlogs,
    GetBlogById,
    UploadBlog,
    UpdateBlog,
    DeleteBlog
)

app = APIRouter(tags=['Blog'])

@app.post("/")
@handle_exception
async def upload_blog(blog: blog) -> blog:
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
    return await UploadBlog.execute(blog = blog)

@app.get("/")
@handle_exception
async def get_blogs():
    """
    Retrieve all blogs from the database.

    Returns:
    - blogs (list): List of blogs with each blog as a dictionary containing the fields author, blog_name, link, content, overview, and _id.

    Raises:
    - HTTPException: If there is an error while fetching the blogs.
    """

    return await GetAllBlogs.execute()

@app.get("/{id}")
@handle_exception
async def get_blog(id: str):
    """
    Retrieve a specific blog by its id.

    Arguments:
    - id (str): The id of the blog to be get.

    Returns:
    - blog (dict): The get blog with fields author, blog_name, link, content, overview, and _id.

    Raises:
    - HTTPException: one if the id is invalid or The blog is not found.
    """
    return await GetBlogById.execute(id = id)


@app.put("/{id}")
@handle_exception
async def update_blog(id: str, update_data: update):
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
    return await UpdateBlog.execute(id = id , update_data = update_data)


@app.delete("/{blog_id}")
@handle_exception
async def remove_blog(blog_id: str):
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
    return await DeleteBlog.execute(blog_id = blog_id)
