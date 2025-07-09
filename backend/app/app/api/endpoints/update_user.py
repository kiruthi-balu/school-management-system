from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user, get_user_from_token, can_update_user
from app.models import AcademicYear, User
from datetime import date
from app.schemas.update_user_schema import UpdateUser
router = APIRouter()




@router.post("/update-user/{target_user_id}")
def update_user_info(target_user_id: int,payload: UpdateUser,token: str,db: Session = Depends(get_db)):
    
    current_user = get_user_from_token(token, db)

    target_user = db.query(User).filter(User.id == target_user_id, User.status == 1).first()
    if not target_user:
        return {"status": 0, "message": "Target user not found"}

    if not can_update_user(current_user, target_user, db):
        return {"status": 0, "message": "You do not have permission to update this user"}

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(target_user, field, value)

    db.commit()
    db.refresh(target_user)

    return {"status": 1, "message": "User details updated successfully", "user_id": target_user.id}
