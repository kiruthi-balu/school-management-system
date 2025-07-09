from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user
from app.models import SubjectAllocation, Subject, User, AcademicYearClass, Standard, Section

router = APIRouter()

@router.post("/view-subject-allocations/")
def view_subject_allocations(user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    
    allocations = (db.query(SubjectAllocation.id,Subject.name.label("subject_name"),User.name.label("teacher_name"),Standard.name.label("standard_name"),Section.name.label("section_name"))
        .join(Subject, Subject.id == SubjectAllocation.subject_id)
        .join(User, User.id == SubjectAllocation.user_id)
        .join(AcademicYearClass, AcademicYearClass.id == SubjectAllocation.ac_class_id)
        .join(Standard, Standard.id == AcademicYearClass.standard_id)
        .join(Section, Section.id == AcademicYearClass.section_id)
        .filter(SubjectAllocation.status == 1).all())

    if not allocations:
        return {"status": 0, "message": "No subject allocations found"}

    return {
        "status": 1,
        "data": [
            {
                "id": alloc.id,
                "subject": alloc.subject_name,
                "teacher": alloc.teacher_name,
                "class": f"{alloc.standard_name}-{alloc.section_name}"
            }
            for alloc in allocations
        ]
    }
