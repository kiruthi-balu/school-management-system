from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user
from app.models import ExamAllocation, User, Exam, AcademicYearClass, Standard, Section

router = APIRouter()

@router.post("/view-exam-allocations/")
def view_exam_allocations(user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    
    allocations = (db.query(ExamAllocation.id,Exam.name.label("exam_name"),Standard.name.label("standard_name"),Section.name.label("section_name"))
        .join(Exam, Exam.id == ExamAllocation.exam_id).join(AcademicYearClass, AcademicYearClass.id == ExamAllocation.ac_class_id).join(Standard, Standard.id == AcademicYearClass.standard_id)
        .join(Section, Section.id == AcademicYearClass.section_id).filter(ExamAllocation.status == 1).all())

    if not allocations:
        return {"status": 0, "message": "No exam allocations found"}

    return {
        "status": 1,
        "data": [
            {
                "id": alloc.id,
                "exam_name": alloc.exam_name,
                "class": f"{alloc.standard_name}-{alloc.section_name}"
            }
            for alloc in allocations
        ]
    }
