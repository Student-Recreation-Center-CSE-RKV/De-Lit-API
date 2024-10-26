from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel
from models.email import EmailRequest, config


conf = config(
    MAIL_USERNAME="rr200026@rguktrkv.ac.in",
    MAIL_PASSWORD="kgzv qioy zgzy xjzc",
    MAIL_FROM="rr200026@rguktrkv.ac.in",
    MAIL_FROM_NAME="De-Lit",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="",
)


mail_conf = ConnectionConfig(
    MAIL_USERNAME=conf.MAIL_USERNAME,
    MAIL_PASSWORD=conf.MAIL_PASSWORD,
    MAIL_FROM=conf.MAIL_FROM,
    MAIL_FROM_NAME=conf.MAIL_FROM_NAME,
    MAIL_PORT=conf.MAIL_PORT,
    MAIL_SERVER=conf.MAIL_SERVER,
    MAIL_STARTTLS=conf.MAIL_TLS,
    MAIL_SSL_TLS=conf.MAIL_SSL,
    USE_CREDENTIALS=conf.USE_CREDENTIALS,
    TEMPLATE_FOLDER=conf.TEMPLATE_FOLDER,
)


fast_mail = FastMail(mail_conf)


async def plain_mail(email_request: EmailRequest):
    try:
        message = MessageSchema(
            subject=email_request.subject,
            recipients=email_request.recipients,
            body=email_request.body,
            subtype="plain",
        )
        await fast_mail.send_message(message)
        raise HTTPException(status_code=200, detail="Mail sent successfully")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while sending mail: {str(e)}"
        )
