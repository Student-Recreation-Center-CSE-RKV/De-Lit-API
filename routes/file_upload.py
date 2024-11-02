from fastapi import APIRouter, File, UploadFile
from utilities.utils import handle_exception
from controller.file_upload_controller import UploadFileToGit

app = APIRouter()

@app.post("/")
@handle_exception
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the server. The file is stored in the GitHub and its link is stored in the MongoDB database.

    Args:

        file (UploadFile): The file to be uploaded.

    Returns:

        dict: A dictionary containing the message "File uploaded successfully" and the "_id" of the file in the database.

    Raises:

        HTTPException: If there is an error while uploading the file.
    """
    return await UploadFileToGit.execute(file = file)