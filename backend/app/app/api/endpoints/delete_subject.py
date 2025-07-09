from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token
from app.models import Subject, User
from datetime import datetime

router = APIRouter()


@router.post("/delete-subject/")
def delete_subject(subject_id: int = Form(...),token: str = Form(...),db: Session = Depends(get_db)):
    
    
    user = get_user_from_token(token, db)

    if user.user_type != 1:
        return {"Status":0, "Message":"Only admin can delete subjects"}

    subject = db.query(Subject).filter(Subject.id == subject_id, Subject.status == 1).first()
    if not subject:
        return {"Status":0, "Message":"Subject not found or already deleted"}

    subject.status = -1
    subject.m_by = user.id
    subject.m_at = datetime.now()

    db.commit()

    return {"status": 1, "message": "Subject deleted successfully"}
