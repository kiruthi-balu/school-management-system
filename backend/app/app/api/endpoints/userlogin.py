from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from typing import Optional
from sqlalchemy import or_, and_
import random
from app.api.deps import generate_api_token, get_db
from app.schemas.userloginschema import UserLogin 


router = APIRouter()

@router.post("/user-login/")
def user_login(loguser:UserLogin, db:Session=Depends(deps.get_db)):
    
    data = db.query(User).filter(or_(User.name == loguser.user_name,User.email == loguser.user_name),User.status == 1).first()
    
    if not data:
        return {"status":0 ,"Message":"User Not Found"}


    if not verify_password(loguser.password,data.password):
        return {"status":0 ,"Message":"Incorrect User name/Password"}
    
    db.query(Apitoken).filter(Apitoken.user_id == data.id,Apitoken.status == 1).update({"status": -1})
    db.commit()
    token = generate_api_token(data.id, db)
    return {"status":1 ,"Message": "Login Successfully", "Token":token}

