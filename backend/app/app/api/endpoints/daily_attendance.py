from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Attendance, AcademicYearClass, AcademicYearStudent
from app.api.deps import get_db, marks_view_access
from datetime import date

router = APIRouter()

@router.post("/daily-attendance/", description=" Get daily (particular date) attandance data of a class")
def get_daily_attendance(ac_class_id: int = Query(...),att_date: date = Query(...),db: Session = Depends(get_db),user = Depends(marks_view_access)):
    
    
    students = db.query(AcademicYearStudent).filter(AcademicYearStudent.ac_class_id == ac_class_id,AcademicYearStudent.status == 1).all()

    student_ids = [s.student_id for s in students]

    if not student_ids:
        return {"status": 0, "message": "No students in this class"}

    results = db.query(
        Attendance.user_id,
        Attendance.present,
        Attendance.status,
        Attendance.date
    ).filter(
        Attendance.user_id.in_(student_ids),
        Attendance.date == att_date,
        Attendance.status != -1
    ).all()

    response = []
    for row in results:
        response.append({
            "student_id": row.user_id,
            "present": row.present,
            "status": row.status,
            "date": row.date
        })

    return {
        "status": 1,
        "date": att_date,
        "attendance": response
    }
