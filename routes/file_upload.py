from fastapi import APIRouter, HTTPException, File, UploadFile
from utilities.utils import handle_exception
from utilities.gtihub_utilities import upload_to_github

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

    file_content = await file.read()

    response = await upload_to_github(file_content, file.filename)

    if response.status_code == 201:
        file_url = response.json().get("content", {}).get("html_url", "")
    else:
        raise HTTPException(
            status_code=400, detail="Error uploading file to GitHub"
        )

    return {"message": "File uploaded successfully", "file_url": file_url}