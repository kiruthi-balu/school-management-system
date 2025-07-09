from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import ExamAllocation, User
from app.api.deps import get_db, admin_only_user


router=APIRouter()

@router.post("/update-exam-allocation/{allocation_id}")
def update_exam_allocation(allocation_id: int,exam_id: int = Form(...),ac_class_id: int = Form(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    allocation = db.query(ExamAllocation).filter(ExamAllocation.id == allocation_id, ExamAllocation.status != -1).first()
    
    if not allocation:
        return {"status": 0, "message": "Exam allocation not found"}

    allocation.exam_id = exam_id
    allocation.ac_class_id = ac_class_id
    allocation.m_by = user.id

    
    db.commit()
    db.refresh(allocation)

    return {"status": 1, "message": "Exam allocation updated"}
