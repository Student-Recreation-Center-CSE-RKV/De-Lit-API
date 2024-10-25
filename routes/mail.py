from fastapi import APIRouter, HTTPException
from utilities.utils import client, handle_exception
from utilities.gtihub_utilities import upload_to_github, delete_file_from_github

app = APIRouter()


mydb = client['Delit-test']
mail_db = mydb.mail

@app.post('/')
@handle_exception
async def add_mail_id(mail_id : str):
    """It is to add mail id in database. The mail ids are subscribed by the users.

    Args:
        mail_id (str): it is the mail id of user

    Returns:
        _type_: _description_
    """
    res = await mail_db.find_one({"mail_id":mail_id})
    print(res)
    if res == None:
        mail_db.insert_one({"mail_id":mail_id})
    else:
        return {"Message":"Already subscribed"}
    return {"mail_id":mail_id}