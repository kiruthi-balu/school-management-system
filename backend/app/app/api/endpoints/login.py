
from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_

import random


router = APIRouter()
dt = str(int(datetime.utcnow().timestamp()))

@router.post("/signup-user")
async def signup_user(db:Session=Depends(deps.get_db),
                      user_name:str=Form(...),first_name:str=Form(...),
                      last_name:str=Form(None),group_type:int=Form(...),
                      email:str=Form(...),phone_number:str=Form(None),
                      password:str=Form(...)):
    
    get_user = db.query(User).filter(User.status ==1)
    
    check_user_name = get_user.filter(User.user_name == user_name).first()
    if check_user_name:
        return {"status":0,"msg":"User name already exits."}
    
    check_email =  get_user.filter(User.email == email).first()
    if check_email:
        return {"status":0,"msg":"Email already exits."}
    
    check_mobile =  get_user.filter(User.phone_number == phone_number).first()
    if check_mobile:
        return {"status":0,"msg":"Mobile number already exits."}
    
    create_user = User(
 
        user_name = user_name,
        first_name = first_name,
        last_name = last_name,
        email = email,
        phone_number = phone_number,
        group_type = group_type,
        password = get_password_hash(password), 
        created_at = datetime.now(),
        status = 1 )
    db.add(create_user)
    db.commit()
    
    return {"status":1,"msg":"Now you can enjoy with your credentials keep login"}

@router.post('/login-user')
async def login_user(db:Session=Depends(deps.get_db),password:str=Form(...),
                    user_name:str=Form(...)):
    checkUser = db.query(User).filter(or_(User.user_name == user_name,
                                          User.email == user_name,
                                          User.phone_number == user_name),
                                      User.status ==1).first()
    
    if not checkUser:
        return {"status":0,"msg":"User not found."}
    password_verification = verify_password(checkUser.password, password)
    if not password_verification:
        return {"status":0,"msg":"Password might be worng."}
    else:
        char1 = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
        char2 = 'QWERTYUIOPLKJHGFDSAZXCVBNM0123456789'
        reset_character = char1 + char2
        key = ''.join(random.choices(reset_character, k=30))
        
        token =f"{key}nTew20drhkl"
    
        create_token = Apitoken(
            user_id = checkUser.id,
            token = token,
            created_at = datetime.now(),
            status = 1
        )
        db.add(create_token)
        db.commit()
        
        return {"status":1,"msg":"Login successfully","token":token}
    
    
    
        
        
    
        
        