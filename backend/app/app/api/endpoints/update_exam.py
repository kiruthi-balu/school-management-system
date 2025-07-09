from fastapi import APIRouter, Depends, HTTPException, Path, Form
from sqlalchemy.orm import Session
from app.models import Exam, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/update-exam/{exam_id}")
def update_exam(exam_id: int = Path(...),name: str = Form(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.status != -1).first()
    if not exam:
        return {"Status":0, "Message":"Exam Not Found"}

    exam.name = name
    exam.m_by = user.id
    db.commit()
    db.refresh(exam)

    return {"status": 1, "message": "Exam updated successfully", "data": {"id": exam.id, "name": exam.name}}
