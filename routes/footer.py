from fastapi import APIRouter, Form
from utilities.utils import handle_exception
from pydantic import BaseModel
from controller.footer_controller import (
    GetAllApplicationLinks,
    GetApplicationLinkById,
    UploadApplicationLink,
    UpdateApplicationLink,
    DeleteApplicationLink
)

app = APIRouter()

@app.get("/")
@handle_exception
async def get_application_links() :
    """
    Summary:
    
        Retrieving all the links

    Raises:
    
        HTTPException: (404) if no data available in the collection

    Returns:
    
        list : list of dictionaries having data of links
    """    
    return await GetAllApplicationLinks.execute()

@app.get("/{id}") 
@handle_exception
async def get_individual_link(id : str) :
    """
    Summary :
    
        Retrieving link for given application
    
    Args:
    
        app_name (str): app_name of the application

    Raises:
    
        HTTPException: (422) if app_name not given
        HTTPException: (404) if app_name not found in the database

    Returns:
    
        dictionary : document(app_link) of given application
    """    
    return await GetApplicationLinkById.execute(id = id)


@app.put("/{app_name}")
@handle_exception
async def update(app_name : str, app_link : str = Form(...)) :
    """
    Summary :
    
        Link is updated for different application

    Args :
    
        app_name : app_name of the application
        app_link : app_link to be updated for the given application

    Raises:
    
        HTTPException: (422) if app_name and app_link not provided
        HTTPException: (404) if there is no document for given application
        HTTPException: (404) if document is not updated 

    Returns:
    
        dictionary : return status(success) and message(Document is updated)
    """    
    return await UpdateApplicationLink.execute(app_name = app_name, app_link = app_link)
