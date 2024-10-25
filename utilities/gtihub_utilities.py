from .utils import GITHUB_TOKEN, REPO_OWNER, REPO_NAME, FOLDER_PATH
import httpx
import datetime
import base64
from fastapi import HTTPException
import re

async def upload_to_github(file_content, file_name):
    """ Uploading the actual image file into github repository

    Args:
        file_content ( File ): actual file 
        file_name ( str ): name of the file

    Returns:
        object : httpx.Response object
    """    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FOLDER_PATH}/{file_name}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Get current time for commit message
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "message": f"Add {file_name} at {now}",
        "content": base64.b64encode(file_content).decode("utf-8") # Encode image content into base64
    }
    response = httpx.put(url, json=data, headers=headers)
    return response


async def delete_file_from_github(link: str):
    """ Delete the file from github repository

    Args:
        link (str): path of the file 

    Raises:
        HTTPException: 404 (if repository not found)

    Returns:
        object : httpx.Response object
    """
    pattern = r"blob/[^/]+/(.+)"
    match = re.search(pattern, link)
    if not match:
        HTTPException(
            status_code=404, detail="Link Not Found"
        )
    file_path = match.group(1)

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(
            status_code=404, detail="Folder not found"
        )
    sha = response.json()["sha"]
    data = {
        "message": f"Delete {file_path}",
        "sha": sha
    }
    response = httpx.delete(url, params=data, headers=headers)
    return response
