from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, admin_only_user
from app.models import SubjectAllocation, AcademicYearClass, Subject, User


router = APIRouter()


@router.post("/create-subject-allocation/")
def create_subject_allocation(ac_class_id: int = Form(...),subject_id: int = Form(...),user_id: int = Form(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    allocation = SubjectAllocation(
        ac_class_id=ac_class_id,
        subject_id=subject_id,
        user_id=user_id,
        c_by=user.id
    )
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return {"status": 1, "message": "Subject allocation created", "id": allocation.id}
