from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import Exam, User
from app.api.deps import get_db, get_user_from_token

router = APIRouter()

@router.post("/add-exam/")
def create_exam(Exam_name: str = Form(...),token: str = Form(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)

    if user.user_type != 1:
        return {"Status":0,"Message":"Only Admin can add exams"}

    existing = db.query(Exam).filter(Exam.name == Exam_name, Exam.status != -1).first()
    if existing:
        return {"status": 0, "message": "Exam already exists"}

    new_exam = Exam(
        name=Exam_name,
        c_by=user.id,
        m_by=user.id
    )
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return {"status": 1, "message": "Exam created successfully", "exam_id": new_exam.id}
