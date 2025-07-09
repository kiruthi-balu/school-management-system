from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.models import AcademicYearStudent, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/delete-academic-year-student/{student_record_id}")
def delete_academic_year_student(student_record_id: int = Path(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):

    record = db.query(AcademicYearStudent).filter(AcademicYearStudent.id == student_record_id, AcademicYearStudent.status != -1).first()

    if not record:
        return{"Status":0,"Message":"Academic year student record not found"}

    record.status = -1
    record.m_by = user.id

    db.commit()

    return {"status": 1, "message": "Academic year student record deleted"}
