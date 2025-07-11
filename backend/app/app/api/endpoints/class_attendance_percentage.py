from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Attendance, AcademicYearClass, AcademicYearStudent
from app.api.deps import get_db, master_access_user
from datetime import date


router = APIRouter()

@router.post("/class-attendance-percentage/", description="Entire class all date percentage")
def get_attendance_percentage(ac_class_id: int = Query(...),db: Session = Depends(get_db),user = Depends(master_access_user)):
    
    student_ids = db.query(AcademicYearStudent.student_id).filter(AcademicYearStudent.ac_class_id == ac_class_id,AcademicYearStudent.status == 1).all()

    student_ids = [s[0] for s in student_ids]
    if not student_ids:
        return {"status": 0, "message": "No students found in this class."}

    total_possible = db.query(func.count()).filter(Attendance.user_id.in_(student_ids),Attendance.status != -1).scalar()

    present_count = db.query(func.count()).filter(Attendance.user_id.in_(student_ids),Attendance.present == "Present",Attendance.status != -1).scalar()

    percentage = (present_count / total_possible * 100) if total_possible > 0 else 0

    return {
        "status": 1,
        "total_entries": total_possible,
        "present_entries": present_count,
        "attendance_percentage": round(percentage, 2)
    }
