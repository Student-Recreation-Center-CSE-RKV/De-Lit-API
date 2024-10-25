from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List

mail_conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",
    MAIL_PASSWORD="your_password",
    MAIL_FROM="your_email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.example.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)

fast_mail = FastMail(mail_conf)


async def plain_mail(subject_ : str, recipents_ : List[str],body_: str):
    message = MessageSchema(subject = subject_,recipents = recipents_,body = body_,subtype = 'plain')
    try :
        await fast_mail.send_message(message)
    except:
        return HTTPException(status_code=500, content="Error while sending mail.")
    raise HTTPException(status_code=200, detail="Mail sent successfully.")