from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token
from app.models import Standard
from datetime import datetime

router = APIRouter()

@router.post("/update-standard/")
def update_standard(standard_id: int = Form(...),new_name: str = Form(...),token: str = Form(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)

    if user.user_type != 1:
        return {"Status":0,"Message":"Only admin can update standards"}

    standard = db.query(Standard).filter(Standard.standard_id == standard_id, Standard.status == 1).first()
    if not standard:
        return {"Status":0,"Message":"Standard not found"}


    standard.name = new_name
    standard.m_by = user.id
    standard.m_at = datetime.now()

    db.commit()
    db.refresh(standard)

    return {"status": 1, "message": "Standard updated successfully"}
