from utilities.mail_utils import plain_mail
from fastapi import APIRouter, HTTPException
from utilities.utils import client, handle_exception
from utilities.gtihub_utilities import upload_to_github, delete_file_from_github
from models.email import EmailRequest

app = APIRouter()


mydb = client["Delit-test"]
mail_db = mydb.mail


@app.post("/")
@handle_exception
async def add_mail_id(mail_id: str):
    """It is to add mail id in database. The mail ids are subscribed by the users.

    Args:
        mail_id (str): it is the mail id of user

    Returns:
        _type_: _description_
    """
    res = await mail_db.find_one({"mail_id": mail_id})
    print(res)
    if res == None:
        mail_db.insert_one({"mail_id": mail_id})
        message = EmailRequest(
            subject="Subscribe",
            recipients=[mail_id],
            body="Thank you for subscribing De-Lit. We will send you updates.",
        )
        res = await plain_mail(message)
        if res.status_code != 200:
            mail_db.delete_one({"mail_id": mail_id})
            raise HTTPException(
                status_code=500, detail="Failed Subscibe subscribe again"
            )
    else:
        message = EmailRequest(
            subject="Already subscribed",
            recipients=[mail_id],
            body="We apprecite your efforts for subscibing to De-Lit,but you are already subscribed .We will send you updates.",
        )
        res = await plain_mail(
            message,
        )
        return {"Message": "Already subscribed"}
    return {"mail_id": mail_id}
