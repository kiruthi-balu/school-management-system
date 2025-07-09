from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import ExamAllocation, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/create-exam-allocation/")
def create_exam_allocation(exam_id: int = Form(...),ac_class_id: int = Form(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    existing = db.query(ExamAllocation).filter(ExamAllocation.exam_id == exam_id,ExamAllocation.ac_class_id == ac_class_id,ExamAllocation.status != -1).first()
    
    if existing:
        return {"status": 0, "message": "Exam already allocated to this class"}

    allocation = ExamAllocation(
        exam_id=exam_id,
        ac_class_id=ac_class_id,
        c_by=user.id,
        m_by=user.id
    )
    db.add(allocation)
    db.commit()
    db.refresh(allocation)

    return {"status": 1, "message": "Exam allocation created", "allocation_id": allocation.id}
