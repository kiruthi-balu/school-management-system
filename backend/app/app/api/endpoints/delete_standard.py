from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token
from app.models import Standard, User
from datetime import datetime

router=APIRouter()

@router.post("/delete-standard/")
def delete_standard(standard_id: int = Form(...),token: str = Form(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)

    if user.user_type != 1:
        return {"Status":0,"Message":"Only admin can delete standards"}

    standard = db.query(Standard).filter(Standard.standard_id == standard_id, Standard.status == 1).first()
    if not standard:
        return {"Status":0,"Message":"Standard not found or already deleted"}


    standard.status = -1
    standard.m_by = user.id
    standard.m_at = datetime.now()

    db.commit()

    return {"status": 1, "message": "Standard deleted successfully"}
