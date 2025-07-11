
from typing import Generator
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.session import SessionLocal
from app.core.config import settings
from datetime import datetime
import random
from app.models import Apitoken, User, AcademicYearStudent, AcademicYearClass
from sqlalchemy.orm import Session
from fastapi import Depends


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token")

"""Initializing the database Connection"""
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def generate_api_token(user_id: int, db: Session) -> str:
    char1 = "qwertyuioplkjhgfdsazxcvbnm1234567890"
    char2 = "QWERTYUIOPLKJHGFDSAZXCVBNM01234567890"
    mixed = char1 + char2
    key = "".join(random.choices(mixed, k=30))
    token = f"{key}{user_id}HKLvk001"

    create_token = Apitoken(
        user_id=user_id,
        token=token,
        created_at=datetime.now(),
        status=1
    )
    db.add(create_token)
    db.commit()

    return token

ALLOWED_ROLES_FOR_MASTER = [1, 2, 3, 4]  # 1:Admin, 2:Principal, 3:Teacher, 4:Office Staff

def get_user_from_token(token: str, db: Session) -> User|dict:
    token_record = db.query(Apitoken).filter(Apitoken.token == token, Apitoken.status == 1).first()
    if not token_record:
        return {"Status":0,"Message":"Invalid or expired token"}

    user = db.query(User).filter(User.id == token_record.user_id, User.status == 1).first()
    if not user:
        return {"Status":0,"Message":"User not found or inactive"}


    return user

def master_access_user(token: str, db: Session = Depends(get_db)) :
    user = get_user_from_token(token, db)
    if isinstance(user, dict):
        return user
    if user.user_type not in ALLOWED_ROLES_FOR_MASTER:
        return {"Status":0, "Message":"You are not allowed to modify master tables"}
    return user


def can_update_user(current_user: User, target_user: User, db: Session) -> bool:

    if current_user.user_type in [1, 2, 4]:
        return True

    if current_user.user_type == 3 and current_user.id == target_user.id:
        return True

    if current_user.user_type == 3 and target_user.user_type == 6:  
        teacher_classes = db.query(AcademicYearClass).filter(AcademicYearClass.staff_id == current_user.id,AcademicYearClass.status == 1).all()

        for class_obj in teacher_classes:
            is_student_in_class = db.query(AcademicYearStudent).filter(AcademicYearStudent.ac_class_id == class_obj.id,AcademicYearStudent.student_id == target_user.id,AcademicYearStudent.status == 1).first()

            if is_student_in_class:
                return True


    return False  


def admin_only_user(token: str, db: Session = Depends(get_db)) -> User|dict:
    user = get_user_from_token(token, db)
    if user.user_type != 1:
        return {"Status":0, "Message":"Only Admin is allowed to access this resource."}
    return user



def teacher_access_user(token: str, db: Session = Depends(get_db)) -> User|dict:
    token_data = db.query(Apitoken).filter(Apitoken.token == token, Apitoken.status == 1).first()
    if not token_data:
        return {"Status":0, "Message":"Invalid or expired token"}

    user = db.query(User).filter(User.id == token_data.user_id, User.status == 1).first()
    
    if not user:
        return {"Status":0,"Message":"User not found"}

    if not user.user_type != 3:
        return {"Status":0,"Message":"Only teachers are allowed to add marks"}
    
    return user


def marks_view_access(token: str, db: Session = Depends(get_db)) -> User| dict:

    token_data = db.query(Apitoken).filter(Apitoken.token == token, Apitoken.status == 1).first()
    if not token_data:
        return {"Status":0,"Message":"Invalid or expired token"}

    user = db.query(User).filter(User.id == token_data.user_id, User.status == 1).first()
    if not user:
        return {"Status":0,"Message":"User not found"}
    print("program working")

    if user.user_type not in ALLOWED_ROLES_FOR_MASTER:
        return {"Ststus":0,"Message":"You are not authorized to view mark sheets"}


    return user