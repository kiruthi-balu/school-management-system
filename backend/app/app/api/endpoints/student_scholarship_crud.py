from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from sqlalchemy import not_
from app.models import StudentScholarship, User, AcademicYearStudent, Scholarship
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/create-student-scholarship")
def create_student_scholarship(acy_stud_id: int,scholarship_id: int,is_paid: str,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    acy_student = db.query(AcademicYearStudent).filter_by(id=acy_stud_id, status=1).first()
    if not acy_student:
        return{"Status":0,"Message":"Academic Year Student not found"}

    scholarship = db.query(Scholarship).filter_by(id=scholarship_id, status=1).first()
    if not scholarship:
        return{"Status":0,"Message":"Scholarship not found"}

    record = StudentScholarship(
        acy_stud_id=acy_stud_id,
        scholarship_id=scholarship_id,
        is_paid=is_paid,
        c_by=user.id
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"status": 1, "message": "Student scholarship added", "id": record.id}


@router.post("/view-student-scholarships")
def view_student_scholarships(
    user: User = Depends(master_access_user),
    db: Session = Depends(get_db)
):
    records = db.query(StudentScholarship).filter(not_(StudentScholarship.status == -1)).all()
    return {
        "status": 1,
        "data": [
            {
                "id": r.id,
                "acy_stud_id": r.acy_stud_id,
                "scholarship_id": r.scholarship_id,
                "is_paid": r.is_paid,
                "status": r.status
            } for r in records
        ]
    }


@router.post("/update-student-scholarship/{record_id}")
def update_student_scholarship(record_id: int,scholarship_id: Optional[int] = None,acy_stud_id: Optional[int] = None,is_paid: Optional[str] = None,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    record = db.query(StudentScholarship).filter(StudentScholarship.id == record_id, StudentScholarship.status != -1).first()

    if not record:
        return{"Status":0,"Message":"Record not found"}

    if scholarship_id:
        record.scholarship_id = scholarship_id
    if acy_stud_id:
        record.acy_stud_id = acy_stud_id
    if is_paid:
        record.is_paid = is_paid

    record.m_by = user.id
    record.m_at = datetime.now()

    db.commit()
    return {"status": 1, "message": "Student scholarship updated"}


@router.post("/delete-student-scholarship/{record_id}")
def delete_student_scholarship(record_id: int,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    record = db.query(StudentScholarship).filter(StudentScholarship.id == record_id, StudentScholarship.status != -1).first()
    if not record:
        return{"Status":0,"Message":"Record not found"}

    record.status = -1
    record.m_by = user.id
    record.m_at = datetime.now()

    db.commit()
    return {"status": 1, "message": "Student scholarship deleted"}
