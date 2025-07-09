from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import AcademicYearStudent, User
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/add-academic-student/")
def create_academic_year_student(ac_class_id: int = Form(...),student_id: int = Form(...),user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    existing = db.query(AcademicYearStudent).filter(AcademicYearStudent.ac_class_id == ac_class_id,AcademicYearStudent.student_id == student_id,AcademicYearStudent.status != -1).first()

    if existing:
        return {"status": 0, "message": "Student already assigned to this class"}

    new_entry = AcademicYearStudent(
        ac_class_id=ac_class_id,
        student_id=student_id,
        c_by=user.id
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {"status": 1, "message": "Student assigned to academic class successfully", "id": new_entry.id}
