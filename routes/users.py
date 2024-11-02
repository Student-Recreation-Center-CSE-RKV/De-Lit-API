from fastapi import APIRouter, Form,Request
from controller.users_controller import GetAllUsers, CreateUser, DeleteUser
from utilities.utils import handle_exception

app = APIRouter()


@app.post("/", summary="Create a new user")
@handle_exception
async def create_user(username: str = Form(...), password: str = Form(...)) -> dict:
    """
    API endpoint to create a new user with the specified username and password.
    """
    return await CreateUser.execute(username, password)


@app.delete("/", summary="Delete an existing user")
@handle_exception
async def delete_user(username: str = Form(...)) -> None:
    """
    API endpoint to delete a user by username.
    """
    return await DeleteUser.execute(username)


@app.get("/", summary="Retrieve all users")
@handle_exception
async def all_users() -> list:
    """
    API endpoint to retrieve all users in the database.
    """
    return await GetAllUsers.execute()


