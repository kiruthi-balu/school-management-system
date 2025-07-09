from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from datetime import date
from app.models import Attendance
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/add-attendance/")
def add_individual_attendance(student_id: int = Form(..., description="User ID of the student"),attendance_date: date = Form(..., description="Date of attendance"),present: str = Form(..., description="Present/Absent"),session_status: int = Form(..., description="1: Full Day, 2: Morning, 3: Afternoon, 4: On Duty"),user = Depends(master_access_user),db: Session = Depends(get_db)):
    
    existing = db.query(Attendance).filter(Attendance.user_id == student_id,Attendance.date == attendance_date,Attendance.status != -1  ).first()

    if existing:
        return {"Status":0, "Message":"Attendance already marked for this student on this date"}

    attendance = Attendance(
        user_id=student_id,
        date=attendance_date,
        present=present,
        status=session_status,
        c_by=user.id
    )
    db.add(attendance)
    db.commit()

    return {"status": 1, "message": "Attendance added successfully","id": attendance.id}
