from fastapi import HTTPException,Request
from models.users_model import User
from utilities.login_utilities import login_db,pwd_context

class CreateUser:
    """Handles user-related operations, including creation, deletion, and retrieval."""

    @staticmethod
    async def execute(username: str, password: str) -> dict:
        """
        Creates a user with the given username and password, stores the credentials in the database,
        and returns a success message if the operation is successful.

        Args:
            
            username (str): The username for the new user.
           
            password (str): The password for the new user.

        Returns:
            
            dict: A dictionary containing a success message if the user is created successfully.

        Raises:
            
            HTTPException: 
                - 404 : If there is an error while creating the user. 
                - 409 : If any user already exits with the same username.
                - 422: If the username or password is empty or None, with a message prompting the user to enter valid values.
        """
        if not username:
            raise HTTPException(status_code=422, detail="Please enter a username.")
        if not password:
            raise HTTPException(status_code=422, detail="Please enter a password.")
        if await login_db.find_one({"username": username}):
            raise HTTPException(status_code=409, detail="Username already exists.")
        
        user = User(username=username, password=pwd_context.hash(password)).model_dump()
        result = await login_db.insert_one(user)
        
        if result.inserted_id:
            return {"Message": "User Created Successfully"}
        else:
            raise HTTPException(status_code=404, detail="Error creating the user.")
class DeleteUser:
    @staticmethod
    async def execute(username: str) -> None:
        """
        Deletes a user from the database based on the provided username.

        This function attempts to find a user by username in the `login_db` database. If a matching user is found,
        it proceeds to delete the user record. Based on the result of the deletion operation, it raises an HTTP 
        exception with an appropriate status and message.

        Args:
            username (str): The username of the user to delete.

        Raises:
            HTTPException: 
                - 404: If no user with the provided username is found in the database.
                - 200: If the user is successfully deleted.
                - 500: If there is a failure to delete the user despite finding the user in the database.
                - 422: If the username or password is empty or None, with a message prompting the user to enter valid values.

        Returns:
            None: Raises HTTP exceptions with relevant status codes and messages instead of returning data.
        """
        if not username:
            raise HTTPException(status_code=422, detail="Please enter a username.")
        
        if not await login_db.find_one({"username": username}):
            raise HTTPException(status_code=404, detail="User not found.")
        
        delete_result = await login_db.delete_one({"username": username})

        if delete_result.deleted_count == 1:
            raise HTTPException(status_code=200, detail="User deleted successfully.")
        else:
            raise HTTPException(status_code=500, detail="Failed to delete the user.")
class GetAllUsers:
    @staticmethod
    async def execute() -> list:
        """
        Retrieve all users from the database.

        This function fetches all user records from the 'login_db' collection, 
        converts the '_id' field of each user to a string for JSON serialization, 
        and returns a list of users. If no users are found, an HTTPException with 
        a 404 status code is raised.

        Returns:
            List[dict]: A list of user dictionaries, where each dictionary 
            represents a user's data.

        Raises:
            HTTPException: If no users are found, with a 404 status code and 
            a "No users found" detail message.
        """
        users = []
        async for user in login_db.find():
            user["_id"] = str(user["_id"])
            users.append(user)
        
        if not users:
            raise HTTPException(status_code=404, detail="No users found.")
        
        return users
