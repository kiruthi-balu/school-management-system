from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, admin_only_user
from app.models import SubjectAllocation, AcademicYearClass, Subject, User

router=APIRouter()


@router.post("/delete-subject-allocation/{allocation_id}")
def delete_subject_allocation(allocation_id: int,user: User = Depends(admin_only_user),db: Session = Depends(get_db)):

    allocation = db.query(SubjectAllocation).filter(SubjectAllocation.id == allocation_id, SubjectAllocation.status != -1).first()
    
    if not allocation:
        return {"Status":0, "Message":"Subject allocation not found"}

    allocation.status = -1
    allocation.m_by = user.id
    db.commit()
    return {"status": 1, "message": "Subject allocation deleted successfully"}
