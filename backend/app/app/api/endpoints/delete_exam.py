from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.models import Exam, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/delete-exam/{exam_id}")
def delete_exam(exam_id: int = Path(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.status != -1).first()
    
    if not exam:
        return {"Status":0, "Message":"Exam Not Found"}

    exam.status = -1
    exam.m_by = user.id
    db.commit()

    return {"status": 1, "message": "Exam deleted successfully"}
