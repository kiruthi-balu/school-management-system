from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from typing import Optional
from sqlalchemy import or_
import random
from app.api.deps import generate_api_token, get_db
from app.schemas.createuserschema import CreateUser


router = APIRouter()

@router.post("/Create-Users/")
def create_user(payload:CreateUser,token:str, db:Session=Depends(get_db)):

    token_record = db.query(Apitoken).filter(Apitoken.token == token, Apitoken.status == 1).first()
    if not token_record:
        return {"status":0 , "message": "Invalid or expired token"}


    get_user = db.query(User).filter(User.id==token_record.user_id, User.status==1).first()

    if not get_user:
        return  {"status":0 , "message": "User not found or Invalid User"}

    creator_type = get_user.user_type
    new_user_type = payload.user_type

    if creator_type == 1:  
        pass
    elif creator_type in [2, 3, 4]:  
        if new_user_type != 6:
            return {"status": 0, "message": "You are only allowed to create student users."}
    else:
        return {"status": 0, "message": "You are not allowed to create any users."}


    existing_user = db.query(User).filter(
        or_(User.email == payload.email, User.name == payload.name)
    ).first()
    if existing_user:
        return {"status":0, "message": "User with this name or email already exists."}
    
    hashed_password = get_password_hash(payload.password)
    new_user = User(
        name= payload.name,
        email = payload.email,
        password = hashed_password,
        gender= payload.gender,
        Dateofbirth= payload.Dateofbirth,
        aadhaar_num=payload.aadhaar_num,
        Father_name= payload.Father_name,
        Mother_name= payload.Mother_name,
        guardian_name=payload.guardian_name,
        Address= payload.Address,
        city = payload.city,
        pincode=payload.pincode,
        Father_pnum=payload.Father_pnum,
        mother_pnum=payload.mother_pnum,
        guardian_pnum=payload.guardian_pnum,
        blood_group = payload.blood_group,
        religion= payload.religion,
        nationality=payload.nationality,
        community = payload.community,
        is_hostel = payload.is_hostel,
        admission_date= payload.admission_date,
        dummy = payload.dummy,
        user_type= payload.user_type,
        c_by=payload.c_by
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": 1,
        "message": f"{'Student' if new_user_type == 6 else 'Staff'} user created successfully",
        "user_id": new_user.id
    }


