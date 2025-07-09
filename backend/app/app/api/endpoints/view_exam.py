from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Exam, User
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/view-exams/")
def view_exams(user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    exams = db.query(Exam).filter(Exam.status != -1).all()
    if not exams:
        return {"status": 0, "message": "No exams found"}
    
    return {
        "status": 1,
        "data": [{"id": e.id, "name": e.name, "status": e.status} for e in exams]
    }
