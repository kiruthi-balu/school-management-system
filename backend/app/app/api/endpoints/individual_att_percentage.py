from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_user_from_token
from app.models import Attendance, User

router = APIRouter()

@router.post("/my-attendance-percentage/")
def get_my_attendance_percentage(token: str = Query(...),db: Session = Depends(get_db)):

    user = get_user_from_token(token, db)
    
    if isinstance(user, dict) and user.get("Status") == 0:
        return user 
    student_id = user.id

    total = db.query(func.count()).filter(Attendance.user_id == student_id,Attendance.status != -1).scalar()


    present = db.query(func.count()).filter(Attendance.user_id == student_id,Attendance.present == "Present",Attendance.status != -1).scalar()

    percentage = (present / total * 100) if total > 0 else 0

    return {
        "status": 1,
        "student_id": student_id,
        "total_days": total,
        "present_days": present,
        "attendance_percentage": round(percentage, 2)
    }
