from fastapi import APIRouter, HTTPException, Form
from utilities.utils import client, handle_exception
app = APIRouter()

mydb = client['Delit-test']
footer_db = mydb.footer

@app.get("/")
@handle_exception
async def links() :
    """
    Summary:
    
        Retrieving all the links

    Raises:
    
        HTTPException: (404) if no data available in the collection

    Returns:
    
        list : list of dictionarys having data of links
    """    
    links = []
    async for link in footer_db.find() :
        link["_id"] = str(link["_id"])
        links.append(link)
    if not links :
        raise HTTPException(
            status_code= 404, detail="There are no links available in this collection"
        )
    return links

@app.get("/{app_name}") 
@handle_exception
async def individual(app_name : str) :
    """
    Summaru :
    
        Retrieving document for given application
    
    Args:
    
        app_name (str): app_name of the application

    Raises:
    
        HTTPException: (422) if app_name not given
        HTTPException: (404) if app_name not found in the database

    Returns:
    
        dictionary : document(app_link) of given application
    """    
    
    if app_name is None :
        raise HTTPException(
            status_code=422, detail="Provide sufficient data"
        )
    link = await footer_db.find_one({"app_name" : app_name})
    if link is None:
        raise HTTPException(
            status_code=404, detail="There is no thing like that. Enter proper details"
        )
    link["_id"] = str(link["_id"])
    return link

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
    if app_name=="string" or app_link=="string" :
        raise HTTPException(
            status_code=422, detail="Provide sufficient detials")
        
    status = await footer_db.find_one({"app_name" : app_name})
    if status is None :
        raise HTTPException(
            status_code=404, detail= f"No document is there for {app_name}")
        
    dictionary = {"app_link" : app_link}
    result = await footer_db.update_one(
        {"app_name" : app_name},
        {"$set" : dictionary}
    )
    if result.modified_count :
        return {"status" :"success", "message" : "link updated successfullyt"}
    else :
        raise HTTPException(
            status_code=404, detail="Document not found or No changes made ")