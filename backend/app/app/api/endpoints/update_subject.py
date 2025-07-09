from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token
from app.models import Subject, User
from datetime import datetime

router = APIRouter()

@router.post("/update-subject/")
def update_subject(subject_id: int = Form(...),new_name: str = Form(...),token: str = Form(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)

    if user.user_type != 1:
        return {"Status":0,"Message":"Only admin can update subjects"}

    subject = db.query(Subject).filter(Subject.id == subject_id, Subject.status == 1).first()
    if not subject:
        return {"Status":0,"Message":"ubject not found"}


    subject.name = new_name
    subject.m_by = user.id
    subject.m_at = datetime.now()

    db.commit()
    db.refresh(subject)

    return {"status": 1, "message": "Subject updated successfully", "updated_name": subject.name}
