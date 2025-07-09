from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import AcademicYearStudent, User
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/view-academic-year-students/")
def view_academic_year_students(
    user: User = Depends(master_access_user),
    db: Session = Depends(get_db)
):
    students = db.query(AcademicYearStudent).filter(AcademicYearStudent.status != -1).all()
    if not students:
        return {"status": 0, "message": "No academic year student data found"}

    data = []
    for stud in students:
        data.append({
            "id": stud.id,
            "student_id": stud.student_id,
            "ac_class_id": stud.ac_class_id,
            "status": stud.status,
            "created_at": stud.c_at,
            "modified_at": stud.m_at
        })
    return {"status": 1, "data": data}
