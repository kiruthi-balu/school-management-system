from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, admin_only_user
from app.models import SubjectAllocation, AcademicYearClass, Subject, User


router = APIRouter()




@router.post("/update-subject-allocation/{allocation_id}")
def update_subject_allocation(allocation_id: int,ac_class_id: int = Form(...),subject_id: int = Form(...),user_id: int = Form(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    allocation = db.query(SubjectAllocation).filter(SubjectAllocation.id == allocation_id, SubjectAllocation.status != -1).first()
    if not allocation:
        return {"Status":0,"Message":"Subject allocation not found"}

    allocation.ac_class_id = ac_class_id
    allocation.subject_id = subject_id
    allocation.user_id = user_id
    allocation.m_by = user.id
    db.commit()
    return {"status": 1, "message": "Subject allocation updated"}
