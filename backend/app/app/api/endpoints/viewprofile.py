from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.api.deps import generate_api_token, get_db
from app.schemas.viewprofilleschema import UserProfileOut


router = APIRouter()

@router.post("/View-Profile/", response_model=UserProfileOut)
def view_profile(token:str, db:Session=Depends(get_db)):

    token_record = db.query(Apitoken).filter(Apitoken.token == token, Apitoken.status == 1).first()
    if not token_record:
        return {"status":0 , "message": "Invalid or expired token"}


    get_user = db.query(User).filter(User.id==token_record.user_id, User.status==1).first()

    if not get_user:
        return  {"status":0 , "message": "User not found or Invalid User"}

    return get_user