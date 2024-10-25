from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from utilities.utils import handle_exception
from utilities.gtihub_utilities import upload_to_github

app = APIRouter(tags=['File Upload'])

