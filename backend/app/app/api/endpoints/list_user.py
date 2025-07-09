from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, marks_view_access
from app.models import AcademicYearStudent, User, AcademicYearClass, Standard, Section
from app.utils import get_pagination, paginate 
from sqlalchemy import func

router = APIRouter()

@router.post("/list-students-info/")
def list_students_info(token: str = Query(...),page: int = Query(1, ge=1),size: int = Query(10, ge=1),db: Session = Depends(get_db)):
    
    
    user = marks_view_access(token, db)
    if isinstance(user, dict) and user.get("Status") == 0:
        return user

    total_count = (db.query(func.count(AcademicYearStudent.id)).join(User, AcademicYearStudent.student_id == User.id).filter(User.user_type == 6, User.status == 1, AcademicYearStudent.status == 1).scalar())


    total_pages, offset, limit = get_pagination(total_count, page, size)

    results = (
        db.query(User.id.label("user_id"),AcademicYearStudent.id.label("academic_year_student_id"),Standard.name.label("standard"),Section.name.label("section"),User.name.label("student_name"))
        .join(AcademicYearStudent, AcademicYearStudent.student_id == User.id).join(AcademicYearClass, AcademicYearStudent.ac_class_id == AcademicYearClass.id)
        .join(Standard, AcademicYearClass.standard_id == Standard.id).join(Section, AcademicYearClass.section_id == Section.id)
        .filter(User.user_type == 6, User.status == 1, AcademicYearStudent.status == 1).order_by(Standard.name, Section.name, User.name).offset(offset).limit(limit).all())

    students = []
    for row in results:
        students.append({
            "user_id": row.user_id,
            "academic_year_student_id": row.academic_year_student_id,
            "class": f"{row.standard} - {row.section}",
            "name": row.student_name
        })

    return paginate(page, size, students, total_pages, total_count)
