from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import TimeTable
from app.api.deps import get_db, master_access_user
from app.models import User

router = APIRouter()

@router.post("/update-timetable/")
def update_timetable(id: int = Form(...),day: str = Form(None),period: int = Form(None),user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    timetable = db.query(TimeTable).filter(TimeTable.id == id, TimeTable.status != -1).first()
    
    if not timetable:
        return{"Status":0,"Message":"Timetable not found"}

    if day:
        timetable.day = day
    if period:
        timetable.period = period
    timetable.m_by = user.id

    db.commit()
    db.refresh(timetable)

    return {"status": 1, "message": "Timetable updated successfully"}
