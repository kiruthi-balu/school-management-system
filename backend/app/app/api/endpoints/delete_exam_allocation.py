from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import ExamAllocation, User
from app.api.deps import get_db,admin_only_user


router = APIRouter()

@router.post("/delete-exam-allocation/{allocation_id}")
def delete_exam_allocation(allocation_id: int,user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    allocation = db.query(ExamAllocation).filter(ExamAllocation.id == allocation_id, ExamAllocation.status != -1).first()
    
    if not allocation:
        return {"status": 0, "message": "Exam allocation not found"}

    allocation.status = -1
    allocation.m_by = user.id
    db.commit()

    return {"status": 1, "message": "Exam allocation deleted"}
